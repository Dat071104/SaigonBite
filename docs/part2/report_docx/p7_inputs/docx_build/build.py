from pathlib import Path
import sys, json, csv, re, hashlib, shutil, copy
sys.path.insert(0,r'C:\Users\ADMIN\AppData\Roaming\Python\Python313\site-packages')
from markdown_it import MarkdownIt
from docx import Document
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.shared import Mm, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_BREAK
from urllib.parse import unquote
B=Path(r'D:\RAD\FINAL'); R=B/'SaigonBite'; L=R/'docs/part2/latex'; OUT=B/'Part2/deliverables/Team02_BRS_SRS_for_SaigonBite.docx'; OUT.parent.mkdir(parents=True,exist_ok=True)
T=B/'RAD_Sem01_2627_Report_Template.docx'; P=json.loads((B/'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8')); rows=P['sections']; M=list(csv.DictReader((L/'figure_manifest.csv').open(encoding='utf-8-sig',newline=''))); figs=[x for x in M if x['record_type']=='figure']; links=json.loads((B/'Part2/content/links.json').read_text(encoding='utf-8')); md=MarkdownIt('commonmark').enable('table')
d=Document(T); body=d.element.body
# Retain the template's front matter, existing styles and IP page; remove its instruction page and sample body.
children=list(body); title=next(x for x in children if ''.join(x.itertext()).find('[TITLE OF YOUR PROJECT]')>=0); executive=next(x for x in children if 'Executive Summary (0.25 point)' in ''.join(x.itertext()))
for x in children:
 if children.index(x)<children.index(title) or (children.index(x)>=children.index(executive) and x.tag!=qn('w:sectPr')):body.remove(x)
for p in d.paragraphs:
 for old,new in [('[TITLE OF YOUR PROJECT]','SaigonBite: Online Food Delivery Hub Platform'),('1. [StudentID1] : [Student Name 1]','722I0004 : Nguyen Thanh Dat'),('2. [StudentID2] : [Student Name 2]','523K0049 : Le Minh Quan'),('3. [StudentID3] : [Student Name 3]   (delete if your team has 2 students)','523K0050 : Nguyen Minh Quan'),('Copyright [year] Team XX.','Copyright 2026 Team 02.'),('Team XX','Team 02')]:
  if old in p.text:p.text=p.text.replace(old,new)
for table in d.tables:
 for row in table.rows:
  for cell in row.cells:
   for para in cell.paragraphs:
    v=para.text
    replacements={'[Title of your project]':'SaigonBite','[Project title]':'SaigonBite','[Your project title]':'SaigonBite','TeamXX_BRS_SRS_for_[CaseName]':'Team02_BRS_SRS_for_SaigonBite','[This document provides an in-depth analysis and design of the proposed system, with the requirement':'[This document provides an in-depth analysis and design of the proposed system, with the requirement','[Name of lecturer]':'Mr. Pham Thai Ky Trung','[date]':'28/10/2026'}
    for a,b in replacements.items():v=v.replace(a,b)
    if v!=para.text:para.text=v
for table in d.tables:
 if len(table.rows)>=2 and table.cell(0,0).text.strip()=='Abstract':
  table.cell(1,0).text='SaigonBite connects customer ordering, kitchen decisions, delivery and operational reporting. This report records the requirements, design, implementation and evidence for the Part 2 demonstration. The online payment option is simulated and refund obligations are recorded without a payout. Recorded test and deployment results are scoped to the documented runs.'
settings=d.settings.element
for tag in ['updateFields','doNotAutoCompressPictures']:
 e=settings.find(qn('w:'+tag))
 if e is None:e=OxmlElement('w:'+tag);settings.append(e)
 if tag=='updateFields':e.set(qn('w:val'),'true')
# Add a real TOC field after the retained template heading.
toc=next(p for p in d.paragraphs if p.text.strip()=='Table of Contents');p=d.add_paragraph();toc._p.addnext(p._p);r=p.add_run();e=OxmlElement('w:fldSimple');e.set(qn('w:instr'),r'TOC \o "1-3" \h \z \u');r._r.addnext(e)
styles={x['text']:x['style'] for x in P['template_styled_headings']};used=[];bookmark_id=10;missing=[]
def mark(p,name):
 global bookmark_id
 # Word bookmark identifiers cannot contain punctuation.
 name='B'+re.sub('[^A-Za-z0-9_]','_',name)
 a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(bookmark_id));a.set(qn('w:name'),name);p._p.append(a)
 z=OxmlElement('w:bookmarkEnd');z.set(qn('w:id'),str(bookmark_id));p._p.append(z);bookmark_id+=1

linkkeys={'LinkRepo':'github_repo','LinkRelease':'github_release_url','LinkFigma':'figma_prototype','LinkFigmaFile':'figma_file','LinkDeployed':'deployed_url','LinkDeployedFallback':'deployed_url_fallback','LinkVideo':'demo_video','LinkDrive':'drive_folder'}
def linkvalue(key):
 return links.get(linkkeys.get(key,''))
def add_link(p,url,label):
 from docx.opc.constants import RELATIONSHIP_TYPE as RT
 rid=p.part.relate_to(url,RT.HYPERLINK,is_external=True);a=OxmlElement('w:hyperlink');a.set(qn('r:id'),rid);r=OxmlElement('w:r');pr=OxmlElement('w:rPr');style=OxmlElement('w:rStyle');style.set(qn('w:val'),'Hyperlink');pr.append(style);r.append(pr);t=OxmlElement('w:t');t.text=label;r.append(t);a.append(r);p._p.append(a)
def text_into(p,s,code=False):
 for part in re.split(r'(\{\{(?:Link[A-Za-z]+|PAGEREF:[^}]+)\}\})',s):
  m=re.fullmatch(r'\{\{(Link[A-Za-z]+|PAGEREF:([^}]+))\}\}',part)
  if m and m.group(2):
   fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),' PAGEREF B'+re.sub('[^A-Za-z0-9_]','_',m.group(2))+' \\h ');p._p.append(fld)
  elif m:
   v=linkvalue(m.group(1))
   if v and not v.startswith('PENDING'):add_link(p,v,v)
   else:
    run=p.add_run('PENDING: '+linkkeys.get(m.group(1),m.group(1)));run.bold=True;run.font.color.rgb=__import__('docx').shared.RGBColor(255,0,0)
  else:
   part=part.replace('OWNER-PENDING','owner action outstanding')
   for piece in re.split(r'(⟦|⟧|(?<![A-Za-z0-9_.])PENDING(?![A-Za-z0-9_]))',part):
    if piece in ('⟦','⟧'):
     run=p.add_run();sym=OxmlElement('w:sym');sym.set(qn('w:font'),'Cambria Math');sym.set(qn('w:char'),'27E6' if piece=='⟦' else '27E7');run._r.append(sym)
    else:
     run=p.add_run(piece)
     if code or piece=='PENDING':run.font.name='Consolas'

def inlines(p,t):
 children=t.children or [];i=0
 while i<len(children):
  c=children[i]
  if c.type=='link_open':
   target=unquote(c.attrGet('href') or '');j=i+1;pieces=[]
   while j<len(children) and children[j].type!='link_close':
    if children[j].type in ('text','code_inline'):pieces.append(children[j].content)
    j+=1
   match=re.match(r'^\{\{(Link[A-Za-z]+)\}\}(.*)$',target)
   if match:
    v=linkvalue(match.group(1));target=(v+match.group(2)) if v and not v.startswith('PENDING') else ''
   if target.startswith(('http://','https://')):add_link(p,target,''.join(pieces))
   else:text_into(p,''.join(pieces))
   i=j+1;continue
  if c.type in ('text','code_inline'):text_into(p,c.content,c.type=='code_inline')
  elif c.type in ('softbreak','hardbreak'):p.add_run().add_break()
  elif c.type=='html_inline' and re.fullmatch(r'<br\s*/?>',c.content,re.I):p.add_run().add_break()
  i+=1

def image(item):
 used.append(item['fig_id']);land=item['page_orientation']=='landscape'
 if land:
  sec=d.add_section(WD_SECTION.NEW_PAGE);sec.orientation=WD_ORIENT.LANDSCAPE;sec.page_width=Mm(297);sec.page_height=Mm(210);sec.left_margin=Mm(30);sec.right_margin=Mm(30);sec.top_margin=Mm(15);sec.bottom_margin=Mm(15)
 p=d.add_paragraph();p.paragraph_format.keep_with_next=True;mark(p,item['fig_id']);p.add_run().add_picture(str(R/item['source_png']),width=Mm(float(item['width_mm'])))
 c=d.add_paragraph(item['caption'])
 if land:
  sec=d.add_section(WD_SECTION.NEW_PAGE);sec.orientation=WD_ORIENT.PORTRAIT;sec.page_width=Mm(210);sec.page_height=Mm(297);sec.left_margin=Mm(20);sec.right_margin=Mm(20);sec.top_margin=Mm(20);sec.bottom_margin=Mm(20)

def incl(t,src,seen=None):
 seen=set() if seen is None else seen
 def sub(m):
  p=(src.parent/m.group(1)).resolve()
  if p in seen:raise ValueError('recursive include '+str(p))
  return '\n'+incl(p.read_text(encoding='utf-8-sig'),p,seen|{p})+'\n'
 return re.sub(r'<!--\s*include:\s*([^>]+?)\s*-->',sub,t)

def find(dest,src,row):
 path=(src.parent/unquote(dest)).resolve().relative_to(R.resolve()).as_posix();loc='appendix' if row['heading'].startswith('Appendix ') else 'body';opts=[x for x in figs if x['source_png']==path and x['body_or_appendix']==loc]
 if loc=='appendix':opts=[x for x in opts if x['section']==row['heading'].split(':')[0]]
 else:opts=[x for x in opts if x['source_section']==src.name or x['source_section']=='II_state_machines.md']
 return opts[0] if len(opts)==1 else None

def emit(text,src,row):
 toks=md.parse(text);i=0;skip=False
 while i<len(toks):
  t=toks[i]
  if t.type in ('heading_open','paragraph_open') and i+2<len(toks) and toks[i+1].type=='inline':
   z=toks[i+1];ims=[x for x in (z.children or []) if x.type=='image']
   if ims:
    for im in ims:
     found=find(im.attrGet('src'),src,row)
     if found:image(found)
    skip=True
   elif skip and re.match(r'^\s*(?:\*\*)?(?:Figure\s|A[13]\.\d+\.)',z.content):skip=False
   else:
    skip=False;p=d.add_paragraph();inlines(p,z)
    if t.type=='heading_open':
     for run in p.runs:run.bold=True
   i+=3;continue
  if t.type in ('fence','code_block'):
   p=d.add_paragraph();content=t.content.replace('{{LinkRepo}}',links['github_repo']);run=p.add_run(content);run.font.name='Consolas';run.font.size=Pt(8);i+=1;continue
  if t.type=='table_open':
   j=i+1;records=[];cur=None;cell=None
   while j<len(toks) and toks[j].type!='table_close':
    q=toks[j]
    if q.type=='tr_open':cur=[]
    elif q.type in ('th_open','td_open'):cell=[]
    elif q.type=='inline' and cell is not None:cell.append(q)
    elif q.type in ('th_close','td_close'):cur.append(cell);cell=None
    elif q.type=='tr_close':records.append(cur)
    j+=1
   n=max(map(len,records),default=1);table=d.add_table(rows=len(records),cols=n)
   if records:
    pr=table.rows[0]._tr.get_or_add_trPr();h=OxmlElement('w:tblHeader');h.set(qn('w:val'),'true');pr.append(h)
   table_rows=table.rows
   for ri,record in enumerate(records):
    cells=table_rows[ri].cells
    for ci,content in enumerate(record):
     p=cells[ci].paragraphs[0]
     for v in content:inlines(p,v)
     if n>6:
      for rr in p._p.xpath('.//w:r'):
       prop=rr.get_or_add_rPr()
       for tag in ('w:sz','w:szCs'):
        e=prop.find(qn(tag))
        if e is None:e=OxmlElement(tag);prop.append(e)
        e.set(qn('w:val'),'16')
   i=j+1;continue
  i+=1
state=R/'docs/part2/report/II_state_machines.md'; st=state.read_text(encoding='utf-8');blocks={m.group(1):m.group(2) for m in re.finditer(r'<!-- BEGIN STATE_MACHINE ([A-Z_]+) -->(.*?)<!-- END STATE_MACHINE \1 -->',st,re.S)}
for idx,row in enumerate(rows,1):
 heading=row['heading'];src=R/row['source file'] if row['source file'].startswith('docs/') else None
 if src and ('[Name]' in heading or '[Actor ' in heading):
  number=re.match(r'^[0-9]+(?:\.[0-9]+)+',heading).group();matches=[x for x in src.read_text(encoding='utf-8-sig').splitlines() if re.match(r'^#+\s+'+re.escape(number)+r'(?:\s|$)',x)]
  assert len(matches)==1;(heading:=re.sub(r'^#+\s*','',matches[0]).strip())
 p=d.add_paragraph(heading,style=styles.get(row['heading'],'Normal'))
 m=re.match(r'^3\.([1-6])\.3 ',row['heading'])
 if m:mark(p,'CRC-UC-0'+m.group(1))
 if src:
  lines=src.read_text(encoding='utf-8-sig').splitlines();content=[line for a,z in row.get('content_line_ranges',[]) for line in lines[a-1:z]]
  if content and re.match(r'^#+\s',content[0]):content=content[1:]
  emit(incl('\n'.join(content)+'\n',src),src,row)
  for key in P['state_machine_insertions'].get(row['heading'],[]):emit(blocks[key],state,row)
  if row.get('post_content_line_ranges'):
   ps=R/row['post_source_file'];ls=ps.read_text(encoding='utf-8-sig').splitlines();emit(incl('\n'.join(line for a,z in row['post_content_line_ranges'] for line in ls[a-1:z]),ps),ps,row)
 if row['heading']=='Appendix':
  for name in ['Appendix_Glossary.md','Appendix_P4_status.md','Appendix_Evidence_Index.md']:
   p=R/'docs/part2/report'/name;emit(p.read_text(encoding='utf-8-sig'),p,row)
 if idx%20==0:print('sections',idx,'figures',len(used),flush=True)
print('Saving',len(used),'figures',flush=True);d.save(OUT)
(B/'Part2/notes/P7/docx_draft_receipt.json').write_text(json.dumps({'path':str(OUT),'figures':used,'missing':sorted(set(x['fig_id'] for x in figs)-set(used)),'size':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')


