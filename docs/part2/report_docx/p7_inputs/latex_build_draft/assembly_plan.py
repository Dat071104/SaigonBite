from pathlib import Path
from docx import Document
import json,csv,re,collections
b=Path(r'D:\RAD\FINAL');repo=b/'SaigonBite';rows=list(csv.DictReader((b/'Part2/notes/P7/source_map.csv').open(encoding='utf-8-sig',newline='')));doc=Document(b/'RAD_Sem01_2627_Report_Template.docx');styled=[{'style':p.style.name,'text':p.text.strip()} for p in doc.paragraphs if p.style.name.startswith('Heading') and p.text.strip()];lookup={x['heading']:x for x in rows};missing=[x for x in styled if x['text'] not in lookup and x['text'] not in ['Intellectual Property','Table of Contents']];assert not missing,missing
for row in rows:
 row['content_line_ranges']=[]
 if not row['source file'].startswith('docs/'):continue
 m=re.fullmatch(r'(\d+)-(\d+)',row['lines']);assert m,row;start,end=map(int,m.groups());p=repo/row['source file'];lines=p.read_text(encoding='utf-8-sig').splitlines();assert start<=end<=len(lines),row
 # A containing range owns only lines not assigned to any strictly smaller descendant range in the same file.
 claimed=set()
 for other in rows:
  if other is row or other['source file']!=row['source file']:continue
  q=re.fullmatch(r'(\d+)-(\d+)',other['lines'])
  if not q:continue
  a,z=map(int,q.groups())
  if start<=a and z<=end and (a>start or z<end):claimed.update(range(a,z+1))
 indices=[i for i in range(start,end+1) if i not in claimed]
 if indices:
  spans=[];a=last=indices[0]
  for i in indices[1:]:
   if i!=last+1:spans.append([a,last]);a=i
   last=i
  spans.append([a,last]);row['content_line_ranges']=spans
# Append source tails after their last child, so excluded descendants do not reorder later content.
for index,row in enumerate(rows):
 spans=row.get('content_line_ranges',[])
 if len(spans)<2:continue
 parent_start,parent_end=map(int,row['lines'].split('-'));children=[]
 for j,other in enumerate(rows[index+1:],index+1):
  if other['source file']!=row['source file']:continue
  q=re.fullmatch(r'(\d+)-(\d+)',other['lines'])
  if q and parent_start<=int(q.group(1)) and int(q.group(2))<=parent_end:children.append(j)
 if not children:raise ValueError('No destination for parent tail '+row['heading'])
 target=rows[max(children)];target.setdefault('post_content_line_ranges',[]).extend(spans[1:]);target['post_source_file']=row['source file'];row['content_line_ranges']=spans[:1]
# The shared-state model contains separate blocks and must be inserted beneath the matching iv subsection.
states={'2.2.1 iv.':['ORDER','PAYMENT'],'2.2.2 iv.':['DELIVERY'],'2.2.3 iv.':['HUB','USER_ACCOUNT'],'2.2.4 iv.':[],'2.2.5 iv.':['REPLACEMENT_OFFER'],'2.2.6 iv.':['CATALOGUE']};t=(repo/'docs/part2/report/II_state_machines.md').read_text(encoding='utf-8');markers=re.findall(r'<!-- BEGIN STATE_MACHINE ([A-Z_]+) -->',t);print('state-machine source blocks',markers)
print('template styled headings',len(styled),'source entries',len(rows),'unmapped styled',len(missing));plan={'template_styled_headings':styled,'sections':rows,'state_machine_insertions':states,'state_block_names':markers,'front_matter_sources':['links.json','RAD_Sem01_2627_Report_Template.docx'],'notes':['PAGEREF tokens must resolve to exact figure and CRC labels','Use actual UC names and author ID where the template contains placeholders','Only manifest-selected figures are emitted; aliases are metadata','Evidence index and glossary are included as non-heading material','Do not compile or generate PDF during Stage 1']};out=b/'Part2/notes/P7/assembly_plan.json';out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Wrote',out)
