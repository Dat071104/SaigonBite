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
 table_depth=0
 for n,line in enumerate(t.splitlines(),1):
  if re.search(r'\\begin\{(?:longtable|tabular|tabularx)\}',line):table_depth+=1
  if not table_depth and re.search(r'(?<!\\)&',line):raw.append((p.name,n,'&'))
  if re.search(r'\\end\{(?:longtable|tabular|tabularx)\}',line):table_depth-=1
  if line.lstrip().startswith('%'):continue
  for char in '_%#':
   if re.search(r'(?<!\\)'+re.escape(char),line):raw.append((p.name,n,char));break
check('raw special characters',not raw,f'issues={raw[:12]} total={len(raw)}')
def mask_code(t):
 t=re.sub(r'\\begin\{(lstlisting|verbatim)\}.*?\\end\{\1\}',lambda m:' '*len(m.group()),t,flags=re.S)
 for m in reversed(list(re.finditer(r'\\(?:texttt|code)\{',t))):
  i=m.end();depth=1
  while i<len(t) and depth:
   if t[i]=='{' and (i==0 or t[i-1]!='\\'):depth+=1
   elif t[i]=='}' and (i==0 or t[i-1]!='\\'):depth-=1
   i+=1
  t=t[:m.start()]+' '*(i-m.start())+t[i:]
 return t
markers=[]
for p,t in texts.items():
 if p.name=='links.tex':continue
 for pattern in [r'⟦',r'\bTODO\b',r'\[VERIFY\]']:
  if re.search(pattern,t):markers.append((p.name,pattern,len(re.findall(pattern,t))))
 t=mask_code(t)
 for m in re.finditer('PENDING',t):
  before=t[:m.start()];after=t[m.end():]
  if before.endswith(('\\_', '_','.')) or after.startswith(('\\_', '_')):continue
  markers.append((p.name,'bare PENDING',t.count('\n',0,m.start())+1))
check('forbidden placeholder strings',not markers,f'matches={markers[:12]} total={len(markers)}; application state code excluded by owner decision')
manifest=list(csv.DictReader((root/'figure_manifest.csv').open(encoding='utf-8-sig',newline='')));placed=[x for x in manifest if x['record_type']=='figure'];expected={x['fig_id'] for x in placed};actual={x for x in labels if x.startswith(('P7-','A1.','A3.'))};missing=sorted(expected-actual);extra=sorted(actual-expected);counts=collections.Counter(x['source_png'] for x in placed);wrong=[(p,n) for p,n in counts.items() if n>1 and not (n==2 and all(x['note'].startswith('body overview + appendix full size') for x in placed if x['source_png']==p))];check('manifest figures referenced',not missing and not extra and not wrong and len(figs)==len(placed),f'expected={len(placed)} emitted={len(figs)} missing={missing[:6]} extra={extra[:6]} unauthorized duplicates={wrong[:6]}')
plan=json.loads((base/'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8'));template=plan['template_styled_headings'];receipt=json.loads((base/'Part2/notes/P7/latex_draft_receipt.json').read_text(encoding='utf-8'))
# Reconstruct only the formatting functions, then compare actual generated heading text and order.
import ast
source=(base/'Part2/build/p7_latex/build_sections.py').read_text(encoding='utf-8');tree=ast.parse(source);keep=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('unicode_map','esc') for t in n.targets):keep.append(n)
 if isinstance(n,ast.FunctionDef) and n.name in ('safe','formatted'):keep.append(n)
ns={'re':re,'unknown':[]};exec(compile(ast.Module(body=keep,type_ignores=[]),'formatting','exec'),ns)
style_map={x['text']:x['style'] for x in template};template_order=[x['text'] for x in template][2:];actual_rows=[(i,r) for i,r in enumerate(plan['sections'],1) if r['heading'] in style_map];actual_order=[r['heading'] for i,r in actual_rows];heading_errors=[]
for i,row in actual_rows:
 heading=row['heading']
 if '[Name]' in heading or '[Actor ' in heading:
  number=re.match(r'^[0-9]+(?:\.[0-9]+)+',heading).group();lines=(repo/row['source file']).read_text(encoding='utf-8-sig').splitlines();hits=[re.sub(r'^#+\s*','',x).strip() for x in lines if re.match(r'^#+\s+'+re.escape(number)+r'(?:\s|$)',x)]
  if len(hits)!=1:heading_errors.append((i,'source heading',hits));continue
  heading=hits[0]
 level={'Heading 1':'section','Heading 2':'subsection','Heading 3':'subsubsection'}.get(style_map[row['heading']],'paragraph')
 expected='\\'+level+'*{'+ns['formatted'](heading)+'}'
 first=(root/'sections'/f'section_{i:03}.tex').read_text(encoding='utf-8').splitlines()[0]
 if first!=expected:heading_errors.append((i,expected,first))
 if 'Use Case ' in heading and ('author:' in heading.lower()) and not re.search(r'\b[0-9]{3}[A-Z][0-9]{4}\b',heading):heading_errors.append((i,'missing author',heading))
main=(root/'main.tex').read_text(encoding='utf-8');inputs=re.findall(r'\\input\{sections/section_(\d+)\}',main);wanted=[f'{i:03}' for i in range(1,len(plan['sections'])+1)]
check('template heading order and text',actual_order==template_order and not heading_errors and inputs==wanted,f'{len(template)} template headings including IP and TOC; section input order checked; errors={heading_errors[:4]}; order_match={actual_order==template_order}; inputs_order={inputs==wanted}')
missing_author=[x['fig_id'] for x in placed if not x['author'] or x['author'] not in x['caption'] or not x['ai_label']];check('figure author and AI labels',not missing_author,f'violations={missing_author[:12]} total={len(missing_author)}')
models=[x for x in placed if x['source_png'].startswith('models/') and x['readability']=='ESTIMATE BELOW 9pt']
screens=[x for x in placed if x['source_png'].startswith('docs/') and x['readability']=='ESTIMATE BELOW 9pt']
issue_text=(base/'Part2/notes/P7/diagram_issues.md').read_text(encoding='utf-8')
bad=[x['fig_id'] for x in models if '(editable source: '+x['drawio_source']+')' not in x['caption'] or x['fig_id'] not in issue_text or not (repo/x['drawio_source']).is_file()]
check('figure readability exceptions',len(models)==12 and not bad,f'PASS (exceptions listed): {len(models)} model placements; {len(screens)} screenshot estimates exempt; invalid={bad}; final layout not rendered')
result=['P7 B7 static checks -- no compilation or PDF','']+[f'{status} | {name} | {detail}' for name,status,detail in checks];result+=['','OVERALL: '+('PASS' if all(x[1]=='PASS' for x in checks) else 'FAIL')];report.write_text('\n'.join(result)+'\n',encoding='utf-8');print('\n'.join(result))

