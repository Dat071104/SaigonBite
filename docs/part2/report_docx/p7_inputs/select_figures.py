from pathlib import Path
import csv,json,re,hashlib
from PIL import Image
base=Path(r'D:\RAD\FINAL'); repo=base/'SaigonBite'; notes=base/'Part2/notes/P7'; draft=repo/'docs/part2/latex/figure_candidates_DRAFT.csv'
candidates=list(csv.DictReader(draft.open(encoding='utf-8-sig',newline=''))); rec={r['sha256']:r['visual_record'] for r in csv.DictReader((notes/'candidate_visual_reconciliation.csv').open(encoding='utf-8-sig',newline=''))}
fonts={r['source_png'].replace('\\','/'):float(r['estimated_min_pt']) for r in csv.DictReader((repo/'docs/part2/latex/figure_font_candidates.csv').open(encoding='utf-8-sig',newline=''))}
rows=[]; seen=set(); appendix={'Appendix 1':[],'Appendix 3':[]}; first={'use_case_diagram':'Appendix 1','domain_model':'Appendix 3','dcd_subsystem':'Appendix 3'}
def add(fig,section,path,source,caption,author,ai,location,note='',ref=''):
 path=path.replace('\\','/'); p=repo/path
 if not p.exists():raise FileNotFoundError(path)
 with Image.open(p) as im: im.verify()
 with Image.open(p) as im:w,h=im.size
 digest=hashlib.sha256(p.read_bytes()).hexdigest(); draw=p.with_suffix('.drawio');width=230 if path.startswith('models/') else min(170,round(220*w/h,1)); orientation='landscape' if path.startswith('models/') else 'portrait'
 f=fonts.get(path);estimate=round(f*width/230,3) if f is not None else None
 rows.append(dict(record_type='figure',fig_id=fig,section=section,source_png=path,drawio_source=str(draw.relative_to(repo)).replace('\\','/') if draw.exists() else '',author=author,ai_label=ai,width_mm=width,page_orientation=orientation,body_or_appendix=location,note=note,caption=caption,pixel_size=f'{w}x{h}',sha256=digest,prior_visual_record=rec.get(digest,'NOT YET RECONCILED'),estimated_min_pt=estimate if estimate is not None else 'NOT MEASURED',readability='PASS estimate' if estimate is not None and estimate>=9 else 'REVIEW REQUIRED',source_section=source,reference=ref))
 seen.add(path)
for x in candidates:
 path=x['png'].replace('\\','/'); name=Path(path).name; sec=x['section_source']; team=None
 for stem,app in first.items():
  if re.fullmatch(re.escape(stem)+r'_Part[A-Z]+\.png',name):team=(stem,app);break
 if team:
  stem,app=team
  # All parts of a team-wide diagram are printed in the appendix; Part A is also a body overview.
  appendix[app].append((x,path,stem))
  if not name.endswith('_PartA.png'):continue
  n='body overview + appendix full size';caption=x['caption']+f' Full size: {app}; see the corresponding figure series.'
 else:n='';caption=x['caption']
 fig='P7-'+str(len(rows)+1).zfill(4);add(fig,sec,path,sec,caption,x['author'],x['ai_label'],'body',n)
for app,items in appendix.items():
 for i,(x,path,stem) in enumerate(items,1):
  fig=('A1.' if app=='Appendix 1' else 'A3.')+str(i);n='body overview + appendix full size' if path.endswith('_PartA.png') else ''
  cap=f'{fig}. {x["alt"]} — Author: {x["author"]} · AI-assisted ({x["ai_label"]}).'
  add(fig,app,path,x['section_source'],cap,x['author'],x['ai_label'],'appendix',n)
# The new integration and demonstration draft sections were created after the candidate inventory.
for sec in ['IV_4-3-6_integration.md','V_5-3_demonstration.md']:
 t=(repo/'docs/part2/report'/sec).read_text(encoding='utf-8')
 for m in re.finditer(r'!\[([^]]+)\]\(([^)]+\.png)\)\s*\n\s*(Figure [^\n]+)',t):
  p=((repo/'docs/part2/report')/m.group(2)).resolve().relative_to(repo);path=p.as_posix()
  if path in seen:raise ValueError('duplicate screenshot '+path)
  cap=m.group(3); ai='Claude Sonnet 5.5' if 'Claude' in cap else 'Codex';add('P7-'+str(len(rows)+1).zfill(4),sec,path,sec,cap,'722I0004',ai,'body')
# Record the eight first-page aliases as metadata, never a placed figure.
conf=json.loads((notes/'panorama_conflict.json').read_text(encoding='utf-8'))
for item in conf['evidence']:
 rows.append(dict(record_type='alias',fig_id='',section='',source_png=item['base'],drawio_source='',author='',ai_label='',width_mm='',page_orientation='',body_or_appendix='not placed',note='alias of '+item['part_a'],caption='',pixel_size='',sha256=item['base_sha256'],prior_visual_record='',estimated_min_pt='',readability='',source_section='',reference=''))
fields=['record_type','fig_id','section','source_png','drawio_source','author','ai_label','width_mm','page_orientation','body_or_appendix','note','caption','pixel_size','sha256','prior_visual_record','estimated_min_pt','readability','source_section','reference']
out=repo/'docs/part2/latex/figure_manifest.csv'
with out.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
print('placed',sum(r['record_type']=='figure' for r in rows),'unique PNGs',len(seen),'aliases',sum(r['record_type']=='alias' for r in rows));print('without matched visual record',sum(r['record_type']=='figure' and r['prior_visual_record']=='NOT YET RECONCILED' for r in rows));print('without estimated font or below 9pt',sum(r['recordability']!='PASS estimate' for r in []))
print('appendices', {k:len(v) for k,v in appendix.items()})
