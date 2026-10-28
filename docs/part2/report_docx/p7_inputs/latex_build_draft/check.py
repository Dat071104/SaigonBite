from pathlib import Path
import json,csv,re,collections
base=Path(r'D:\RAD\FINAL');repo=base/'SaigonBite';root=repo/'docs/part2/latex';files=sorted(root.rglob('*.tex'));report=repo/'docs/part2/test_report/p7_2026-10-28/static_checks.txt';checks=[]
def check(name,ok,detail):checks.append((name,'PASS' if ok else 'FAIL',detail))
texts={p:p.read_text(encoding='utf-8-sig') for p in files};unlist=lambda t:re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}','',t,flags=re.S);alltext='\n'.join(texts.values());inputs=[];missing_inputs=[]
for p,t in texts.items():
 for ref in re.findall(r'\\(?:input|include)\{([^}]+)\}',unlist(t)):
  q=root/(ref if ref.endswith('.tex') else ref+'.tex');inputs.append((p.name,ref))
  if not q.exists():missing_inputs.append((p.name,ref))
check('inputs exist',not missing_inputs,f'{len(inputs)} checked; missing={missing_inputs[:10]}')
figs=[];missing_img=[]
for p,t in texts.items():
 for x in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{\\detokenize\{([^}]+)\}\}',unlist(t)):
  figs.append(x)
  if not (repo/x).is_file():missing_img.append((p.name,x))
check('graphic files exist',not missing_img,f'{len(figs)} occurrences; missing={missing_img[:10]}')
labels=collections.Counter(re.findall(r'\\label\{([^}]+)\}',alltext));refs=collections.Counter(re.findall(r'\\(?:ref|pageref)\{([^}]+)\}',alltext));dup=[x for x,n in labels.items() if n>1];missing_ref=[x for x in refs if x not in labels];check('labels and references',not dup and not missing_ref,f'{len(labels)} labels, {len(refs)} referenced; duplicate={dup[:8]}; unresolved={missing_ref[:8]}')
issues=[]
for p,t in texts.items():
 t=unlist(t);stack=[]
 for kind,name in re.findall(r'\\(begin|end)\{([^}]+)\}',t):
  if kind=='begin':stack.append(name)
  elif not stack or stack.pop()!=name:issues.append((p.name,'environment mismatch',name));break
 if stack:issues.append((p.name,'unclosed environment',stack[-1]))
 # Count braces except escaped literal symbols; TeX comments are removed, except links.tex uses a local percent catcode.
 if p.name!='links.tex':
  t='\n'.join(re.split(r'(?<!\\)%',line,1)[0] for line in t.splitlines());depth=0
  for k,c in enumerate(t):
   if c not in '{}':continue
   n=0;j=k-1
   while j>=0 and t[j]=='\\':n+=1;j-=1
   if n%2:continue
   depth+=1 if c=='{' else -1
   if depth<0:issues.append((p.name,'extra closing brace',k));break
  if depth!=0:issues.append((p.name,'brace balance',depth))
check('environment and brace balance',not issues,f'issues={issues[:12]} total={len(issues)}')
# Raw special-character audit ignores listings, generated hyperlinks/paths and table alignment delimiters.
raw=[]
for p,t in texts.items():
 if p.name=='links.tex':continue
 t=unlist(t);t=re.sub(r'\\detokenize\{[^}]*\}','',t);t=re.sub(r'\\(?:input|label|ref|pageref)\{[^}]*\}','',t)
 for n,line in enumerate(t.splitlines(),1):
  if line.lstrip().startswith('%'):continue
  for char in '_%#':
   if re.search(r'(?<!\\)'+re.escape(char),line):raw.append((p.name,n,char));break
check('raw special characters',not raw,f'issues={raw[:12]} total={len(raw)}')
markers=[]
for p,t in texts.items():
 if p.name=='links.tex':continue
 for pattern in [r'⟦',r'\bTODO\b',r'\[VERIFY\]',r'PENDING']:
  if re.search(pattern,t):markers.append((p.name,pattern,len(re.findall(pattern,t))))
check('forbidden placeholder strings',not markers,f'matches={markers[:12]} files={len(markers)}; note: PENDING also names legitimate payment states and appears byte-exact in required method excerpts')
manifest=list(csv.DictReader((root/'figure_manifest.csv').open(encoding='utf-8-sig',newline='')));placed=[x for x in manifest if x['record_type']=='figure'];expected={x['fig_id'] for x in placed};actual={x for x in labels if x.startswith(('P7-','A1.','A3.'))};missing=sorted(expected-actual);extra=sorted(actual-expected);counts=collections.Counter(x['source_png'] for x in placed);wrong=[(p,n) for p,n in counts.items() if n>1 and not (n==2 and all(x['note'].startswith('body overview + appendix full size') for x in placed if x['source_png']==p))];check('manifest figures referenced',not missing and not extra and not wrong and len(figs)==len(placed),f'expected={len(placed)} emitted={len(figs)} missing={missing[:6]} extra={extra[:6]} unauthorized duplicates={wrong[:6]}')
plan=json.loads((base/'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8'));template=plan['template_styled_headings'];receipt=json.loads((base/'Part2/notes/P7/latex_draft_receipt.json').read_text(encoding='utf-8'));headings={x['heading'] for x in receipt['sections']};unmapped=[x['text'] for x in template if x['text'] not in headings and x['text'] not in ['Intellectual Property','Table of Contents']];check('template heading coverage',not unmapped and len(template)==87,f'{len(template)} template headings mapped; unmapped={unmapped}; exact rendered order and filled UC titles require independent comparison')
missing_author=[x['fig_id'] for x in placed if not x['author'] or x['author'] not in x['caption'] or not x['ai_label']];check('figure author and AI labels',not missing_author,f'violations={missing_author[:12]} total={len(missing_author)}')
check('figure readability estimates',not any(x['readability']=='ESTIMATE BELOW 9pt' for x in placed),f'{sum(x["readability"]=="ESTIMATE BELOW 9pt" for x in placed)} placements below 9pt estimate; see diagram issues; actual layout unverified')
result=['P7 B7 static checks -- no compilation or PDF','']+[f'{status} | {name} | {detail}' for name,status,detail in checks];result+=['','OVERALL: '+('PASS' if all(x[1]=='PASS' for x in checks) else 'FAIL')];report.write_text('\n'.join(result)+'\n',encoding='utf-8');print('\n'.join(result))
