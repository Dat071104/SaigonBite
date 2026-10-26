"""One-time P4.7 schema/mapping update under the owner's A2 exception.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import csv, hashlib, io, json
R=Path(__file__).resolve().parents[3]
N=R.parent/'Part2/notes'
mapping=R/'docs/part2/design/class_table_mapping.csv'
snapshot=N/'P4_start_snapshots/class_table_mapping_before_P4_7.csv'
assert not snapshot.exists()
original=mapping.read_bytes(); snapshot.write_bytes(original)
schema=R/'db/schema.sql'; text=schema.read_text(encoding='utf-8')
old="(customer_type = 'TOURIST' AND passport_no IS NOT NULL AND email IS NOT NULL)"
new="(customer_type = 'TOURIST' AND passport_no IS NOT NULL AND email IS NOT NULL AND nationality IS NOT NULL AND length(trim(nationality)) >= 2)"
assert text.count(old)==1
text=text.replace(old,new)
triggers="""
-- P4: profile ownership is a CUSTOMER account, in both update directions.
CREATE TRIGGER customer_role_insert BEFORE INSERT ON customer
WHEN NOT EXISTS (SELECT 1 FROM user_account WHERE id=NEW.user_id AND role='CUSTOMER')
BEGIN SELECT RAISE(ABORT, 'A customer profile requires a CUSTOMER account'); END;
CREATE TRIGGER customer_role_update BEFORE UPDATE OF user_id ON customer
WHEN NOT EXISTS (SELECT 1 FROM user_account WHERE id=NEW.user_id AND role='CUSTOMER')
BEGIN SELECT RAISE(ABORT, 'A customer profile requires a CUSTOMER account'); END;
CREATE TRIGGER linked_customer_role BEFORE UPDATE OF role ON user_account
WHEN NEW.role != 'CUSTOMER' AND EXISTS (SELECT 1 FROM customer WHERE user_id=OLD.id)
BEGIN SELECT RAISE(ABORT, 'A linked customer account must keep its CUSTOMER role'); END;

"""
text=text.replace('CREATE TABLE address (',triggers+'CREATE TABLE address (')
schema.write_text(text,encoding='utf-8')
reader=csv.DictReader(io.StringIO(original.decode('utf-8-sig'))); rows=list(reader)
for row in rows:
    if row['class']=='Customer':
        row['check']=row['check'].replace(old,new)
        if row['attribute']=='nationality':
            row['check']="(customer_type = 'LOCAL' AND phone IS NOT NULL)\n        OR "+new
            row['meaning']='P4 CURRENT-SCHEMA MAPPING: Tourist nationality is required by the table CHECK and controller validation. Historical P3 classification is retained.'
        if row['attribute']=='user_id':
            row['meaning']='P4 CURRENT-SCHEMA MAPPING: FK + UNIQUE permits one profile per account; insert/update triggers require CUSTOMER role and a reverse role-update trigger preserves it. Historical P3 classification is retained.'
buffer=io.StringIO(newline=''); w=csv.DictWriter(buffer,fieldnames=reader.fieldnames);w.writeheader();w.writerows(rows)
mapping.write_text(buffer.getvalue(),encoding='utf-8',newline='')
receipt={'authority':'Owner A2 mapping exception; current P4 schema only; original G3 evidence unchanged',
         'before_snapshot':str(snapshot),'before_sha256':hashlib.sha256(original).hexdigest(),
         'after_sha256':hashlib.sha256(mapping.read_bytes()).hexdigest()}
(N/'P4_A2_mapping_P4_7.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(receipt)
