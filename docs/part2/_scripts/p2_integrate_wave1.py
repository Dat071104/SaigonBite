"""Root reconciliation after every Wave 1 report was received."""
from pathlib import Path
import json
import re

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; DOC=REPO/'docs/part2'
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'

def main():
    p=DOC/'report/II_2-1_team_analysis.md'; t=p.read_text(encoding='utf-8')
    t=t.replace('# 2.1 Translate from Business Use Cases — Team Analysis','# 2.1 Translate from Business Use Case')
    titles={'System narrative':'System Narrative','Users and their goals':'Users and Their Goals','List of events':'List of Events','List of actors':'List of Actors','List of use cases and ownership':'List of Use Cases and Ownership'}
    for a,b in titles.items(): t=t.replace(a,b)
    t=t.replace('The 12 lifecycle rows use the exact operation names in plan §4 and are typed **State** because the listed event is the resulting domain transition; the actor command is its trigger. A temporal condition is evaluated only when a relevant request is made. No scheduler or database actor is assumed.',
                'The 12 lifecycle rows use the exact operation names in plan §4. They are **External** events because an actor command triggers each change; the new state is the response, not an autonomous state-event handler. Voucher date boundaries are temporal conditions checked on demand. No scheduler, independent state-event handler or database actor is assumed.')
    t=t.replace('| State |','| External |')
    t=t.replace('Customer chooses ONLINE and the simulator returns decline before checkout. | Payment simulator',
                'Customer previously chooses the simulated decline outcome; confirmCheckout evaluates that deterministic decision before persistence. | Customer; Payment simulator')
    t=t.replace('uses COD or an approved simulator result; current quote and capacity still pass.',
                'chooses COD or ONLINE; the deterministic simulator decision and all guards are evaluated within checkout before persistence.')
    t=t.replace('If the simulator approves and the accepted quote still matches, checkout records',
                'The customer chooses approve/decline before the transaction; its short deterministic decision and all writes occur inside checkout. A failure through COMMIT releases simulated authorization and saves nothing (BR-14). If the simulator approves and the accepted quote still matches, checkout records')
    p.write_text(t,encoding='utf-8')
    # A display result does not silently become a new persistent field.
    p=REPO/'models/shared/domain_model.py'; t=p.read_text(encoding='utf-8').replace(", 'withdrawal_reason: String?'",'').replace(",'withdrawal_reason: String?'",''); p.write_text(t,encoding='utf-8')
    p=DOC/'report/II_2-1-6_2-1-7_models.md'; t=p.read_text(encoding='utf-8')
    t=t.replace('; model `withdrawal_reason`','')
    t=t.replace('**No column/dataclass field retains the invalid-target withdrawal reason required by plan §3.3(5).**',
                'The invalid-target withdrawal reason is a displayed operation result under §3.3(5); no new persistent reason field is required by this analysis.')
    t=t.replace('Preserve invalid-target withdrawal reason. The diagram uses optional `withdrawal_reason` as the conservative representation of the plan\'s “WITHDRAWN with reason” result; the draft has no equivalent storage. P3/P4 must confirm the final field/API mapping before implementation.',
                'Return the invalid-target withdrawal reason with the operation result. Root rejected an extra persistent withdrawal_reason attribute: §3.3(5) requires a reason to be shown, and does not require new reason-history storage. P3 confirms the result/API mapping; the diagram adds no column.')
    p.write_text(t,encoding='utf-8')
    # Qualify only existing scope, never grant generic record edit/delete access.
    actors=['Customer','Kitchen staff','Shipper','Admin','Manager']; classes=['Hub','Brand','MenuItem','HubMenuItem','UserAccount','Customer','Address','Voucher','Order','OrderLine','Payment','Delivery','ReplacementOffer']
    data={a:{} for a in actors}
    def put(a,c,C='',R='',U='',D=''):
        data[a][c]={k:set(v.split('; ')) if v else set() for k,v in zip('CRUD',[C,R,U,D])}
    put('Customer','UserAccount','SUC-02','SUC-01; SUC-02','SUC-02')
    put('Customer','Customer','SUC-02','SUC-02; SUC-03','SUC-02')
    put('Customer','Address','SUC-02','SUC-02; UC-01','SUC-02','SUC-02')
    put('Customer','Order','UC-01','SUC-03','SUC-03; SUC-04')
    put('Customer','OrderLine','UC-01','SUC-03','SUC-03')
    put('Customer','Payment','UC-01','SUC-03','SUC-03; SUC-04')
    put('Customer','ReplacementOffer','','SUC-03','SUC-03; SUC-04')
    put('Customer','Delivery','','SUC-03')
    for c in ['Hub','Brand','MenuItem','HubMenuItem','Voucher']: put('Customer',c,R='UC-01')
    put('Kitchen staff','UserAccount',R='SUC-01')
    put('Kitchen staff','Order',R='UC-05; SUC-05',U='UC-05; SUC-05')
    put('Kitchen staff','OrderLine',R='UC-05'); put('Kitchen staff','MenuItem',R='UC-05')
    put('Kitchen staff','ReplacementOffer',C='UC-05',R='UC-05',U='UC-05')
    put('Kitchen staff','HubMenuItem',R='UC-05; SUC-06',U='SUC-06')
    put('Kitchen staff','Delivery',C='SUC-05'); put('Kitchen staff','Payment',U='UC-05')
    put('Shipper','UserAccount',R='SUC-01'); put('Shipper','Delivery',R='UC-02',U='UC-02')
    put('Shipper','Order',R='UC-02',U='UC-02'); put('Shipper','Payment',R='UC-02',U='UC-02')
    put('Shipper','Customer',R='UC-02'); put('Shipper','Address',R='UC-02')
    put('Admin','Hub',C='UC-03',R='UC-03',U='UC-03',D='UC-03')
    for c in ['Brand','MenuItem','HubMenuItem']: put('Admin',c,C='UC-06',R='UC-06',U='UC-06',D='UC-06')
    put('Admin','Voucher',C='SUC-07',R='SUC-07',U='SUC-07',D='SUC-07')
    put('Admin','UserAccount',C='SUC-08',R='SUC-01; SUC-08',U='SUC-08',D='SUC-08')
    put('Admin','Customer',R='SUC-08',D='SUC-08')
    for c in ['Order','OrderLine','Payment','Delivery','ReplacementOffer']: put('Admin',c,R='SUC-09',D='SUC-09')
    put('Manager','UserAccount',R='SUC-01')
    for c in ['Order','OrderLine','Payment','Delivery','Hub']: put('Manager',c,R='UC-04')
    union={c:{v:set() for v in 'CRUD'} for c in classes}
    for a,cs in data.items():
        for c,verbs in cs.items():
            for v,refs in verbs.items(): union[c][v]|=refs
    plan=(ROOT/'PLAN_SaigonBite_Part2_Final.md').read_text(encoding='utf-8')
    plan_union={}
    table=plan.split('### 2.4 CRUD union',1)[1].split('Not persisted:',1)[0]
    for line in table.splitlines():
        fields=[s.strip() for s in line.strip('|').split('|')]
        if len(fields)!=5 or fields[0].split(' (')[0] not in classes: continue
        c=fields[0].split(' (')[0]; plan_union[c]={v:set(re.findall(r'(?<![A-Z])(?:SUC|UC)-\d\d',x)) for v,x in zip('CRUD',fields[1:])}
    missing=[]; added=[]
    for c in classes:
        for v in 'CRUD':
            missing += [(c,v,x) for x in plan_union[c][v]-union[c][v]]
            added += [(c,v,x) for x in union[c][v]-plan_union[c][v]]
    assert not missing,missing
    assert all(v=='R' for _,v,_ in added),added
    intro=f'''# 2.3 Verifying Use Cases for Actor (CRUD)\n\n{AUTHOR}\n\nThese five actor tables implement the locked portfolio under the narrow root reconciliations below. The plan is unchanged. Cells name observable UC/SUC paths, not generic database privileges. An intentional blank grants no operation. All behavior remains an analysis contract; no running CRUD result is claimed before P4.\n\nScope restrictions apply to every cell: Customer reads/changes own records only; Kitchen staff work only at their hub (BR-26); Shipper sees delivery contact/address snapshots and payment method/state/cash due only (BR-12/25), never passport details; Admin reads authorized account/history data. UserAccount Read SUC-01 in each actor table means own authentication/role context only, with credential verification internal: it grants neither an account-list endpoint nor access to password hashes. Address UC-02 is the saved Order address snapshot, not permission to edit or browse live addresses.\n\n'''
    sections=[]
    for i,a in enumerate(actors,1):
        lines=[f'## 2.3.{i} Verifying use cases for {a}','',AUTHOR,'','| Data entity / domain class | C R U D | Verified use case |','|---|---|---|']
        for c in classes:
            if c not in data[a]: continue
            for j,(v,label) in enumerate(zip('CRUD',['Create','Read / report','Update','Delete (or archive)'])):
                refs='; '.join(sorted(data[a][c][v])) or '— (intentional blank)'
                lines.append(f"| {c if j==0 else ''} | {label} | {refs} |")
        sections.append('\n'.join(lines))
    lines=['## Union and bidirectional verification','',AUTHOR,'',
           'Every original §2.4 qualified C/R/U/D cell is held by at least one actor above. Every actor cell is in the reconciled union below. Literal omissions in the locked tables are retained as explicit plan issues, rather than claimed to be exact original equality. The six missing qualified reads found by D and the reverse-direction omissions are resolved only within existing UC/SUC scope.','',
           '| Persistent class | C | R | U | D / archive | Actors holding cells |','|---|---|---|---|---|---|']
    for c in classes:
        values=['; '.join(sorted(union[c][v])) for v in 'CRUD']; assert all(values)
        holders='; '.join(a for a in actors if c in data[a])
        lines.append('| '+c+' | '+' | '.join(values)+' | '+holders+' |')
    lines += ['', '| Comparison | Result |','|---|---|','| Original §2.4 → reconciled actor tables | 0 missing qualified cells |','| Reconciled actor tables → reconciled union | 0 missing qualified cells (union derived from those tables) |','| Additional cells against literal §2.4 | Read-only cells listed below; no new create/update/archive grants |','| Persistent classes / schema tables | 13 / 13; mapping below |', '',
              '### Root dispositions for literal plan differences','',
              '| Discrepancy | Accepted conservative reconciliation |','|---|---|',
              '| UserAccount R SUC-01 lacks an actor assignment in §2.5 | Own authentication-context read for all five human actors, already the All actor scope of SUC-01; no general account read permission. |',
              '| Customer R SUC-03; Address R UC-01 lack matching own-read actor qualifiers | Add only the owning Customer read while tracking / selecting their checkout address. |',
              '| MenuItem R UC-05; HubMenuItem R UC-05 / SUC-06 lack kitchen qualifiers | Read only own-hub replacement candidates/listings; no master-data update. |',
              '| Payment R UC-02 lacks shipper read cell | Read method/state/cash due for delivery under BR-25, without other customer-private data. |',
              '| Admin Customer R is unqualified and absent from §2.4 | Qualify already listed authorized linked-account read as SUC-08. |',
              '| Admin Order/children history R SUC-09 absent from §2.4 | Retain the reads already stated in §2.5 and §2.2 SUC-09, through authorized closed-order history only. |',
              '| Kitchen Order R SUC-05 stated in §2.5 but omitted from §2.4 | Retain the own-hub read required to start/finish preparation; this reverse-direction omission was added by root. |',
              '', 'Added Read qualifiers against literal §2.4: '+ '; '.join(f'{c} R {x}' for c,_,x in added)+'.',
              '', 'No locked plan cell was removed. Proposed owner clarification: add these qualifiers to the next approved plan revision; this phase records the discrepancy without editing the locked contract.',
              '', '## Archive and persistence notes','',
              'An archived parent hides itself and its children from operational lists (boards, menus and checkout). Authorised history, receipts, reports and refund obligations still include them. Archive is an operational visibility rule, not physical child deletion or permission to erase snapshots. SUC-09 accepts only DELIVERED, DELIVERY_FAILED, REJECTED or CANCELLED orders. Customer deactivation is through the linked UserAccount; it does not erase the profile. HubMenuItem unlisting removes only that association row, and historical OrderLine snapshots survive. Seed rows are test setup, never a “Create”.',
              '', 'Not persisted: Quote, ReportFilter, report rows and receipt (computed views). No Shipper class/table: SHIPPER is a UserAccount role linked from Delivery.',
              '', '## Schema table coverage (Static)','', '| SQL table | Persistent class |','|---|---|']
    tables=['hub','brand','menu_item','hub_menu_item','user_account','customer','address','voucher','orders','order_line','payment','delivery','replacement_offer']
    for c,s in zip(classes,tables): lines.append(f'| `{s}` | {c} |')
    lines += ['', 'All 13 schema tables are covered. Local/Tourist share Customer persistence. State/attribute differences and behavioral guards remain explicitly listed as P4 inputs; this table-coverage result does not qualify the app.']
    (DOC/'report/II_2-3_crud.md').write_text(intro+'\n\n'.join(sections)+'\n\n'+'\n'.join(lines)+'\n',encoding='utf-8')
    payload={'actors':actors,'classes':classes,'actor_cells':{a:{c:{v:sorted(refs) for v,refs in verbs.items()} for c,verbs in cs.items()} for a,cs in data.items()},'union':{c:{v:sorted(refs) for v,refs in verbs.items()} for c,verbs in union.items()},'original_plan_cells_missing':missing,'read_qualifiers_added':added,'write_privileges_added':[]}
    (ROOT/'Part2/notes/P2-root/crud_reconciliation.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    p=DOC/'SUC.md'; t=p.read_text(encoding='utf-8')
    t=t.replace('UserAccount — Create/Update; Customer','UserAccount — Create/Read/Update; Customer')
    t=t.replace('Order — Read own; OrderLine','Customer — Read own contact under SUC-03; Order — Read/Update own on an answer; OrderLine')
    t=t.replace('Order — Update to PREPARING/READY; Delivery','Order — Read/Update own-hub to PREPARING/READY; Delivery')
    t=t.replace('Customer — Read through the linked account only (SUC-08).','Customer — Read and deactivate through the linked account only (SUC-08); the profile is preserved.')
    p.write_text(t,encoding='utf-8')
    print('Root Wave 1 reconciliation:',len(added),'Read qualifiers; zero missing original plan cells; no new write privileges.')

if __name__=='__main__': main()
