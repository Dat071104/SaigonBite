"""Final semantic/boundary and meaningful security regressions.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import importlib.util,json,sqlite3
import pytest
from saigonbite.business.controllers import AccountController,UserAdminController,KitchenController,OrderTrackingController,ValidationError
from saigonbite.data_access import connect, immediate_transaction
from .test_p4_foundation import facts
from .test_p4_accounts import registration
from .p4_helpers import place
from .conftest import login

R=Path(__file__).resolve().parents[1]


def load(name):
    spec=importlib.util.spec_from_file_location(name,R/f'docs/part2/_scripts/{name}.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def test_semantic_exact_tokens_reject_historical_nonempty_wrong_links():
    module=load('p4_traceability');rows,audit,negative=module.build()
    assert len(rows)==len(audit)==52 and len(negative)==3 and all(n['rejected'] for n in negative)
    assert module.tokens('SUC02-PC01; UC02-PC01')=={'SUC02-PC01','UC02-PC01'}
    assert module.tokens('UC02-PC010; XUC02-PC01')==set()
    assert rows[0]['code method']=='AccountController.register'
    assert 'no standalone main-UC diagram' in rows[0]['design operation']
    assert next(r for r in rows if r['Req ID']=='NFR-09')['status']=='Planned'


def test_architecture_inventory_is_truthful_and_domain_views_respect_io_boundary():
    records,io,sql=load('p4_architecture_audit').inventory()
    assert io==sql==[]
    assert not [r for r in records if r['source'].startswith('saigonbite.business.domain') and not r['target'].startswith('saigonbite.business.domain')]
    assert not [r for r in records if r['source'].startswith('saigonbite.presentation') and (r['target'].startswith('saigonbite.data_access') or r['target'].startswith('saigonbite.business.domain') or r['target']=='saigonbite')]
    unresolved={(r['source'],r['target']) for r in records if r['source'].startswith('saigonbite.data_access') and r['target'].startswith('saigonbite.business.domain')}
    assert len(unresolved)==12  # Known blocker, explicitly not an architecture PASS.


def test_sql_injection_does_not_authenticate_and_stored_html_is_escaped(client,db_path):
    before=facts(db_path)
    assert client.post('/login',data={'username':"customer' OR 1=1 --",'password':'wrong'}).status_code==401
    assert facts(db_path)==before
    login(client,'admin');payload='<script>window.P4_SENTINEL=1</script>'
    assert client.post('/admin/brands',data={'name':payload}).status_code==303
    page=client.get('/admin/menu')
    assert page.status_code==200 and payload.encode() not in page.data and b'&lt;script&gt;window.P4_SENTINEL=1&lt;/script&gt;' in page.data
    conn=connect(db_path)
    assert conn.execute('SELECT name FROM brand WHERE name=?',(payload,)).fetchone()[0]==payload
    assert conn.execute('SELECT COUNT(*) FROM user_account').fetchone()[0]==len(before['user_account']);conn.close()


@pytest.mark.parametrize('field,value',[('role','ADMIN'),('username','another')])
def test_immutable_staff_identity_forgery_refused_without_other_edits(db_path,field,value):
    conn=connect(db_path);before=facts(db_path)
    with pytest.raises(ValidationError):UserAdminController(conn).update_user(4,3,{'display_name':'Changed Name',field:value})
    assert facts(db_path)==before;conn.close()


def test_registered_subtype_forgery_cannot_alter_profile(db_path):
    conn=connect(db_path);before=facts(db_path)
    with pytest.raises(ValidationError):AccountController(conn).update_profile(1,registration('TOURIST'))
    assert facts(db_path)==before;conn.close()


def test_main_kitchen_confirm_and_reject_have_exact_durable_effects(db_path):
    conn=connect(db_path);o=place(conn).order;k=KitchenController(conn)
    k.confirm_order(2,o.id)
    row=conn.execute('SELECT state,confirmed_at FROM orders WHERE id=?',(o.id,)).fetchone()
    assert row['state']=='CONFIRMED' and row['confirmed_at']
    o=place(conn).order  # Rejection is a PLACED alternative, never CONFIRMED -> REJECTED.
    k.reject_order(2,o.id,'Synthetic refusal')
    row=conn.execute('SELECT state,reject_reason,closed_at FROM orders WHERE id=?',(o.id,)).fetchone()
    assert row['state']=='REJECTED' and row['reject_reason']=='Synthetic refusal' and row['closed_at']
    assert conn.execute('SELECT state FROM payment WHERE order_id=?',(o.id,)).fetchone()[0]=='VOIDED'
    conn.close()


def test_failed_rollback_discards_connection_and_preserves_original_error(db_path):
    class BrokenRollback(sqlite3.Connection):
        def rollback(self):raise sqlite3.OperationalError('rollback failed')
    before=facts(db_path);conn=sqlite3.connect(db_path,isolation_level=None,factory=BrokenRollback)
    with pytest.raises(RuntimeError,match='original body error'):
        with immediate_transaction(conn):
            conn.execute("UPDATE hub SET name='Must rollback' WHERE id=1")
            raise RuntimeError('original body error')
    with pytest.raises(sqlite3.ProgrammingError,match='closed'):conn.execute('SELECT 1')
    assert facts(db_path)==before
