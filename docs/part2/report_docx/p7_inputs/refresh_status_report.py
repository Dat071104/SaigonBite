from pathlib import Path
import csv,re,collections,json,subprocess
base=Path(r'D:\RAD\FINAL');root=base/'SaigonBite';reports=root/'docs/part2/report';r=list(csv.DictReader((root/'docs/part2/implementation/p4_design_resolution.csv').open(encoding='utf-8-sig',newline='')));byop=collections.defaultdict(list);byel=collections.defaultdict(list)
for x in r:byop[x['op_id']].append(x);byel[x['element']].append(x)
files=sorted(reports.glob('III_3-*_UC-*.md'))+[reports/x for x in ['IV_4-1_subsystem_dcd.md','IV_4-2_package.md','IV_4-3-1_mapping.md','IV_4-3-2_dao_sequences.md']];audit=[]
for p in files:
 rel=p.relative_to(root).as_posix();t=subprocess.check_output(['git','show','HEAD:'+rel],cwd=root).decode('utf-8'); before=t; out=[]
 for line in t.splitlines():
  inc=re.search(r'<!-- include: ../(UC-\d+)/(design_classes|crc)\.md -->',line)
  if inc:line=f'<!-- include: ../report_docx/p7_inputs/status_refresh/{inc.group(1)}_{inc.group(2)}.md -->'
  if line.startswith('**Status.**'):
   line='**Status.** The diagram retains its historical design notation at C0. Table P4-1 and its detailed appendix record each element’s later P4 disposition, evidence and limitations.'
  elif line.startswith('The baseline is committed application `C0'):
   line='The design baseline was C0 `45ac76221b0a103174c7c01d17577e6e49cfd665`. A dagger in a diagram marks a target at that baseline; Table P4-1 records its final status and scoped evidence.'
  if 'P4-TARGET' in line or re.search(r'\bGAP\b',line):
   matches=[]
   for op in re.findall(r'\bOP-\d+\b',line):matches+=byop.get(op,[])
   for element,rr in byel.items():
    if element and element in line:matches+=rr
   ids=sorted({int(x['source_row']) for x in matches})
   status=('P4 resolution rows '+', '.join(map(str,ids))+' (scoped evidence in Table P4-1)' if ids else 'historical C0 design target; final status in Table P4-1')
   line=line.replace('P4-TARGET†',status).replace('P4-TARGET',status)
   line=re.sub(r'\bGAP\b',status,line)
   audit.append({'file':p.name,'resolution_rows':ids,'line_status':'mapped' if ids else 'reference_only'})
  if '†' in line and line.startswith('|'):
   line=line.replace('†','')
  if line.lstrip().startswith('Figure ') and p.name.startswith(('III_','IV_')):
   line+=' † = target at design commit C0; final status in Table P4-1.'
  out.append(line)
 result='\n'.join(out)+'\n'
 # Every pre-existing operation, UC/postcondition, requirement and source-file identifier must survive.
 pat=r'\b(?:OP-\d+|(?:S?UC\d{2}-(?:PC|MG)\d+)|P[234]-S\d+|F-\d+|BR-\d+)\b'
 old=collections.Counter(re.findall(pat,before));new=collections.Counter(re.findall(pat,result));missing=old-new
 if missing:raise ValueError(f'{p.name} lost identifiers: {missing}')
 p.write_text(result,encoding='utf-8')
print('refreshed files',len(files),'marked lines',len(audit),'matched',sum(x['line_status']=='mapped' for x in audit),'appendix references',sum(x['line_status']=='reference_only' for x in audit))
(base/'Part2/notes/P7/status_report_mapping.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
