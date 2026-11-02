"""UML-style deployment diagram of the public demonstration (report 5.2).

Author: 722I0004 · AI-assisted (Claude). Facts from deploy/ (compose.prod.yml, Caddyfile, backup timer)
and docs/part2/test_report/deploy_2026-10-27/cloud_setup.md.
Run: python models/shared/deployment_diagram.py   (needs Graphviz `dot`)
"""
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent / "deployment_diagram"
DOT = r'''digraph D {
graph [rankdir=LR, fontname="Arial", fontsize=16, nodesep=0.4, ranksep=0.7, pad=0.3, dpi=200, labelloc="t",
 label=<<B>SaigonBite deployment (release v0.9-part2)</B><BR/><FONT POINT-SIZE="12">Author 722I0004 · AI-assisted (Claude) · boxes = nodes, inner boxes = execution environments and artifacts</FONT>>];
node [fontname="Arial", fontsize=13, shape=box3d, style=filled, fillcolor="#F4F7FA"];
edge [fontname="Arial", fontsize=11, color="#36454F"];
user [label="«device»\nUser browser\n(phone or PC)\ncustomer, kitchen, shipper,\nadmin, manager", fillcolor="#FFFFFF"];
dns [label="«service»\nDNS (Tenten)\nsaigonbite.io.vn → 34.21.141.239\nfallback 34-21-141-239.sslip.io", shape=box, style="rounded,filled", fillcolor="#FFFFFF"];
subgraph cluster_vm {
  label=<<B>«node» Google Cloud VM saigonbite-vm</B><BR/>e2-medium · Ubuntu · asia-southeast1-b · static IP · firewall 80/443, SSH via IAP only>;
  style="rounded,filled"; fillcolor="#EAF2FB"; color="#7FA7CF";
  subgraph cluster_docker {
    label=<<B>«execution environment» Docker Compose</B>>; style="rounded,filled"; fillcolor="#FFFFFF"; color="#9AA7B4";
    caddy [label="«container» caddy\nHTTPS (Let's Encrypt)\nHTTP → HTTPS 308\nreverse proxy :443 → app:8000", fillcolor="#E8F5E9"];
    app [label="«container» app\ngunicorn + Flask\nsaigonbite package\n(presentation, controllers,\ndomain, data access)", fillcolor="#FFF6E0"];
  }
  disk [label="«device» persistent disk 30 GiB\n/srv/saigonbite/data\nSQLite saigonbite.db (WAL)", shape=cylinder, fillcolor="#F2ECF8"];
  timer [label="«system service»\nsaigonbite-backup.timer\n03:00 VN (20:00 UTC) daily", shape=component, fillcolor="#FFFFFF"];
}
bucket [label="«cloud storage»\nGCS bucket\noff-VM backup copies", shape=cylinder, fillcolor="#FFFFFF"];
snap [label="«snapshot schedule»\ndaily disk snapshots", shape=note, fillcolor="#FFFFFF"];
user -> dns [label="name lookup"];
user -> caddy [label="HTTPS 443"];
caddy -> app [label="HTTP 8000\n(internal network)"];
app -> disk [label="sqlite3\nBEGIN IMMEDIATE"];
timer -> disk [label="online backup\n+ integrity check", style=dashed];
timer -> bucket [label="upload .db.gz", style=dashed];
disk -> snap [style=dotted, arrowhead=none];
}'''


if __name__ == "__main__":
    OUT.with_suffix(".dot").write_text(DOT, encoding="utf-8")
    for fmt in ("svg", "png"):
        subprocess.run(["dot", f"-T{fmt}", str(OUT.with_suffix(".dot")), "-o", str(OUT.with_suffix("." + fmt))], check=True)
    print("wrote", OUT.with_suffix(".png"))
