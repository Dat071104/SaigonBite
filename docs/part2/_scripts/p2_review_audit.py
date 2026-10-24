"""Check the corrected cross-page activity graphs and six review dispositions.

Document-model validation only; never imports or executes application code.
"""
from pathlib import Path
import csv,json,xml.etree.ElementTree as ET

R=Path('D:/RAD/FINAL/SaigonBite');D=R/'docs/part2';OUT=Path('D:/RAD/FINAL/Part2/notes/P2-root')
def traverse(start,adj):
 seen=set();todo=list(start)
 while todo:
  x=todo.pop()
  if x not in seen:seen.add(x);todo.extend(adj.get(x,[]))
 return seen
def graph(uc,pairs):
 nodes={};edges=[];initial=[];final=[]
 for part in 'ABC':
  path=R/f'models/UC-{uc}/activity_uc{uc}_Part{part}.drawio'
  for c in ET.parse(path).findall('.//mxCell'):
   ident=(part,c.get('id'));style=c.get('style','');label=c.get('value','')
   if c.get('edge')=='1':edges.append(((part,c.get('source')),(part,c.get('target'))))
   elif c.get('vertex')=='1':
    nodes[ident]=c
    if 'shape=endState;' in style:final.append(ident)
    elif 'ellipse;' in style and not label and 'fillColor=#004387;' in style:initial.append(ident)
 assert len(initial)==1,(uc,'initial nodes',initial)
 assert initial[0][0]=='A' and final
 for a,b in pairs:assert a in nodes and b in nodes;edges.append((a,b))
 adj={};rev={}
 for a,b in edges:adj.setdefault(a,[]).append(b);rev.setdefault(b,[]).append(a)
 control={x for e in edges for x in e}|set(initial)|set(final)
 assert control<=traverse(initial,adj),(uc,'unreachable',control-traverse(initial,adj))
 assert control<=traverse(final,rev),(uc,'cannot finish',control-traverse(final,rev))
 return {'sole_initial':initial,'activity_finals':final,'control_nodes':len(control),'control_edges_including_continuations':len(edges),'all_reachable':True,'all_can_reach_complete_final':True,'paired_continuations':pairs}

def main():
 out={'activity_graphs':{}}
 out['activity_graphs']['UC-02']=graph('02',[(('A','TF'),('B','I')),(('B','FL'),('C','I'))])
 out['activity_graphs']['UC-04']=graph('04',[(('A','WB'),('B','I')),(('A','DP'),('C','I')),(('B','F'),('A','R_entry')),(('C','F'),('A','R_entry'))])
 out['activity_graphs']['UC-06']=graph('06',[(('A','CA-mi'),('B','CB-start')),(('A','CA-hl'),('C','CC-start')),(('B','CB-final'),('A','CA-return')),(('C','CC-final'),('A','CA-return'))])
 for path in [R/'models/UC-06/ssd_uc06_PartA.json',D/'analysis_consistency.csv']:
  text=path.read_text(encoding='utf-8');assert 'Active-name uniqueness' not in text and 'Duplicate active names/pair' not in text
 item=json.loads((R/'models/UC-06/activity_uc06_PartB.json').read_text(encoding='utf-8'))['pages'][0]
 assert 'update/archive only: existing ACTIVE item' in item['validate']
 for uc,stem in [('03','activity_uc03'),('06','activity_uc06_PartA'),('06','activity_uc06_PartB'),('06','activity_uc06_PartC')]:
  p=json.loads((R/f'models/UC-{uc}/{stem}.json').read_text(encoding='utf-8'))['pages'][0]
  assert 'recheck active Admin; denial ends' in p['read']
 for part,ids in [('B',['05S-R08a','05S-R08b','05S-R08c','05S-R08d']),('C',['05S-R09','05S-R09b','05S-R09c'])]:
  data=json.loads((R/f'models/UC-05/ssd_uc05_Part{part}.json').read_text(encoding='utf-8'));e={v['id']:v for v in data['edges']}
  assert set(ids)<=set(e)
  assert 'committed' in e[ids[0]]['label']
  assert 'controlledFailure; rollback' in e[ids[-1]]['label'] and 'MG01' in e[ids[-1]]['label']
 with (D/'ssd_operations.csv').open(encoding='utf-8',newline='') as f:ops=list(csv.DictReader(f))
 assert len(ops)==60 and all('controlledFailure' in r['returns'] for r in ops if r['operation'] in ('acceptReplacement','declineReplacement'))
 assert 'step 6\'s transaction' not in (D/'UC-01/description.md').read_text(encoding='utf-8')
 out.update({'review_findings_covered':['R1','R2','R3','R4','R5','R6'],'operations':60,'application_tests_run':False,'pass':True})
 (OUT/'review_corrections_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
