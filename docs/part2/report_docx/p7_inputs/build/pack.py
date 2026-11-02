from pathlib import Path
import csv,shutil,zipfile,hashlib,json
B=Path(r'D:\RAD\FINAL');R=B/'SaigonBite';source=R/'docs/part2/latex';dest=B/'Part2/deliverables/Team02_BRS_SRS_for_SaigonBite_latex';dest.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((source/'figure_manifest.csv').open(encoding='utf-8-sig',newline='')));images=sorted({x['source_png'] for x in rows if x['record_type']=='figure'});files=[]
for x in source.rglob('*.tex'):
 rel=x.relative_to(source);out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(x,out);files.append(rel.as_posix())
for x in images:
 out=dest/x;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/x,out);files.append(x)
shutil.copy2(source/'figure_manifest.csv',dest/'figure_manifest.csv');files.append('figure_manifest.csv')
text='''SAIGONBITE PART 2 — LATEX SOURCE / NGUON LATEX\n\nEnglish: Open a terminal in this folder and run:\n  latexmk -pdf main.tex\nRun the command up to two more times if the table of contents changes.\nThe standalone statements can be built using:\n  latexmk -pdf contribution_statement.tex\n  latexmk -pdf ai_usage_log.tex\nMiKTeX can install missing standard packages on first run. Overleaf free may time out with this many images; a local build is recommended.\n\nTieng Viet: Mo terminal trong thu muc nay va chay:\n  latexmk -pdf main.tex\nChay them toi da hai lan neu muc luc thay doi. De bien dich cac ban rieng, chay:\n  latexmk -pdf contribution_statement.tex\n  latexmk -pdf ai_usage_log.tex\nMiKTeX co the cai goi thieu o lan chay dau. Overleaf mien phi co the het thoi gian voi nhieu hinh; nen bien dich tren may.\n\nStage 1 contains sources only. Rendering, page layout and links to the release tag require Stage 2 verification.\n'''
(dest/'README_BUILD.txt').write_text(text,encoding='utf-8');files.append('README_BUILD.txt')
archive=dest.with_suffix('.zip')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for name in sorted(files):z.write(dest/name,name)
with zipfile.ZipFile(archive) as z:
 bad=z.testzip(); names=set(z.namelist());assert bad is None and names==set(files);assert all(x in names for x in images)
receipt={'zip':str(archive),'size_bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'tex_files':sum(x.endswith('.tex') for x in files),'unique_pngs':len(images),'entries':len(files),'zip_test':'PASS','pdf':'NOT PRODUCED'}
(B/'Part2/notes/P7/pack_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
