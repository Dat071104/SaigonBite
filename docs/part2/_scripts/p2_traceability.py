"""Add requirement-specific analysis references; keep later evidence columns blank."""
from pathlib import Path
import csv
import re

DOC=Path(__file__).resolve().parents[1]
MAP={
1:['SUC02-PC01'],2:['SUC02-PC02','SUC02-PC03'],3:['SUC01-PC01','SUC01-PC02','SUC08-PC02'],
4:['UC06-PC03','UC01-MG01'],5:['UC01-PC04'],6:['UC01-MG03','UC01-PC06'],7:['UC01-PC03','UC01-MG01'],
8:['UC01-PC04'],9:['UC01-PC04','UC01-MG01'],10:['UC01-PC04'],11:['UC01-MG01'],12:['UC01-PC05','UC01-MG01'],
13:['UC01-MG02','UC01-MG01'],14:[f'UC01-PC{x:02}' for x in range(1,7)],15:['SUC03-PC01'],16:['SUC03-PC02'],
17:['SUC04-PC01','SUC04-PC02'],18:['UC02-PC01','UC02-MG01'],19:['UC02-PC01','UC02-MG01'],20:['UC02-PC02','UC02-MG01'],
21:['UC02-PC03'],22:['UC03-PC01','UC03-PC02','UC03-MG01'],23:['UC04-PC01','UC04-MG01'],24:['UC04-PC01','UC04-MG01'],
25:['UC04-PC01','UC04-PC02','UC04-MG01'],26:['UC05-MG01','UC05-PC01','UC05-PC02'],27:['UC05-PC01','UC05-PC02'],
28:['UC05-PC03','UC05-MG01'],29:['UC05-PC03','SUC03-PC01','SUC03-PC03','SUC03-PC05'],30:['UC05-MG01','UC05-PC01','SUC05-PC01'],
31:['UC05-PC04','UC05-MG01','SUC03-PC05'],32:['UC05-PC04','SUC03-PC03'],33:['SUC03-PC04','UC05-MG01'],34:['SUC05-PC01','SUC05-PC02'],
35:['SUC06-PC01','UC06-PC02'],36:['UC06-PC01','UC06-MG01','UC06-MG02'],37:['UC06-PC02','UC06-MG01'],
38:['SUC07-PC01','SUC07-PC02'],39:['SUC08-PC01','SUC08-PC02'],40:['SUC09-PC01','SUC09-PC02']}
NFR={1:['UC01-MG01','UC02-MG01','UC03-MG01','UC04-MG02','UC05-MG01','UC06-MG02','SUC01-PC01'],
     2:['UC01-MG02'],11:['SUC09-PC01','SUC09-PC02'],12:['UC01-MG01','UC01-MG02','UC02-MG01','UC05-MG01','UC05-PC04']}
LATER={3:'P6 durability across restart; successful checkout creation PCs do not prove durability',
       4:'P6 latency measurements; no measured response-time anchor in P2.3',
       5:'BR-12 privacy constraint is retained in SUC-02/08 and UC-02/05; full disclosure verification is P4/P5',
       6:'P3/P4 CSRF boundary and request checks; domain refusal PCs do not prove transport protection',
       7:'P3/P4/P6 production-secret configuration',8:'P6 HTTPS deployment',9:'P5 viewport/UI verification',10:'P3 architecture/layer allocation'}

def rows(name):
    with (DOC/name).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def main():
    main_ids={r['id'] for r in rows('pc_mg_register.csv')}
    supporting=set(re.findall(r'SUC\d\d-PC\d\d',(DOC/'SUC.md').read_text(encoding='utf-8')))
    matrix=rows('analysis_consistency.csv'); by_anchor={}
    for r in matrix: by_anchor.setdefault(r['PC/MG'],[]).append(r)
    path=DOC/'traceability.csv'; trace=rows('traceability.csv'); columns=list(trace[0])
    for r in trace:
        kind,n=r['Req ID'].split('-'); n=int(n)
        anchors=MAP[n] if kind=='FR' else NFR.get(n,[])
        assert all(x in main_ids|supporting for x in anchors),r['Req ID']
        refs=[]; sections=set()
        for a in anchors:
            if a.startswith('SUC'):
                refs.append('docs/part2/SUC.md#'+a)
                sections.add('II.2.1.5 (supporting contract)')
            else:
                matched=by_anchor[a]; uc=matched[0]['UC']; number=int(uc[-2:]); sections.add(f'II.2.2.{number}')
                refs.append('analysis_consistency.csv#'+a+' ('+'; '.join(dict.fromkeys(x['SSD message'] for x in matched))+')')
        if anchors:
            r['PC/MG ID']='; '.join(anchors); r['activity/SSD/state ref']='; '.join(refs)
            r['status']='Analysed'; r['report section']='I.1.7; '+'; '.join(sorted(sections))
        else:
            assert kind=='NFR' and n in LATER
            r['PC/MG ID']=''; r['activity/SSD/state ref']='Analysis constraint retained; '+LATER[n]+'; not closed by a P2 anchor'
            r['status']='Planned'; r['report section']='I.1.7; II (constraint context only)'
        for c in ['design operation','screen/control','code method','test ID','result evidence']: assert not r[c],(r['Req ID'],c)
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=columns); writer.writeheader(); writer.writerows(trace)
    print('Traceability:',sum(r['status']=='Analysed' for r in trace),'Analysed;',sum(r['status']=='Planned' for r in trace),'cross-cutting NFRs retained Planned; no later evidence filled.')

if __name__=='__main__': main()
