"""Record binary SHA-256 manifests for Phase 1's frozen boundaries."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(r"D:\RAD\FINAL")
REPO = ROOT / "SaigonBite"
OUT = ROOT / "Part2/notes"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def manifest():
    result = {}
    for label, base in [("part1", ROOT / "Part1_v2"),
                        ("repo_part1", REPO / "docs/part1"),
                        ("app", REPO / "saigonbite"),
                        ("tests", REPO / "tests"), ("db", REPO / "db")]:
        result[label] = {p.relative_to(base).as_posix(): digest(p)
                         for p in sorted(base.rglob("*")) if p.is_file()
                         and not any(x in p.parts for x in ("__pycache__", ".pytest_cache"))}
    result["entrypoints"] = {n: digest(REPO / n) for n in ("app.py", "init_db.py")}
    result["contracts"] = {n: digest(ROOT / n) for n in (
        "PLAN_SaigonBite_Part2_Final.md", "Part2/content/links.json")}
    return result


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    current = manifest()
    target = OUT / "P1_start_hashes.json"
    if sys.argv[1] == "start":
        if target.exists():
            raise SystemExit("Refusing to replace start manifest")
        target.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print(json.dumps({k: len(v) for k, v in current.items()}))
    else:
        old = json.loads(target.read_text(encoding="utf-8"))
        changes = {k: [n for n in sorted(set(old[k]) | set(v))
                       if old[k].get(n) != v.get(n)] for k, v in current.items()}
        data = {"counts": {k: len(v) for k, v in current.items()},
                "changed": changes, "pass": not any(changes.values())}
        (OUT / "P1_end_hash_check.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(json.dumps(data, indent=2))
        if not data["pass"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
