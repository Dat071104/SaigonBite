"""P4.1 postconditions. Author: 722I0004 · AI-assisted (Codex)."""
from pathlib import Path
from datetime import datetime
import hashlib
import sqlite3
import pytest
from flask.testing import FlaskClient
from init_db import main, build_database
from saigonbite import create_app
from saigonbite.data_access import connect, immediate_transaction, UserDAO
from saigonbite.business.domain import Role, UserAccount
from .conftest import new_connection, login


def facts(db_path):
    with new_connection(db_path) as conn:
        return {r[0]: [tuple(x) for x in conn.execute('SELECT * FROM '+r[0]+' ORDER BY rowid')]
                for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}


@pytest.mark.parametrize('version',[0,1,2,3,999])
def test_migration_refusal_is_read_only(tmp_path,version,capsys):
    p=(tmp_path/'disposable_version.db').resolve()
    assert p.is_relative_to(tmp_path.resolve())
    conn=sqlite3.connect(p)
    conn.executescript(f'CREATE TABLE preserved(value TEXT); INSERT INTO preserved VALUES ("keep"); PRAGMA user_version={version};')
    conn.close()
    before=hashlib.sha256(p.read_bytes()).hexdigest()
    assert main(['--db',str(p),'--migrate']) == (0 if version==2 else 1)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==before
    if version!=2:
        assert 'fresh v2' in capsys.readouterr().err


def test_missing_migration_path_never_creates_file(tmp_path):
    p=tmp_path/'missing.db'
    assert main(['--db',str(p),'--migrate'])==1
    assert not p.exists()


def test_created_at_and_connection_policy(db_path):
    conn=connect(db_path)
    assert conn.execute('PRAGMA foreign_keys').fetchone()[0]==1
    assert conn.execute('PRAGMA busy_timeout').fetchone()[0]==10000
    assert conn.execute('PRAGMA journal_mode').fetchone()[0]=='wal'
    assert conn.execute('PRAGMA synchronous').fetchone()[0]==1
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO hub_menu_item VALUES(999,999,1)")
    dao=UserDAO(conn)
    assert datetime.fromisoformat(dao.get_by_id(1).created_at).utcoffset().total_seconds()==0
    stamp='2026-10-26T00:01:00+00:00'
    uid=dao.insert(UserAccount(0,'utc-new','synthetic','UTC',Role.MANAGER,created_at=stamp))
    assert dao.get_by_id(uid).created_at==stamp
    uid=dao.insert(UserAccount(0,'utc-default','synthetic','UTC',Role.MANAGER))
    assert datetime.fromisoformat(dao.get_by_id(uid).created_at).utcoffset().total_seconds()==0
    conn.close()
    memory=connect(':memory:')
    assert memory.execute('PRAGMA journal_mode').fetchone()[0]=='memory'
    memory.close()


class FaultConnection(sqlite3.Connection):
    fault=None
    def execute(self,sql,*args,**kwargs):
        if sql==self.fault:
            raise sqlite3.OperationalError('injected '+sql)
        return super().execute(sql,*args,**kwargs)


@pytest.mark.parametrize('fault',['BEGIN IMMEDIATE','BODY','COMMIT'])
def test_transaction_failures_preserve_error_and_durable_state(db_path,fault):
    before=facts(db_path)
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection)
    conn.fault=fault
    with pytest.raises(sqlite3.OperationalError,match='injected '+fault):
        with immediate_transaction(conn):
            conn.execute("UPDATE hub SET name='changed' WHERE id=1")
            if fault=='BODY':
                raise sqlite3.OperationalError('injected BODY')
    assert not conn.in_transaction
    conn.close()
    assert facts(db_path)==before


def test_programming_error_is_not_hidden_and_rolls_back(db_path):
    before=facts(db_path)
    conn=connect(db_path)
    with pytest.raises(RuntimeError,match='programming error'):
        with immediate_transaction(conn):
            conn.execute("UPDATE hub SET name='changed'")
            raise RuntimeError('programming error')
    assert not conn.in_transaction
    conn.close()
    assert facts(db_path)==before


def test_real_second_connection_write_lock_is_controlled(app,db_path,monkeypatch):
    import saigonbite.presentation.db as db_module
    before=facts(db_path)
    holder=connect(db_path)
    holder.execute('BEGIN IMMEDIATE')
    original=db_module.connect
    def short_wait(path):
        conn=original(path)
        conn.execute('PRAGMA busy_timeout=25') # Bounded test wait; production default separately asserted.
        return conn
    monkeypatch.setattr(db_module,'connect',short_wait)
    try:
        client=app.test_client()
        login(client,'customer')
        response=client.post('/order/confirm',data=dict(hub_id=1,address_id=1,qty_1='1',idempotency_token='held',quoted_total='65000'))
        assert response.status_code==503 and 'retry' in response.get_data(as_text=True).lower()
        assert facts(db_path)==before
    finally:
        holder.rollback();holder.close()
    assert facts(db_path)==before


def test_production_requires_secret_and_secure_settings(monkeypatch,db_path):
    monkeypatch.setenv('SAIGONBITE_ENV','production')
    monkeypatch.delenv('SAIGONBITE_SECRET_KEY',raising=False)
    with pytest.raises(RuntimeError,match='SAIGONBITE_SECRET_KEY'):
        create_app({'TESTING':True,'DATABASE':db_path,'SECRET_KEY':'test-overrides-do-not-bypass'})
    monkeypatch.setenv('SAIGONBITE_SECRET_KEY','synthetic-production-test-key-'*3)
    monkeypatch.setenv('SAIGONBITE_HTTPS','0')
    app=create_app({'DATABASE':db_path})
    assert not app.debug
    assert app.config['SESSION_COOKIE_SECURE'] and app.config['SESSION_COOKIE_HTTPONLY']
    assert app.config['SESSION_COOKIE_SAMESITE']=='Lax'
    cookie=app.test_client().get('/login').headers.get('Set-Cookie','')
    assert 'Secure' in cookie and 'HttpOnly' in cookie and 'SameSite=Lax' in cookie


@pytest.mark.parametrize('token',[None,'wrong','nonascii-đ'])
def test_every_mutating_route_rejects_invalid_csrf_without_domain_writes(app,db_path,token):
    before=facts(db_path)
    # Raw Flask client deliberately does not use the valid-token convenience client.
    client=FlaskClient(app)
    for rule in app.url_map.iter_rules():
        if 'POST' not in rule.methods:
            continue
        path=rule.rule
        import re
        path=re.sub(r'<(?:int:)?[^>]+>','1',path)
        data={} if token is None else {'csrf_token':token}
        response=client.post(path,data=data)
        assert response.status_code==400,(rule.rule,response.status_code)
        assert facts(db_path)==before


def test_valid_csrf_is_session_bound_and_distinct_from_checkout(client,app,db_path):
    login(client,'customer')
    with client.session_transaction() as state:
        token=state['csrf_token']
    foreign=FlaskClient(app)
    assert foreign.post('/login',data={'username':'customer','password':'123456','csrf_token':token}).status_code==400
    assert client.post('/order/confirm',data={'hub_id':1,'address_id':1,'qty_1':'1',
        'quoted_total':65000,'csrf_token':'checkout-token','idempotency_token':token}).status_code==400
    assert facts(db_path)['orders']==[]
