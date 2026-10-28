from pathlib import Path
from markdown_it import MarkdownIt
from docx import Document
import csv,json,re,hashlib
from urllib.parse import unquote
base=Path(r'D:\RAD\FINAL');repo=base/'SaigonBite';latex=repo/'docs/part2/latex';plan=json.loads((base/'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8')); rows=plan['sections']; images=list(csv.DictReader((latex/'figure_manifest.csv').open(encoding='utf-8-sig',newline='')));placed=[x for x in images if x['record_type']=='figure']; md=MarkdownIt('commonmark').enable('table');used=[];unknown=[]
# Text-only UTF-8 is normalized to pdfLaTeX commands; token delimiters remain literal in the Markdown record.
unicode_map={'—':'---','–':'--','·':r'\ensuremath{\cdot}','†':r'\textdagger{}','→':r'\ensuremath{\rightarrow}','↔':r'\ensuremath{\leftrightarrow}','−':r'\ensuremath{-}','×':r'\ensuremath{\times}','≤':r'\ensuremath{\leq}','≥':r'\ensuremath{\geq}','§':r'\S{}','«':r'\guillemotleft{}','»':r'\guillemotright{}','’':"'",'“':'``','”':"''",'…':r'\ldots{}','₫':'VND','⟦':r'\ensuremath{[\![}','⟧':r'\ensuremath{]\!]}'}
esc={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','_':r'\_','%':r'\%','&':r'\&','#':r'\#','$':r'\$','~':r'\textasciitilde{}','^':r'\textasciicircum{}','<':r'\textless{}','>':r'\textgreater{}'}
def safe(s):
 out=[]
 for c in s:
  if c in unicode_map:out.append(unicode_map[c])
  elif c in esc:out.append(esc[c])
  elif ord(c)>127:unknown.append((hex(ord(c)),c));out.append(c)
  else:out.append(c)
 return ''.join(out)
def formatted(s):
 # Resolve late-bound links and appendix page references before text escaping.
 parts=re.split(r'(\{\{(?:Link[A-Za-z]+|PAGEREF:[^}]+)\}\})',s);out=[]
 for part in parts:
  m=re.fullmatch(r'\{\{(Link[A-Za-z]+|PAGEREF:([^}]+))\}\}',part)
  if m:out.append(r'\pageref{'+m.group(2)+'}' if m.group(2) else '\\'+m.group(1))
  else:out.append(safe(part))
 return ''.join(out)
def inline(tok):
 out=[]; children=tok.children or []; link_stack=[]
 for c in children:
  if c.type=='text':out.append(formatted(c.content))
  elif c.type=='code_inline':out.append(r'\texttt{'+formatted(c.content)+'}')
  elif c.type in ['softbreak','hardbreak']:out.append(r'\newline{}')
  elif c.type=='strong_open':out.append(r'\textbf{')
  elif c.type=='em_open':out.append(r'\emph{')
  elif c.type in ['strong_close','em_close']:out.append('}')
  elif c.type=='html_inline':out.append(r'\newline{}' if re.fullmatch(r'<br\s*/?>',c.content,re.I) else safe(c.content))
  elif c.type=='link_open':
   href=unquote(c.attrGet('href') or ''); m=re.match(r'^\{\{Link([A-Za-z]+)\}\}(.*)$',href)
   if m:
    suffix=m.group(2);out.append(r'\href{\Target'+m.group(1)+(r'\detokenize{'+suffix+'}' if suffix else '')+'}{');out.append('')
   else:out.append('')
   link_stack.append(bool(m))
  elif c.type=='link_close':
   if link_stack and link_stack.pop():out.append('}')
  elif c.type=='image':pass
  else:unknown.append(('token',c.type))
 return ''.join(out)
def imgpath(dest,source):
 return (source.parent/dest).resolve().relative_to(repo.resolve()).as_posix()
def image_tex(item):
 used.append(item['fig_id']);width=item['width_mm'];cap=formatted(item['caption']);path=item['source_png'];label=item['fig_id'];land=item['page_orientation']=='landscape';s=(r'\begin{landscape}'+'\n' if land else '')+r'\begin{figure}[p]'+'\n'+r'\centering'+'\n'+r'\includegraphics[width='+width+r'mm]{\detokenize{'+path+'}}'+'\n'+r'\caption{'+cap+'}'+r'\label{'+label+'}'+'\n'+r'\end{figure}'+'\n'+(r'\end{landscape}'+'\n' if land else '')
 return s
def find_image(path,row):
 # Match the exact planned placement, not the unplaced alias nor a duplicate from a different section.
 loc='appendix' if row['heading'].startswith('Appendix ') else 'body';opts=[x for x in placed if x['source_png']==path and x['body_or_appendix']==loc]
 if loc=='appendix':opts=[x for x in opts if x['section']==row['heading'].split(':')[0]]
 else:opts=[x for x in opts if x['source_section']==Path(row['source file']).name or x['source_section']=='II_state_machines.md']
 return opts[0] if len(opts)==1 else None
def resolve_includes(text,source,seen=None):
 seen=set() if seen is None else seen
 def sub(m):
  p=(source.parent/m.group(1)).resolve()
  if p in seen:raise ValueError('recursive include '+str(p))
  if not p.exists():raise FileNotFoundError(p)
  return '\n'+resolve_includes(p.read_text(encoding='utf-8-sig'),p,seen|{p})+'\n'
 return re.sub(r'<!--\s*include:\s*([^>]+?)\s*-->',sub,text)
def to_tex(text,source,row):
 toks=md.parse(text);out=[];i=0;skipcaption=False
 while i<len(toks):
  t=toks[i]
  if t.type in ['heading_open','paragraph_open'] and i+2<len(toks) and toks[i+1].type=='inline':
   content=toks[i+1];isimage=any(c.type=='image' for c in content.children or [])
   if isimage:
    for im in [c for c in content.children if c.type=='image']:
     dest=im.attrGet('src');path=imgpath(dest,source);item=find_image(path,row)
     if item:out.append(image_tex(item))
    skipcaption=True
   elif skipcaption and re.match(r'^\s*(?:\*\*)?(?:Figure\s|A[13]\.\d+\.)',content.content):skipcaption=False
   else:
    skipcaption=False;z=inline(content)
    if z:out.append((r'\textbf{'+z+'}' if t.type=='heading_open' else z)+'\n\n')
   i+=3;continue
  if t.type in ['fence','code_block']:
   content=t.content.replace('\\end{lstlisting}','[end listing]')
   if '{{LinkRepo}}' in content:
    lines=content.splitlines();out.append(r'\noindent\texttt{git clone \TargetRepo}\par'+'\n');content='\n'.join(lines[1:])
   out.append(r'\begin{lstlisting}'+'\n'+content.rstrip()+'\n'+r'\end{lstlisting}'+'\n');i+=1;continue
  if t.type=='table_open':
   j=i+1;records=[];current=None;cell=None
   while j<len(toks) and toks[j].type!='table_close':
    q=toks[j]
    if q.type=='tr_open':current=[]
    elif q.type in ['th_open','td_open']:cell=''
    elif q.type=='inline' and cell is not None:cell+=inline(q)
    elif q.type in ['th_close','td_close']:current.append(cell);cell=None
    elif q.type=='tr_close':records.append(current)
    j+=1
   count=max(map(len,records),default=1);w=max(.035,min(.9,.92/count));spec=''.join(r'>{\raggedright\arraybackslash}p{'+f'{w:.4f}'+r'\linewidth}' for _ in range(count));land=count>=8
   if land:out.append('\\begin{landscape}\n')
   out.append('\\begin{longtable}{'+spec+'}\n')
   for k,record in enumerate(records):
    record=record+['']*(count-len(record));out.append(' & '.join(record)+r' \\'+'\n')
    if k==0:out.append(r'\hline\endfirsthead'+'\n'+' & '.join(record)+r' \\'+'\n'+r'\hline\endhead'+'\n')
   out.append('\\end{longtable}\n')
   if land:out.append('\\end{landscape}\n')
   i=j+1;continue
  if t.type in ['bullet_list_open','ordered_list_open']:out.append('\\begin{itemize}\n')
  elif t.type in ['bullet_list_close','ordered_list_close']:out.append('\\end{itemize}\n')
  elif t.type=='list_item_open':out.append('\\item ')
  elif t.type in ['hr']:out.append('\\par\\medskip\n')
  i+=1
 return ''.join(out)
# Additional included state-machine blocks are selected by the 2.2 subsection owner.
statefile=repo/'docs/part2/report/II_state_machines.md';stateall=statefile.read_text(encoding='utf-8');blocks={}
for m in re.finditer(r'<!-- BEGIN STATE_MACHINE ([A-Z_]+) -->(.*?)<!-- END STATE_MACHINE \1 -->',stateall,re.S):blocks[m.group(1)]=m.group(2)
if set(sum(plan['state_machine_insertions'].values(),[]))-set(blocks):raise ValueError('state block missing')
styled={x['text']:x['style'] for x in plan['template_styled_headings']};texinputs=[];manifest=[];sections=latex/'sections';sections.mkdir(exist_ok=True)
for idx,row in enumerate(rows,1):
 heading=row['heading'];source=repo/row['source file'] if row['source file'].startswith('docs/') else None
 # Template UC placeholders are intentionally populated from the authorized source title.
 if source and ('[Name]' in heading or '[Actor ' in heading):
  first=source.read_text(encoding='utf-8-sig').splitlines()[0];heading=re.sub(r'^#+\s*','',first).strip()
 style=styled.get(row['heading']);renderheading=formatted(heading);block=''
 if style:
  level={'Heading 1':'section','Heading 2':'subsection','Heading 3':'subsubsection'}.get(style,'paragraph');block='\\'+level+'*{'+renderheading+'}\n'+r'\addcontentsline{toc}{'+level+'}{'+renderheading+'}\n'+r'\pdfbookmark['+str({'Heading 1':0,'Heading 2':1,'Heading 3':2}.get(style,2))+']{'+renderheading+'}{p7h'+str(idx)+'}\n'
 else:block=r'\textbf{'+renderheading+'}'+r'\par'+'\n'
 m=re.match(r'^3\.([1-6])\.3 ',row['heading'])
 if m:block+=r'\label{CRC-UC-0'+m.group(1)+'}\n'
 if source:
  ls=source.read_text(encoding='utf-8-sig').splitlines();pieces=[]
  for a,z in row.get('content_line_ranges',[]):pieces.extend(ls[a-1:z])
  # Source heading is replaced with the exact template heading, not duplicated.
  if pieces and re.match(r'^#+\s',pieces[0]):pieces=pieces[1:]
  text='\n'.join(pieces)+'\n';text=resolve_includes(text,source);block+=to_tex(text,source,row)
  for key in plan['state_machine_insertions'].get(row['heading'],[]):block+=to_tex(blocks[key],statefile,row)
  if row.get('post_content_line_ranges'):
   postsrc=repo/row['post_source_file'];postlines=postsrc.read_text(encoding='utf-8-sig').splitlines();post='\n'.join(line for a,z in row['post_content_line_ranges'] for line in postlines[a-1:z]);block+=to_tex(resolve_includes(post,postsrc),postsrc,row)
 # End of the appendix container also emits the status register, glossary and evidence index once.
 if row['heading']=='Appendix':
  for name in ['Appendix_Glossary.md','Appendix_P4_status.md','Appendix_Evidence_Index.md']:
   p=repo/'docs/part2/report'/name;block+=to_tex(p.read_text(encoding='utf-8-sig'),p,row)
 path=sections/f'section_{idx:03d}.tex';path.write_text(block.rstrip()+'\n',encoding='utf-8');texinputs.append(r'\input{sections/'+path.stem+'}');manifest.append({'heading':row['heading'],'file':str(path.relative_to(latex))})
print('Generated',len(manifest),'section drafts; figure placements emitted',len(used),'distinct',len(set(used)),'missing',len(set(x['fig_id'] for x in placed)-set(used)),'unknown Unicode/tokens',len(unknown));(base/'Part2/notes/P7/latex_draft_receipt.json').write_text(json.dumps({'sections':manifest,'figures_emitted':used,'missing_figures':sorted(set(x['fig_id'] for x in placed)-set(used)),'unknown':unknown},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
