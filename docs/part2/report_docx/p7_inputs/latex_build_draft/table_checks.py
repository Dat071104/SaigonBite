from pathlib import Path
from docx import Document
import re
B=Path(r'D:\RAD\FINAL');L=B/'SaigonBite/docs/part2/latex'
def norm(s):return ' '.join(s.split())
def decode(s):
 s=s.strip();s=re.sub(r'\\(?:textbf|textit|texttt|emph)\{([^{}]*)\}',r'\1',s)
 for a,b in [(r'\ldots{}','…'),(r'\textbackslash{}','\\'),(r'\textasciitilde{}','~'),(r'\textasciicircum{}','^'),(r'\textless{}','<'),(r'\textgreater{}','>'),(r'\textdagger{}','†'),(r'\S{}','§'),(r'\ensuremath{\cdot}','·'),(r'\ensuremath{\rightarrow}','→')]:s=s.replace(a,b)
 s=re.sub(r'\\([_%&#${}])',r'\1',s);s=s.replace('---','—').replace('--','–').replace('``','“').replace("''",'”')
 return norm(s)
def latex_headers():
 out=[]
 for p in sorted((L/'sections').glob('section_*.tex')):
  s=p.read_text(encoding='utf-8');out += [[decode(x) for x in re.split(r'(?<!\\)&',m.group(1))] for m in re.finditer(r'\\begin\{longtable\}[^\n]*\n(.*?)\s*\\\\\s*\n',s)]
 return out
def word_headers(d):return [[norm(c.text) for c in t.rows[0].cells] for t in d.tables]
def template_check(actual):
 template=word_headers(Document(B/'RAD_Sem01_2627_Report_Template.docx'));counts={3:1,4:1,5:1,6:1,7:2,8:1,9:1,10:1,11:1,12:3,15:1,16:1};errors=[]
 for i,need in counts.items():
  exp=template[i];matches=[a for a in actual if a[:len(exp)]==exp]
  if len(matches)<need:errors.append((i,exp,need,len(matches)))
 return errors

def verify_moves():
 import json
 audit=json.loads((B/'Part2/notes/P7/table_move_audit.json').read_text(encoding='utf-8'));errors=[]
 for a in audit:
  idx=a['template_table']
  for k,(o,n) in enumerate(zip(a['old'],a['new']),1):
   if idx==3:e=[o[2],o[3],o[0],o[1],o[4]]
   elif idx==4:e=o
   elif idx==5:e=[o[0],o[1],o[2]+' / '+o[3],o[6],o[4],o[5]]
   elif idx==6:e=[o[0],o[1],o[2],o[6],o[3],o[4],o[5],o[7]]
   elif idx==7:e=[o[0],o[1],('NFR' if o[0].startswith('NFR') else 'FR'),o[2],o[3],o[4],o[5]]
   elif idx==9:e=[o[0]+' '+o[1],o[3],o[4],o[5],o[6],o[7],o[2]]
   elif idx==10:e=[o[0],o[1],o[2],o[4],o[5],o[3],o[6]]
   else:raise ValueError(idx)
   if e!=n:errors.append((a['source'],k))
   line='| '+' | '.join(n)+' |'
   if line not in (B/'SaigonBite/docs/part2/report'/a['source']).read_text(encoding='utf-8').splitlines():errors.append((a['source'],k,'missing from current source'))
  if len(a['old'])!=len(a['new']):errors.append((a['source'],'row count'))
 return sum(len(a['old']) for a in audit),errors
