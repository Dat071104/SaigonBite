"""Contact sheet of the Figma sketch exports for each main use case (report 4.3.3).

Author: 722I0004 · AI-assisted (Claude). The sketches themselves were drawn in Figma by Codex
(AI-assisted) on 27/10/2026; this script only places them side by side with their frame names.
Output: docs/part2/ui/UC-0x/sketch/UC-0x_sketch_sheet.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

UI = Path(__file__).resolve().parent
FONT = "C:/Windows/Fonts/arial.ttf"


def sheet(uc: str) -> Path:
    files = sorted(p for p in (UI / uc / "sketch").glob("*.png") if not p.name.endswith("_sheet.png"))
    w, h, gap, label = 390, 844, 30, 70
    img = Image.new("RGB", (len(files) * (w + gap) + gap, h + label + 2 * gap + 60), "white")
    d = ImageDraw.Draw(img)
    d.text((gap, 12), f"{uc} sketches (low fidelity, drawn in Figma) — Author 722I0004 · AI-assisted (Codex)", fill="#202B36", font=ImageFont.truetype(FONT, 30))
    for k, f in enumerate(files):
        x = gap + k * (w + gap)
        with Image.open(f) as s:
            img.paste(s.convert("RGB").resize((w, h)), (x, 60 + gap))
        d.rectangle((x - 1, 60 + gap - 1, x + w, 60 + gap + h), outline="#9AA7B4", width=2)
        name = f.stem.split(" ", 1)
        d.text((x, 60 + gap + h + 10), name[0], fill="#202B36", font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24))
        d.text((x, 60 + gap + h + 40), name[1][:30] if len(name) > 1 else "", fill="#202B36", font=ImageFont.truetype(FONT, 22))
    out = UI / uc / "sketch" / f"{uc}_sketch_sheet.png"
    img.save(out)
    return out


if __name__ == "__main__":
    for n in range(1, 7):
        print(sheet(f"UC-0{n}"))
