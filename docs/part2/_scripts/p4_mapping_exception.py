"""Apply the owner's narrow A2 mapping exception. Author: 722I0004 · AI-assisted (Codex)."""
from pathlib import Path
import csv, hashlib, json, shutil, sys, tempfile
from datetime import datetime, timezone

R = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R))
N = R.parent / 'Part2/notes'
M = R / 'docs/part2/design/class_table_mapping.csv'
S = N / 'P4_start_snapshots/SaigonBite/docs/part2/design/class_table_mapping.csv'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(M) == sha(S) == 'b9968ebfdc503cbff9957d1d1e2bea0863be1720b3773c25e27f3c4ec34ca4bc'
receipt = N / 'P4_A2_mapping_exception.json'
assert not receipt.exists()
prior = N / 'P4_final_receipt.json'
archive = N / 'P4-root/blocked_entry_final_receipt_c615a80.json'
assert not archive.exists()
shutil.copyfile(prior, archive)
with M.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
row = next(r for r in rows if r['class'] == 'UserAccount' and r['attribute'] == 'created_at')
row.update(mapping_kind='field', column='created_at', sql_type='TEXT', nullability='NO (NOT NULL)',
    meaning='P4 CURRENT-SCHEMA MAPPING under owner-authorized A2 exception, 26 October 2026. '
    'UTC creation timestamp; supplied value or SQLite UTC creation default. '
    'Historical C0 GAP remains in c0_status; original mapping snapshot SHA256 ' + sha(S))
with M.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# Isolated postcondition check, independent of the still-broken pytest conftest.
from init_db import build_database
from saigonbite.data_access import connect, UserDAO
from saigonbite.business.domain import UserAccount, Role
scratch = N / 'P4_test_scratch'
with tempfile.TemporaryDirectory(prefix='created_at_', dir=scratch) as tmp:
    p = Path(tmp) / 'fresh.db'
    build_database(str(p))
    conn = connect(str(p)); dao = UserDAO(conn)
    assert datetime.fromisoformat(dao.get_by_id(1).created_at).utcoffset().total_seconds() == 0
    stamp = '2026-10-26T03:00:00+00:00'
    uid = dao.insert(UserAccount(0, 'new-created', 'synthetic-hash', 'New', Role.MANAGER, created_at=stamp))
    assert dao.get_by_id(uid).created_at == stamp
    uid = dao.insert(UserAccount(0, 'default-created', 'synthetic-hash', 'New', Role.MANAGER))
    assert datetime.fromisoformat(dao.get_by_id(uid).created_at).utcoffset().total_seconds() == 0
    assert conn.execute('PRAGMA user_version').fetchone()[0] == 2
    conn.close()
receipt.write_text(json.dumps(dict(author='722I0004 · AI-assisted (Codex)',
    at_utc=datetime.now(timezone.utc).isoformat(), owner_authorization=
    'Owner permits A2 exception: update only class_table_mapping.csv to P4 schema, first created_at; '
    'preserve P3 snapshot/hash/G3 evidence; checker unchanged; continue P4.1-P4.9 without reapproval.',
    original_sha256=sha(S), snapshot=str(S), p4_mapping_sha256=sha(M),
    standalone_checks='seed timestamp/default timestamp/explicit UTC timestamp round trips; schema v2',
    standalone_result='PASS', prior_receipt_archive=str(archive)), indent=2), encoding='utf-8')
print(receipt.read_text(encoding='utf-8'))
