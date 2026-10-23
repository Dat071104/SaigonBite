"""Derive workbook cell updates from the integrated English report sources.

This module only writes JSON authoring inputs. Artifact Tool authors the cells.
Run only after all four drafting workers have finished.
"""
from pathlib import Path
import json
import re

ROOT = Path(r"D:\RAD\FINAL")
DOC = ROOT / "SaigonBite/docs/part2"
BASE = ROOT / "Part2"


def plain(value):
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return value.replace("**", "").replace("`", "").replace("\\|", "|").replace("<br>", " ").strip()


def tables(path):
    result, current = [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if line.startswith("|"):
            cells = [plain(c) for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
            if all(re.fullmatch(r"[:\-\s]+", c) for c in cells):
                continue
            current.append(cells)
        elif current:
            result.append(current)
            current = []
    return result


def records(path, pattern):
    result = []
    for table in tables(path):
        for row in table[1:]:
            if re.fullmatch(pattern, row[0]):
                if len(row) != len(table[0]):
                    raise ValueError((path.name, row[0], "ambiguous Markdown table"))
                result.append(dict(zip(table[0], row)))
    return result


def discover():
    for path in sorted((DOC / "report").glob("I_1*.md")):
        print(path.name)
        for table in tables(path):
            print(json.dumps({"header": table[0], "rows": len(table)-1,
                              "first_id": table[1][0] if len(table)>1 else None}, ensure_ascii=False))


UPDATES, LAYOUT = [], {}


def put(sheet, cell, value=None, formula=None, style_from=None):
    u = dict(sheet=sheet, cell=cell, value=value)
    if formula:
        u['formula'] = formula
    if style_from:
        u['style_from'] = style_from
    UPDATES.append(u)


def fit(sheet, row, values, widths):
    import textwrap
    lines = max((len(textwrap.wrap(str(v), width=w)) for v,w in zip(values,widths)), default=1)
    LAYOUT.setdefault(sheet,{}).setdefault('heights',{})[str(row)] = min(409,max(56,lines*14+20))


def assumptions():
    s='Assumption Log'
    rows=records(DOC/'report/I_1-4_narrative_assumptions.md',r'A-\d{2}')
    assert len(rows)==19
    for col,label,style in [('J','Current status','F4'),('K','Current interpretation','B4'),('L','Confirmation or source basis','C4')]:
        put(s,col+'4',label,style_from=style)
    put(s,'G4','Date recorded')
    for row,r in enumerate(rows,5):
        original,*current=re.split(r'Part 2 refinement:|Current D-2 roster:',r['Assumption'],maxsplit=1)
        original=re.sub(r'^Part 1 wording(?: \(historical\))?:\s*','',original).strip()
        original=original.replace('⟦ACTUAL m3_short: short name⟧','Quan N.')
        data={'A':r['ID'],'B':original,'C':r['Reason'],'D':r['Q&A ID'],'E':r['Affects (UC/BR)'],
              'F':'Team decision (not confirmed)','H':'Part 2 report 1.4.2','J':r['Status'],
              'K':current[0].strip() if current else r['Assumption'],'L':r['Confirmed by + date']}
        if row>=16:
            data['G']=46318
        for col,value in data.items():
            put(s,f'{col}{row}',value,style_from=f'{col if col<"I" else "B"}5')
            if col == 'G':
                UPDATES[-1]['format_from']='G5'
        fit(s,row,[data[c] for c in ['B','C','E','J','K','L']],[44,36,26,34,64,54])
    put(s,'B26','Default-category count (status in J)')
    LAYOUT[s].update(new_columns={'10':34,'11':64,'12':54},dimension='A1:L26')


def questions():
    s='Client Q&A'
    for row in range(5,10):
        put(s,f'H{row}','Submitted')
    for row in range(10,15):
        for col in 'ABCDEFGHKL':
            put(s,f'{col}{row}',None)
    defaults=[
        'Team default: load PLACED/CONFIRMED/PREPARING; busy at capacity; quiet below25% before insert, discount min(5,000 VND,fee). Q1 unanswered; BR-01–04 / A-02–03,A-12–13.',
        'Team default: approximate district-centroid Haversine distance; raw radius <=8km; base fee +3,000 VND x max(1,ceil(km)). Q2 unanswered; BR-05–07 / A-14–15.',
        'Team default: cancel PLACED/CONFIRMED; COD VOIDED, ONLINE REFUND_PENDING with full captured amount owed. Payout deferred, never claimed paid. Q3 unanswered; BR-15/17 and plan3.3.',
        'Team default: clearly labelled ONLINE simulator; Local E_WALLET/BANK_QR, Tourist INTERNATIONAL_CARD; both COD. No real provider. Q4 unanswered; BR-14 / A-05.',
        'Team default: sales by DELIVERED finish time on Vietnam dates; workload now; wait READY to PICKED_UP, ride PICKED_UP to DELIVERED; failure rate failed/(delivered+failed), sample sizes, n/a at zero. Q5 unanswered; BR-20–24.']
    for row,value in enumerate(defaults,5):
        put(s,f'F{row}',value)
    put(s,'B20','Q&A status')
    put(s,'C20','5/5 slots used. Dates and answers unknown. L1–L6: decision_log.md; planned 26/10, checkpoint 31/10.')
    LAYOUT[s]={'heights':{str(i):154 for i in range(5,10)}}


def backlog(book):
    s='Backlog & Risks'; path=DOC/'report/I_1-3_iterations_backlog_risks.md'
    rows=records(path,r'BL-\d{2}'); assert len(rows)==20
    put(s,'I4','MoSCoW',style_from='C4'); put(s,'J4','Full iteration window',style_from='D4')
    for row,r in enumerate(rows,5):
        vals=[r['ID'],r['User story'],'High',int(re.search(r'I([1-6])',r['Iteration'])[1]),r['UC/SUC link'],'722I0004','Backlog']
        for col,value in zip('ABCDEFG',vals):
            put(s,f'{col}{row}',value)
        put(s,f'I{row}',r['MoSCoW'],style_from='C5'); put(s,f'J{row}',r['Iteration'],style_from='D5')
        fit(s,row,[vals[1],vals[4]],[49,18])
    put(s,'B25','D-4 supersedes proposal exclusions. BL-01–BL-20 are current Must items; W-01–W-03 below remain outside this release. Backlog is planned, not a test result.')
    fit(s,25,[UPDATES[-1]['value']],[49])
    for col,value in zip('ABCDEFG',['ID','Deferred or future scope','Priority','Iteration','Source','Actual author','Status']):
        put(s,f'{col}38',value,style_from=f'{col}4')
    for row,r in enumerate(records(path,r'W-\d{2}'),39):
        vals=[r['ID'],r['User story'],"Won't this release",'—',r['UC/SUC link'],'722I0004','Deferred / future']
        for col,value in zip('ABCDEFG',vals):
            put(s,f'{col}{row}',value,style_from=f'{col}5')
        fit(s,row,[vals[1],vals[4]],[49,18])
    LAYOUT[s].update(new_columns={'9':18,'10':24},dimension='A1:J48')
    LAYOUT[s]['heights'].update({'38':60,'45':60})
    risks(book,s,path)


def risks(book,s,path):
    notes={28:'R-10: conservative D-4 paths; L1/L3 and checkpoint31/10.',29:'Assess all affected artifacts when Q/A/BR answers differ; checkpoint31/10.',
           30:'R-08: planned independent-connection capacity/transition races and rollback checks.',
           31:'D-1: Dat owns shared contracts and integration; no work is assigned to another member without evidence.',
           32:'R-06: sole actual author722I0004; no invented pairing or other-member contributions.'}
    for row,text in notes.items():
        put(s,f'H{row}','Historical proposal risk; current mitigation: '+text)
        fit(s,row,[book[s][f'B{row}'].value,text],[49,40])
    for col in 'ABCDEFGH':
        put(s,f'{col}45',book[s][f'{col}27'].value,style_from=f'{col}27')
    for index,r in enumerate(records(path,r'R-\d{2}')):
        row=33+index if index<3 else 43+index
        vals=[r['ID'],r['Risk']+' Trigger: '+r['Trigger'],r['Likelihood'],r['Impact'],'722I0004','Open',r['Mitigation']]
        for col,value in zip('ABCDFGH',vals):
            put(s,f'{col}{row}',value,style_from=f'{col}28')
        if row>=46:
            put(s,f'E{row}',formula=f'=IF(OR(C{row}="",D{row}=""),"",MATCH(C{row},{{"Low","Medium","High"}},0)*MATCH(D{row},{{"Low","Medium","High"}},0))',style_from='E28')
        fit(s,row,[vals[1],vals[-1]],[49,40])
    LAYOUT[s]['validations']=[{'from':'C5:C24 C28:D35','to':'C46:D48'},{'from':'G28:G35','to':'G46:G48'}]


def requirements(book):
    s='Requirements List'; rows=records(DOC/'report/I_1-7_requirements.md',r'(?:FR|NFR)-\d{2}'); assert len(rows)==52
    extra=[('I','Canonical Req ID','A4'),('J','Acceptance criterion / measurement','B4'),('K','MoSCoW','D4')]
    for col,label,style in extra:
        put(s,col+'4',label,style_from=style); put(s,col+'48',label,style_from=style)
    for col in 'ABCDEFGH':
        put(s,f'{col}48',book[s][f'{col}4'].value,style_from=f'{col}4')
    for index,r in enumerate(rows):
        row=5+index if index<40 else 49+index-40
        vals={'B':r['Requirement'],'C':r['ID'].split('-')[0],'D':'High','E':r.get('UC/SUC',r.get('UC/SUC scope')),
              'F':r['Source'],'G':'Draft','I':r['ID'],'J':r.get('Acceptance criterion',r.get('Acceptance criterion and measurement method')),'K':r['MoSCoW']}
        for col,value in vals.items():
            put(s,f'{col}{row}',value,style_from=f'{col if col<"I" else "B"}5')
        if row>=49:
            put(s,f'A{row}',formula=f'=IF(C{row}="","",C{row}&(COUNTIF($C$5:$C$44,C{row})+COUNTIF($C$49:C{row},C{row})))',style_from='A5')
            put(s,f'H{row}',None,style_from='H5')
        fit(s,row,[vals[c] for c in ['B','E','F','J']],[56,16,16,90])
    put(s,'B46','Template block rows5–44 only: FR / NFR')
    put(s,'B63','All Phase1 requirements: FR / NFR',style_from='B46')
    for col,kind in [('C','FR'),('D','NFR')]:
        put(s,f'{col}63',formula=f'=COUNTIF(C5:C44,"{kind}")+COUNTIF(C49:C60,"{kind}")',style_from=col+'46')
    put(s,'B65','Column A keeps template formulas; I has canonical report/CSV IDs. High maps Must; Draft maps Planned. All targets remain unmeasured.',style_from='B5')
    fit(s,65,[UPDATES[-1]['value']],[56])
    LAYOUT[s]['heights']['48']=60
    LAYOUT[s].update(new_columns={'9':18,'10':90,'11':16},dimension='A1:K65',autoFilter='A4:K44',validations=[
        {'from':'C5:C44','to':'C49:C60'},{'from':'D5:D44','to':'D49:D60'},{'from':'G5:G44','to':'G49:G60'}])


def iterations():
    s='Iteration Plan'
    rows=[r for r in records(DOC/'report/I_1-3_iterations_backlog_risks.md',r'I[1-6]') if 'Goal and UC/SUC focus' in r]
    assert len(rows)==6
    for row,r in enumerate(rows,5):
        for col,value in [('B',r['Goal and UC/SUC focus']),('C','See report1.3 BL/W linkage; '+r['Goal and UC/SUC focus']),('D',r['Planned deliverables and exit evidence'])]:
            put(s,f'{col}{row}',value)
        if row>5:
            put(s,f'G{row}','Planned')
        fit(s,row,[r['Goal and UC/SUC focus'],r['Planned deliverables and exit evidence']],[40,44])


def ai_log():
    s='AI Usage Log'
    for row,values in enumerate(tables(DOC/'ai_usage_log.md')[0][1:],8):
        for col,value in zip('ABCDEFG',[str(row-4)]+values+['722I0004']):
            put(s,f'{col}{row}',value)
        fit(s,row,values,[20,40,40,40,50])
    corrections={6:('Historical Part1 outline entry; later AI-generated code, text and diagrams are separately declared below.','Historical source entry; this session did not independently verify that outline session.'),
                 7:('Historical correction: substantial AI-generated I1 skeleton, schema/seed, domain/controllers/DAOs/views and tests, followed by reviews; not merely boilerplate. See proposal7.3 and locked plan.','Historical tests are source-attributed, not rerun in Phase1. The P0 WIP baseline remains red.')}
    for row,(kept,verified) in corrections.items():
        put(s,f'E{row}',kept); put(s,f'F{row}',verified); fit(s,row,[kept,verified],[40,50])


def build():
    import openpyxl
    book=openpyxl.load_workbook(ROOT/'Part1_v2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx')
    assumptions(); questions(); backlog(book); requirements(book); iterations(); ai_log()
    for spec in LAYOUT.values():
        spec.setdefault('heights',{})['4']=60
    views=[('Assumption Log','A11:L13','assumptions_superseded'),('Assumption Log','A16:L19','assumptions_new'),('Client Q&A','F5:L9','qa_current'),('Client Q&A','B16:L20','qa_limit'),
           ('Backlog & Risks','A5:J8','backlog_current'),('Backlog & Risks','A33:H35','risks_current'),('Backlog & Risks','A38:G41','deferred_current'),('Backlog & Risks','A45:H48','risks_overflow'),
           ('Requirements List','A4:K7','requirements_fr'),('Requirements List','A48:K51','requirements_nfr'),('Requirements List','B63:D63','requirements_totals'),
           ('Iteration Plan','A4:H10','iterations_current'),('AI Usage Log','A8:H11','ai_current')]
    for name,value in [('updates',UPDATES),('layout',LAYOUT),('views',[dict(sheet=s,range=r,name=n) for s,r,n in views])]:
        (BASE/f'notes/P1_workbook_{name}.json').write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Prepared',len(UPDATES),'cell updates across',len({u['sheet'] for u in UPDATES}),'sheets.')


if __name__ == '__main__':
    import sys
    build() if 'build' in sys.argv else discover()
