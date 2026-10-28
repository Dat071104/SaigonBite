from pathlib import Path
import csv,re,json,collections,hashlib
root=Path(r'D:\RAD\FINAL\SaigonBite');notes=Path(r'D:\RAD\FINAL\Part2\notes\P7');src=root/'docs/part2'; out=src/'report_docx/p7_inputs/status_refresh';out.mkdir(parents=True,exist_ok=True)
r=list(csv.DictReader((src/'implementation/p4_design_resolution.csv').open(encoding='utf-8-sig',newline=''))); by=collections.defaultdict(list)
for x in r:by[x['element']].append(x)
log=[]
def summarise(rows):
 ids=sorted({int(x['source_row']) for x in rows}); phases=sorted({x['P4 subphase'] for x in rows});pol=all('EXPLICIT_POLICY' in x['disposition'] for x in rows)
 if any(not x['test_nodes'].strip() for x in rows):return 'Not evidenced; see P4 resolution rows '+', '.join(map(str,ids))
 return ('Static dependency-policy checks' if pol else 'P4 scoped evidence')+' ('+', '.join(phases)+'; resolution rows '+', '.join(map(str,ids))+')'
for p in sorted(src.glob('UC-*/design_classes.md')):
 t=p.read_text(encoding='utf-8');category='';output=[]
 for n,line in enumerate(t.splitlines(),1):
  if line.startswith('## '):category=line[3:].strip()
  if line.startswith('Static source: C0 '):
   line='The class tables record the C0 design and the later P4 resolution. P4 status and scoped evidence are listed in the P4 status appendix; unchanged static correspondences remain marked MATCH.'
  elif line.startswith('|') and ('P4-TARGET' in line or re.search(r'\bGAP\b',line)):
   parts=line.split('|');m=re.search(r'`[+\-]?\s*([\w.]+)',parts[2] if len(parts)>2 else '')
   match=by.get(category+'.'+m.group(1),[]) if m else [z for z in r if z['element'].startswith(category+'.')]
   if m and not match:raise ValueError(f'Unmapped {p}:{n}: {category}.{m.group(1)}')
   if not match:raise ValueError(f'Unmapped class {p}:{n}: {category}')
   line=line.replace('†','')
   if m:
    parts=line.split('|');parts[3]=' '+summarise(match)+'; '+re.sub(r'^\s*(?:P4-TARGET|GAP)\s*[—-]?\s*','',parts[3].strip())+' ';line='|'.join(parts)
   else:line=re.sub(r'(?:P4-TARGET|GAP)(?:\s*\(Static\))?',summarise(match),line)
   log.append({'file':str(p.relative_to(root)),'line':n,'resolution_rows':','.join(x['source_row'] for x in match),'kind':'design member' if m else 'class summary'})
  if "P4-TARGET" in line or re.search(r"\bGAP\b",line):
   line=line.replace("P4-TARGET", "C0 design target (final status in Table P4-1)")
   line=re.sub(r"\bGAP\b", "C0 design gap (final status in Table P4-1)",line)
  if "†" in line: line=line.replace("†", "")
  output.append(line)
 dest=out/(p.parent.name+'_design_classes.md');dest.write_text('\n'.join(output)+'\n',encoding='utf-8')
for p in sorted(src.glob('UC-*/crc.md')):
 output=[]
 for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  if line.startswith('Collaborators below resolve'):
   line='Collaborators reflect the design responsibilities. Final P4 status and its scoped evidence are recorded in the P4 status appendix. DAO collaborators also appear in the DCD; persistence sequences are in 4.3.2.'
  elif '†' in line: line=line.replace('†','')
  output.append(line)
 (out/(p.parent.name+'_crc.md')).write_text('\n'.join(output)+'\n',encoding='utf-8')
print('Wrote 12 derived include copies; matched',len(log),'design/member lines to register')
with (notes/'status_include_mapping.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['file','line','resolution_rows','kind']);w.writeheader();w.writerows(log)
