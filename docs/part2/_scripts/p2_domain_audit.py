"""Record the final drawn-attribute/schema mapping after root's narrow revision."""
from pathlib import Path
import hashlib
import json
import re
import sqlite3

ROOT=Path(r'D:\RAD\FINAL'); REPO=ROOT/'SaigonBite'; OUT=ROOT/'Part2/notes/P2-root'
def main():
    path=REPO/'models/shared/domain_model.json'; model=json.loads(path.read_text(encoding='utf-8'))
    mapping={'Hub':'hub','Brand':'brand','MenuItem':'menu_item','HubMenuItem':'hub_menu_item','UserAccount':'user_account','Customer':'customer','Address':'address','Voucher':'voucher','Order':'orders','OrderLine':'order_line','Payment':'payment','Delivery':'delivery','ReplacementOffer':'replacement_offer','LocalCustomer':'customer','TouristCustomer':'customer'}
    conn=sqlite3.connect(':memory:'); conn.executescript((REPO/'db/schema.sql').read_text(encoding='utf-8'))
    found={}; missing=[]
    for page in model['parts']:
        for node in page['nodes']:
            if node['kind']!='class': continue
            name=node['id']; assert name in mapping
            attrs=[x.split(':',1)[0].strip() for x in node['attrs']]
            assert not any(a.endswith('_id') for a in attrs),(name,'FK attribute')
            columns={r[1] for r in conn.execute('PRAGMA table_info('+mapping[name]+')')}
            gaps=sorted(set(attrs)-columns)
            missing += [(name,a) for a in gaps]
            found[name]={'table':mapping[name],'drawn_attributes':attrs,'missing_columns':gaps}
    conn.close(); assert set(found)==set(mapping)
    assert missing==[('UserAccount','created_at')],missing
    out={'label':'Static mapping only; transient in-memory schema, no app database touched','class_count':13,'subclass_count':2,'classes':found,'missing_drawn_columns':missing,'withdrawal_reason_not_required':True,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (OUT/'domain_model_final_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print('Final domain: 13 persistent base classes + 2 subtypes; no FK attributes; only missing drawn SQL column is UserAccount.created_at (P4 input).')

if __name__=='__main__': main()
