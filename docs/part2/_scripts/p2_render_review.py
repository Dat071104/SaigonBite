"""Render local SVG exports for independent visual inspection, without a console."""
from pathlib import Path
import argparse
import subprocess
import xml.etree.ElementTree as ET

def main():
    p=argparse.ArgumentParser(); p.add_argument('svg',nargs='+'); args=p.parse_args()
    out=Path(r'D:\RAD\FINAL\Part2\notes\P2-root\svg_review'); out.mkdir(parents=True,exist_ok=True)
    edge=Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'); assert edge.exists()
    for value in args.svg:
        src=Path(value).resolve(); src.relative_to(Path(r'D:\RAD\FINAL\SaigonBite\models').resolve())
        root=ET.parse(src).getroot(); box=root.get('viewBox','').split()
        w,h=[round(float(x)) for x in box[2:]] if len(box)==4 else [round(float(root.get(n).removesuffix('px'))) for n in ('width','height')]
        target=out/(src.stem+'.png')
        cmd=[str(edge),'--headless','--disable-gpu','--hide-scrollbars','--no-first-run','--no-default-browser-check','--force-device-scale-factor=1','--user-data-dir='+str(out/'profile'),'--screenshot='+str(target),f'--window-size={w},{h}',src.as_uri()]
        result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60,creationflags=subprocess.CREATE_NO_WINDOW)
        (out/(src.stem+'.log')).write_text(f'exit={result.returncode}\n'+result.stdout+result.stderr,encoding='utf-8')
        assert result.returncode==0 and target.exists(),src
        print(target)

if __name__=='__main__': main()
