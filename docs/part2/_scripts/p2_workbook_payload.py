"""Derive workbook input cells from versioned report II sources (no hand copy)."""
from pathlib import Path
import json
import re
import textwrap
import openpyxl

ROOT=Path(r'D:\RAD\FINAL'); DOC=ROOT/'SaigonBite/docs/part2'; BASE=ROOT/'Part2'
def clean(x): return x.strip().replace('`','').replace('**','')
def main():
    updates=[]; layout={}
    def cell(sheet,address,value): updates.append({'sheet':sheet,'cell':address,'value':value})
    team=(DOC/'report/II_2-1_team_analysis.md').read_text(encoding='utf-8')
    events=[]
    for line in team.split('## 2.1.3 ',1)[1].split('## 2.1.4 ',1)[0].splitlines():
        if re.match(r'^\| \d+ \|',line): events.append([clean(x) for x in line.strip('|').split('|')])
    assert 14<=len(events)<=20
    for i,row in enumerate(events,5):
        assert len(row)==8,row
        widths={'B':36,'C':16,'D':23,'E':22,'F':29,'G':23,'H':25}
        wrapped=[textwrap.fill(value,width=widths[col],break_long_words=False,break_on_hyphens=False) for col,value in zip('BCDEFGH',row[1:])]
        for col,value in zip('BCDEFGH',wrapped): cell('Events Table',f'{col}{i}',value)
        layout.setdefault('Events Table',{})[str(i)]=max(72,14+12*max(v.count('\n')+1 for v in wrapped))
    for i in range(5+len(events),25):
        for col in 'BCDEFGH': cell('Events Table',f'{col}{i}',None)
    crud=(DOC/'report/II_2-3_crud.md').read_text(encoding='utf-8')
    rows=[]
    for line in crud.split('| Persistent class | C | R | U | D / archive | Actors holding cells |',1)[1].split('### Root dispositions',1)[0].splitlines():
        parts=[clean(x) for x in line.strip('|').split('|')]
        if len(parts)==6 and parts[0] in ['Hub','Brand','MenuItem','HubMenuItem','UserAccount','Customer','Address','Voucher','Order','OrderLine','Payment','Delivery','ReplacementOffer']: rows.append(parts)
    assert len(rows)==13
    for i,row in enumerate(rows,5):
        c,C,R,U,D,actors=row
        wrapped=[textwrap.fill(value,width=24,break_long_words=False,break_on_hyphens=False) for value in [actors,c,C,R,U,D]]
        for col,value in zip('ABCDEF',wrapped): cell('CRUD Check',f'{col}{i}',value)
        layout.setdefault('CRUD Check',{})[str(i)]=max(58,14+12*max(v.count('\n')+1 for v in wrapped))
    for i in range(18,35):
        for col in 'ABCDEF': cell('CRUD Check',f'{col}{i}',None)
    # The six source names changed from older short labels to exact locked goals.
    mains=[]
    for line in team.split('## 2.1.5 ',1)[1].split('**Group coverage:**',1)[0].splitlines():
        if re.match(r'^\| UC-\d\d \|',line): mains.append([clean(x) for x in line.strip('|').split('|')])
    assert len(mains)==6
    for i,row in enumerate(mains,15):
        uc,name,actor,group,summary,owner,author=row
        for col,value in [('B',uc+' '+name),('C',actor),('D',group),('E',summary+' Actual Part 2 author: '+author+' (D-1/J2).'),('F',owner),('H','Analysed')]:
            if col in ('B','E'): value=textwrap.fill(value,width=29 if col=='B' else 42,break_long_words=False,break_on_hyphens=False)
            cell('Team & Use Cases',f'{col}{i}',value)
        layout.setdefault('Team & Use Cases',{})[str(i)]=112
    mapping=[(9,'E',0),(9,'F',2),(10,'E',1),(10,'F',3),(11,'E',4),(11,'F',5)]
    for row,col,idx in mapping:
        value=mains[idx][0]+' '+mains[idx][1]
        cell('Team & Use Cases',f'{col}{row}',textwrap.fill(value,width=42 if col=='E' else 13,break_long_words=False,break_on_hyphens=False))
    for row,value in {
        9:'Proposal role: ordering, hub management and integration. Actual author of all Part 2 artifacts: 722I0004 (D-1/J2).',
        10:'Proposal role: delivery and reporting; proposal owner of UC-02/04. No Part 2 artifact authorship claimed for this member (D-1/J2).',
        11:'Proposal role: kitchen and catalogue; proposal owner of UC-05/06. No Part 2 artifact authorship claimed for this member (D-1/J2).'
    }.items(): cell('Team & Use Cases',f'D{row}',textwrap.fill(value,width=42,break_long_words=False,break_on_hyphens=False))
    layout['Team & Use Cases'].update({'9':150,'10':150,'11':150})
    original=openpyxl.load_workbook(BASE/'notes/P2-root/workbook_before.xlsx',data_only=False)
    formulas=[{'sheet':s.title,'cell':c.coordinate,'formula':c.value} for s in original for row in s for c in row if c.data_type=='f']
    (BASE/'notes/P2_workbook_formulas.json').write_text(json.dumps(formulas,indent=2),encoding='utf-8')
    wrapping=[{'sheet':s.title,'cell':c.coordinate} for s in original for row in s for c in row if c.alignment.wrapText]
    (BASE/'notes/P2_workbook_wrap.json').write_text(json.dumps(wrapping,indent=2),encoding='utf-8')
    # Do not rewrite any correctly retained P1 content; only wrong/outdated cells.
    updates=[u for u in updates if original[u['sheet']][u['cell']].value!=u['value']]
    for u in updates:
        c=original[u['sheet']][u['cell']]
        assert c.data_type!='f' and c.fill.fgColor.rgb!='FFDDF0DF',u
    (BASE/'notes/P2_workbook_updates.json').write_text(json.dumps(updates,indent=2,ensure_ascii=False),encoding='utf-8')
    (BASE/'notes/P2_workbook_layout.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
    print(json.dumps({'events':len(events),'crud_classes':len(rows),'updated_input_cells':len(updates),'sheets':sorted({u['sheet'] for u in updates})}))

if __name__=='__main__': main()
