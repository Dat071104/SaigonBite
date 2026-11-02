from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from collections import Counter
import json,csv,re,hashlib
B=Path(r'D:\RAD\FINAL');R=B/'SaigonBite';L=R/'docs/part2/latex';D=B/'Part2/deliverables/Team02_BRS_SRS_for_SaigonBite.docx';o=R/'docs/part2/test_report/p7_2026-10-28';o.mkdir(exist_ok=True,parents=True)
from docx import Document
from docx.oxml.ns import qn
plan=json.loads((B/'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8')); m=list(csv.DictReader((L/'figure_manifest.csv').open(encoding='utf-8-sig',newline=''))); figs=[x for x in m if x['record_type']=='figure'];d=Document(D); paragraphs=d.paragraphs; w={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
checks=[];parity=[]
def ck(out,n,v,detail):out.append((n,bool(v),detail))
def cleantext(e):return ''.join(e.xpath('.//w:t/text()',namespaces=w))
with ZipFile(D) as z:
 xml=z.read('word/document.xml').decode('utf-8');root=etree.fromstring(xml.encode('utf-8'));settings=etree.fromstring(z.read('word/settings.xml'));rels=etree.fromstring(z.read('word/_rels/document.xml.rels'));names=set(z.namelist());rr={e.get('Id'):e.get('Target') for e in rels};refs=root.xpath('//a:blip/@r:embed',namespaces=w);missing=[(x,rr.get(x)) for x in refs if x not in rr or ('word/'+rr[x].lstrip('/')) not in names];media=[x for x in names if x.startswith('word/media/')]
 ck(checks,'images resolve',len(refs)==len(figs) and not missing,f'{len(refs)} placements, {len(media)} unique media, missing={missing[:5]}')
 receipt=json.loads((B/'Part2/notes/P7/docx_draft_receipt.json').read_text(encoding='utf-8'));lookup={x['fig_id']:x for x in figs};hashes=[hashlib.sha256(z.read('word/'+rr[x])).hexdigest() for x in refs];bad_hash=[fig for fig,h in zip(receipt['figures'],hashes) if lookup[fig]['sha256']!=h];ck(checks,'original PNG bytes',len(hashes)==len(figs) and not bad_hash,f'{len(hashes)} image hashes checked; mismatches={bad_hash[:5]}')
 bookmarks=set(root.xpath('//w:bookmarkStart/@w:name',namespaces=w));fields=root.xpath('//w:fldSimple/@w:instr',namespaces=w);targets=[re.search(r'PAGEREF\s+(\S+)',x).group(1) for x in fields if re.search(r'PAGEREF\s+(\S+)',x)];bad_targets=[x for x in targets if x not in bookmarks];ck(checks,'PAGEREF bookmarks',bool(targets) and not bad_targets,f'{len(targets)} fields; missing={bad_targets[:5]}')
 ck(checks,'settings and TOC',bool(settings.xpath('//w:updateFields',namespaces=w)) and bool(settings.xpath('//w:doNotAutoCompressPictures',namespaces=w)) and bool(root.xpath('//w:fldSimple[contains(@w:instr,"TOC")]',namespaces=w)),'updateFields, no image compression and TOC field')
 markers=[x for x in ['⟦','TODO','[VERIFY]','{{','Guidance (delete before submitting)'] if x in xml];ck(checks,'unresolved markers',not markers,str(markers))
 ck(checks,'Word document opens',True,f'{D.stat().st_size} bytes; sha256 {hashlib.sha256(D.read_bytes()).hexdigest()}')
 code_text=next(x.read_text(encoding='utf-8') for x in sorted((L/'sections').glob('section_*.tex')) if '4.3.5 Software Classes Method Code' in x.read_text(encoding='utf-8').splitlines()[0]);n_ex=len(json.loads((B/'Part2/notes/P7/code_excerpt_receipt.json').read_text(encoding='utf-8')));excerpts=re.findall(r'\\begin\{lstlisting\}\n(.*?)\n\\end\{lstlisting\}',code_text,re.S);doc_paragraphs=[p.text.rstrip('\n') for p in paragraphs];missing_code=[i for i,x in enumerate(excerpts,1) if x not in doc_paragraphs];code_links=[x.get('Target') for x in rels if 'blob/v0.9-part2' in str(x.get('Target'))];ck(checks,'code excerpts and tag links',len(excerpts)==n_ex and not missing_code and len(code_links)==n_ex,f'{len(excerpts)} excerpts matched; missing={missing_code}; {len(code_links)} tag links (available after push)')
 actual=[(p.style.name,p.text.strip()) for p in paragraphs if p.style.name.startswith('Heading ')]; templ=plan['template_styled_headings']; expected=[]
 for t in templ:
  h=t['text']
  if '[Name]' in h or '[Actor ' in h:
   row=next(r for r in plan['sections'] if r['heading']==h);number=re.match(r'^[0-9]+(?:\.[0-9]+)+',h).group();src=R/row['source file'];hit=[re.sub(r'^#+\s*','',x).strip() for x in src.read_text(encoding='utf-8-sig').splitlines() if re.match(r'^#+\s+'+re.escape(number)+r'(?:\s|$)',x)];h=hit[0]
  expected.append((t['style'],h))
 differences=[(i,a,b) for i,(a,b) in enumerate(zip(expected,actual)) if a!=b];ck(checks,'template headings',actual==expected,f'expected {len(expected)}, actual {len(actual)}, mismatch={differences[:5]}')
 ck(parity,'heading style and text',actual==expected,f'{len(actual)} DOCX headings compared in template order to independently checked LaTeX')
 book=set(root.xpath('//w:bookmarkStart/@w:name',namespaces=w)); wanted={'B'+re.sub('[^A-Za-z0-9_]','_',x['fig_id']) for x in figs};ck(parity,'figure IDs',wanted<=book and len(wanted)==len(figs),f'{len(wanted & book)}/{len(wanted)} manifest IDs in DOCX and LaTeX')
 texfiles=[L/'sections'/f'section_{i:03}.tex' for i in range(1,len(plan['sections'])+1)];texts=[x.read_text(encoding='utf-8') for x in texfiles];tex_table=sum(len(re.findall(r'\\begin\{longtable\}',x)) for x in texts)+2;word_table=len(root.xpath('//w:tbl',namespaces=w));ck(parity,'table count',tex_table==word_table,f'LaTeX {tex_table}; DOCX {word_table}, including two front tables')
 # Compare all PC/MG entries in the 5.1 test table, not every repeated mention elsewhere.
 ids=Counter(x['pc_mg_id'] if 'pc_mg_id' in x else '' for x in [])
 first=next(i for i,x in enumerate(plan['sections']) if x['heading'].startswith('5.1 '));tx=texts[first];tex_ids=Counter(re.findall(r'(?m)^(UC\d\d-(?:PC|MG)\d\d)\s*&',tx))
 b=root.find('w:body',namespaces=w);active=False;word_ids=Counter()
 for e in b:
  text=cleantext(e)
  if e.tag==qn('w:p') and text.startswith('5.1 '):active=True;continue
  if active and e.tag==qn('w:p') and text.startswith('5.2 '):break
  if active and e.tag==qn('w:tbl'):
   for tr in e.xpath('./w:tr',namespaces=w):
    tc=tr.xpath('./w:tc[1]',namespaces=w)
    if tc:
     t=cleantext(tc[0]);
     if re.fullmatch(r'UC\d\d-(?:PC|MG)\d\d',t):word_ids[t]+=1
 ck(parity,'5.1 test table rows',tex_ids==word_ids and sum(tex_ids.values())==30,f'LaTeX {sum(tex_ids.values())}; DOCX {sum(word_ids.values())}; diff={list((tex_ids-word_ids).items())[:5]} / {list((word_ids-tex_ids).items())[:5]}')
 # Compare the numeric tokens rendered by each section. Word table cells are separated;
 # TeX commands and the duplicated longtable continuation header are removed, not content.
 numeric_diffs=[]
 for i,row in enumerate(plan['sections']):
  if not row['heading'].startswith(('Executive Summary','5.1 ','Conclusions / Recommendations')):continue
  heading=row['heading'];nex=plan['sections'][i+1]['heading'];active=False;parts=[]
  for e in b:
   txt=cleantext(e)
   if e.tag==qn('w:p') and txt==heading:active=True;continue
   if active and e.tag==qn('w:p') and txt==nex:break
   if active:
    if e.tag==qn('w:tbl'):
     parts.extend(' '.join(cleantext(cell) for cell in tr.xpath('./w:tc',namespaces=w)) for tr in e.xpath('./w:tr',namespaces=w))
    else:parts.append(txt)
  t=texts[i];t='\n'.join(t.splitlines()[3:]);t=re.sub(r'\\begin\{longtable\}[^\n]*','',t);t=re.sub(r'\\hline\\endfirsthead\s*.*?\\hline\\endhead','',t,flags=re.S);t=re.sub(r'\\(?:label|ref|pageref|pdfbookmark|addcontentsline)\{[^}]*\}','',t);t=re.sub(r'\\[a-zA-Z]+(?:\[[^]]*\])?','',t)
  pattern=r'\d+(?:[.,]\d+)*';texnums=Counter(re.findall(pattern,t));wordnums=Counter(re.findall(pattern,' '.join(parts)))
  if texnums!=wordnums:numeric_diffs.append((heading,dict(texnums-wordnums),dict(wordnums-texnums)))
 ck(parity,'ES, 5.1 and Conclusions numeric equivalence',not numeric_diffs,'digit-token multiset compared per section; differences='+str(numeric_diffs[:3]))
from table_checks import latex_headers, word_headers, template_check
theaders=latex_headers();wheaders=word_headers(d)[2:];table_errors=template_check(word_headers(d));ck(checks,'template table headers',not table_errors,f'template prefix comparisons; errors={table_errors}')
wide_bad=[]
for ti,table in enumerate(d.tables,1):
 if len(table.columns)>6:
  for run in table._tbl.xpath('.//w:r[w:t]'):
   sz=run.xpath('./w:rPr/w:sz/@w:val')
   if not sz or int(sz[0])<16:wide_bad.append(ti);break
ck(checks,'wide table text size',not wide_bad,f'wide tables use at least 8 pt; violations={wide_bad[:10]}')
header_diffs=[(i+1,a,b) for i,(a,b) in enumerate(zip(theaders,wheaders)) if a!=b];ck(parity,'all table headers',len(theaders)==len(wheaders) and not header_diffs,f'LaTeX {len(theaders)}; DOCX {len(wheaders)}; differences={header_diffs[:8]}')
for path,out in [(o/'docx_checks.txt',checks),(o/'parity.txt',parity)]:
 result=['P7 DOCX structural check: no PDF or visual rendering','']+[('PASS' if v else 'FAIL')+' | '+n+' | '+detail for n,v,detail in out]+['','OVERALL: '+('PASS' if all(x[1] for x in out) else 'FAIL')];path.write_text('\n'.join(result)+'\n',encoding='utf-8');print(path);print('\n'.join(result))

if not all(v for _,v,_ in checks+parity): raise SystemExit(1)
