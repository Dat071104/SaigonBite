"""Build the Phase 3 package policy view from the frozen C0 AST inventory.

Author: 722I0004 · AI-assisted (Codex). Static only; imports no application code.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True

OUT = Path(__file__).resolve().parent
REPO = OUT.parent.parent
INVENTORY_PATH = REPO / "docs/part2/design/code_inventory.json"
STEM = "package_diagram"
WIDTH, HEIGHT = 1800, 1360
ALLOWED = {
    ("presentation", "controllers"),
    ("controllers", "domain"),
    ("controllers", "data_access"),
}

spec = importlib.util.spec_from_file_location("p2_diagram_renderer", OUT / "use_case_diagram.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
class Page(R.Page):
    def export(self):
        # Reuse the immutable renderer's dashed/open visual preset. Restore the
        # semantic kind before serializing Phase 3: these are dependencies,
        # never use-case include relationships.
        dependencies = [edge for edge in self.edges if edge['kind'] == 'dependency']
        for edge in dependencies:
            edge['kind'] = 'include'
        try:
            data = super().export()
        finally:
            for edge in dependencies:
                edge['kind'] = 'dependency'
        data['edges'] = self.edges
        (OUT / (self.stem + '.json')).write_text(json.dumps(data, indent=2), encoding='utf-8')
        return data


def source_package(path: str) -> list[str]:
    parts = list(PurePosixPath(path.replace("\\", "/")).parts)
    if parts and parts[-1].endswith(".py"):
        parts.pop()
    return parts


def resolve_import(path: str, record: dict) -> str:
    module = record.get("module") or ""
    level = int(record.get("level", 0) or 0)
    if not level:
        return module
    parts = source_package(path)
    base = parts[: len(parts) - level + 1]
    suffix = [part for part in module.split(".") if part]
    return ".".join(base + suffix)


def layer_for_path(path: str) -> str:
    path = path.replace("\\", "/")
    if path.startswith("saigonbite/presentation/"):
        return "presentation"
    if path.startswith("saigonbite/business/controllers/"):
        return "controllers"
    if path.startswith("saigonbite/business/domain/"):
        return "domain"
    if path.startswith("saigonbite/data_access/"):
        return "data_access"
    return "outside-layer"


def layer_for_import(module: str) -> str | None:
    prefixes = {
        "saigonbite.presentation": "presentation",
        "saigonbite.business.controllers": "controllers",
        "saigonbite.business.domain": "domain",
        "saigonbite.data_access": "data_access",
    }
    for prefix, layer in prefixes.items():
        if module == prefix or module.startswith(prefix + "."):
            return layer
    return None


def audit_imports(inventory: dict) -> dict:
    edges: dict[tuple[str, str], list[dict]] = defaultdict(list)
    root_imports: list[dict] = []
    composition_root: list[dict] = []
    external_examples: dict[str, set[str]] = defaultdict(set)
    records = []
    for module in inventory["modules"].values():
        src_layer = layer_for_path(module["path"])
        for imp in module.get("imports", []):
            resolved = resolve_import(module["path"], imp)
            if resolved == "saigonbite" or resolved.startswith("saigonbite."):
                record = {
                    "source_file": module["path"],
                    "source_layer": src_layer,
                    "target_module": resolved,
                    "imported_name": imp.get("name"),
                    "line": imp.get("line"),
                }
                records.append(record)
                dst_layer = layer_for_import(resolved)
                if dst_layer and src_layer == "outside-layer":
                    composition_root.append(record)
                elif dst_layer:
                    edges[(src_layer, dst_layer)].append(record)
                else:
                    root_imports.append(record)
            else:
                if src_layer != "outside-layer":
                    external_examples[src_layer].add(resolved or "<relative package import>")

    same_layer = []
    allowed = []
    violations = []
    for (source, target), rows in sorted(edges.items()):
        summary = {
            "source": source,
            "target": target,
            "count": len(rows),
            "source_files": sorted({row["source_file"] for row in rows}),
        }
        if source == target:
            same_layer.append(summary)
        elif (source, target) in ALLOWED:
            allowed.append(summary)
        else:
            violations.append(summary)

    root_nav = [r for r in root_imports if r["source_layer"] == "presentation"]
    return {
        "source": str(INVENTORY_PATH.relative_to(REPO)).replace("\\", "/"),
        "source_commit": inventory.get("commit"),
        "evidence_label": inventory.get("evidence_label"),
        "total_saigonbite_import_records": len(records),
        "allowed_cross_layer": allowed,
        "same_layer": same_layer,
        "violations": violations,
        "presentation_to_root": root_nav,
        "composition_root_wiring": composition_root,
        "outside_layer_imports": root_imports,
        "external_imports_excluded": {
            key: sorted(values) for key, values in sorted(external_examples.items())
        },
        "resolved_internal_imports": records,
    }


def patch_json(data: dict, phase3: dict) -> None:
    path = OUT / f"{STEM}.json"
    current = json.loads(path.read_text(encoding="utf-8"))
    current["author"] = "722I0004 · AI-assisted (Codex)"
    current["phase3"] = phase3
    path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build() -> dict:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    audit = audit_imports(inventory)
    p = Page(
        STEM,
        "Package architecture · allowed dependencies and C0 import audit",
        "4.2",
        WIDTH,
        HEIGHT,
    )
    p.texts[-1]["text"] = "Static import comparison at C0 = 45ac762; no runtime behavior inferred."

    p.node(
        "presentation",
        "«package» presentation\nFlask blueprint modules / view routes\naccount · admin · auth · delivery · kitchen\nmain · order · reports · security\nTemplates and static assets are presentation resources.",
        570,
        100,
        660,
        220,
        "rect",
        "#EAF2FA",
    )
    p.node(
        "controllers",
        "«package» business.controllers\nUC and supporting controllers\nPlaceOrder · OrderTracking · Account · Kitchen · Delivery\nHub · Menu · Voucher · UserAdmin · OrderArchive · Report\nShared coordination and domain error types.",
        570,
        400,
        660,
        260,
        "rect",
        "#E9F4EF",
    )
    p.node(
        "domain",
        "«package» business.domain\nDataclasses · enums · state transitions · business rules\nOrder · Customer · Hub · MenuItem · Payment · Delivery\nNo outward application-layer dependency is allowed.",
        100,
        760,
        680,
        250,
        "rect",
        "#F2EFF9",
    )
    p.node(
        "data_access",
        "«package» data_access\nHand-written parameterised-SQL DAOs\ndatabase module: connection / transaction helper\nLocal PaymentGatewaySimulator adapter.",
        1000,
        760,
        680,
        250,
        "rect",
        "#FFF2E6",
    )

    p.edge(
        "dep_presentation_controllers",
        "presentation",
        "controllers",
        [(900, 320), (900, 400)],
        "«dependency»",
        790,
        345,
        kind="dependency",
    )
    p.edge(
        "dep_controllers_domain",
        "controllers",
        "domain",
        [(690, 660), (690, 710), (780, 710), (780, 760)],
        "«dependency»",
        525,
        705,
        kind="dependency",
    )
    p.edge(
        "dep_controllers_data_access",
        "controllers",
        "data_access",
        [(1110, 660), (1110, 710), (1000, 710), (1000, 760)],
        "«dependency»",
        1125,
        705,
        kind="dependency",
    )

    note = (
        "C0 imports that violate the strict layer graph (shown as notes, never allowed arrows):\n"
        "presentation → domain: 12 imports / 7 modules; presentation → data_access: 3 / 2 modules.\n"
        "data_access → domain: 28 imports / 10 modules (DAO materialisation, enums and rules).\n"
        "presentation.auth → saigonbite.NAV: 1 root import; 14 bootstrap imports include app.py → create_app.\n"
        "Flask, SQLite, standard library and other external imports are outside this layer comparison."
    )
    p.node("actual_import_violations", note, 70, 1035, 1660, 190, "note", "#FFF8E8")

    data = p.export()
    module_map = {
        "presentation": [
            "account", "admin", "auth", "delivery", "kitchen", "main", "order", "reports", "security"
        ],
        "controllers": [
            "PlaceOrderController", "OrderTrackingController", "AccountController", "KitchenController",
            "DeliveryController", "HubController", "MenuController", "VoucherController",
            "UserAdminController", "OrderArchiveController", "ReportController"
        ],
        "domain": [
            "UserAccount", "Customer", "Address", "Hub", "Brand", "MenuItem", "HubMenuItem",
            "Voucher", "Order", "OrderLine", "Payment", "Delivery", "ReplacementOffer", "enums", "rules"
        ],
        "data_access": [
            "CustomerDAO", "DeliveryDAO", "HubDAO", "MenuDAO", "OrderDAO", "PaymentDAO",
            "ReplacementOfferDAO", "ReportDAO", "UserDAO", "VoucherDAO", "database (module)", "PaymentGatewaySimulator"
        ],
    }
    phase3 = {
        "diagram_type": "package",
        "elements": [
            {"class": f"{name} (package)", "attributes": module_map[name], "methods": []}
            for name in ("presentation", "controllers", "domain", "data_access")
        ] + [
            {"class": "C0 import-audit note", "attributes": ["actual forbidden imports", "external-import scope note"], "methods": []}
        ],
        "dependencies": [
            {"source": "presentation", "target": "controllers", "kind": "allowed_dependency"},
            {"source": "controllers", "target": "domain", "kind": "allowed_dependency"},
            {"source": "controllers", "target": "data_access", "kind": "allowed_dependency"},
        ],
        "import_audit": audit,
        "notation": {
            "dashed_open_arrow": "allowed UML package dependency",
            "forbidden_imports": "listed in the note and report; not drawn as allowed arrows",
            "external_imports": "framework, standard-library and third-party imports are outside the app-layer graph",
        },
        "C0": inventory.get("commit"),
    }
    patch_json(data, phase3)
    assert data["min_placed_pt"] >= 9
    return {"stem": STEM, "nodes": len(data["nodes"]), "edges": len(data["edges"]), "min_placed_pt": data["min_placed_pt"], "audit": {k: audit[k] for k in ("total_saigonbite_import_records", "allowed_cross_layer", "same_layer", "violations", "presentation_to_root", "composition_root_wiring")}}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(build(), ensure_ascii=False, indent=2))
