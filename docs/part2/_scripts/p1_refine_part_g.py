"""Render only the two explicitly framed activities after G1 notation review."""
from pathlib import Path
import hashlib
import json
import runpy
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(r"D:\RAD\FINAL")
MODELS = ROOT / "SaigonBite/models/shared"
NOTES = ROOT / "Part2/notes"


def check_scopes(page, diagram):
    cells = {c.get("id"): c for c in diagram.findall(".//mxCell")}
    for frame in page["activity_frames"]:
        x,y,w,h = frame["rect"]
        for key in frame["nodes"]:
            g = cells[key].find("mxGeometry")
            a,b,c,d = (float(g.get(k)) for k in ("x","y","width","height"))
            assert x <= a and y <= b and a+c <= x+w and b+d <= y+h, (frame["id"],key)
    f,g = page["activity_frames"]
    assert f["rect"][0]+f["rect"][2] <= g["rect"][0]
    assert set(f["nodes"]).isdisjoint(g["nodes"])
    assert set(f["nodes"]+g["nodes"]) == {n["id"] for n in page["nodes"]}
    for edge in diagram.findall('.//mxCell[@edge="1"]'):
        assert edge.get("source") in cells and edge.get("target") in cells


def rasterize(svg):
    png = svg.with_suffix(".png")
    profile = NOTES / "P1_diagram_browser_profile"
    command = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
               "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--force-device-scale-factor=2", f"--user-data-dir={profile}",
               f"--screenshot={png}", "--window-size=1100,760", svg.as_uri()]
    result = subprocess.run(command,capture_output=True,text=True,timeout=45,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    (NOTES / "P1_part_g_refinement_render.log").write_text(result.stdout+result.stderr,encoding="utf-8")
    assert result.returncode == 0 and Image.open(png).size == (2200,1520)
    page = Image.new("RGB",(1123,794),"white")
    scaled = Image.open(png).convert("RGB").resize((869,600),Image.Resampling.LANCZOS)
    page.paste(scaled,(127,97))
    page.save(NOTES / "P1_diagram_a4/swimlane_v2_PartG.a4.png")
    return png


def main():
    renderer = runpy.run_path(str(MODELS / "business_process_v2.py"),run_name="p1_renderer")
    spec = json.loads((MODELS / "swimlane_v2.json").read_text(encoding="utf-8"))
    page = next(p for p in spec["pages"] if p["key"] == "G")
    diagram,svg = renderer["build_page"](page,"swimlane_v2")
    check_scopes(page,diagram)
    bundle = ET.parse(MODELS / "swimlane_v2.drawio")
    container = bundle.getroot()
    old = next(d for d in container if d.get("id") == "G")
    index = list(container).index(old)
    container.remove(old)
    container.insert(index,diagram)
    bundle.write(MODELS / "swimlane_v2.drawio",encoding="utf-8",xml_declaration=True)
    png = rasterize(svg)
    qa_path = MODELS / "business_process_v2.qa.json"
    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    record = next(c for c in qa["checks"] if c["file"] == svg.name)
    record.update(renderer["CHECKS"][-1])
    record.update(svg_sha256=hashlib.sha256(svg.read_bytes()).hexdigest(),
                  png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),activity_frames=2)
    qa["root_refinement"] = {"finding":"G1 R2", "change":"Two named, disjoint activity scopes; each owns its initial and final nodes",
                              "scope_containment_check":True,"current_PartG_visual_review":"PENDING root inspection"}
    qa_path.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("PASS: two disjoint activity frames; all9 semantic nodes scoped; XML endpoints valid; SVG rasterized2200x1520.")


if __name__ == "__main__":
    main()
