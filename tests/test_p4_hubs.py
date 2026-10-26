"""UC03-PC01/02/MG01 and shared transaction guards. Author: 722I0004 · AI-assisted (Codex)."""
import pytest
from saigonbite.business.controllers import HubController, PlaceOrderController, ConflictError, ValidationError, HubUnavailableError
from saigonbite.data_access import connect
from .test_p4_foundation import facts, FaultConnection
from .conftest import login
from .p4_helpers import place
import sqlite3

FORM=dict(code='HUB-NEW',name='New kitchen',address_text='Test street',latitude='10.78',longitude='106.7',
          max_active_orders='4',base_delivery_fee='12000')

def test_admin_real_crud_and_archived_history(client,db_path):
    login(client,'admin')
    assert client.post('/admin/hubs/new',data=FORM).status_code==303
    conn=connect(db_path); c=HubController(conn)
    hub=next(x.status.hub for x in c.list_hubs(4) if x.status.hub.code=='HUB-NEW')
    assert client.get(f'/admin/hubs/{hub.id}').status_code==200
    assert client.post(f'/admin/hubs/{hub.id}',data={**FORM,'name':'Renamed kitchen'}).status_code==303
    assert c.get_hub(4,hub.id).status.hub.name=='Renamed kitchen'
    assert client.post(f'/admin/hubs/{hub.id}/archive').status_code==303
    assert hub.id in {x.status.hub.id for x in c.list_hubs(4)}
    assert hub.id not in {x.status.hub.id for x in c.list_hubs(4,False)}
    assert hub.id in {x.status.hub.id for x in c.list_hubs(4,True)}
    assert hub.id not in {x.hub.id for x in PlaceOrderController(conn).list_hubs()}
    assert 'Renamed kitchen' not in client.get('/admin/hubs?includeArchived=false').get_data(as_text=True)
    assert 'Renamed kitchen' in client.get('/admin/hubs?includeArchived=true').get_data(as_text=True)
    for change in ({'code':'HUB-NEW'},{'name':'Renamed kitchen'}):
        with pytest.raises(ValidationError): c.create_hub(4,{**FORM,'code':'HUB-ALT','name':'Other',**change})
    conn.close()

@pytest.mark.parametrize('field,value',[('max_active_orders','0'),('max_active_orders','-1'),('max_active_orders','1.5'),
    ('latitude','nan'),('latitude','91'),('longitude','inf'),('base_delivery_fee','-1'),('code','bad'),('name','')])
def test_invalid_fields_and_duplicate_code_change_nothing(db_path,field,value):
    conn=connect(db_path);before=facts(db_path)
    with pytest.raises(ValidationError): HubController(conn).create_hub(4,{**FORM,field:value})
    assert facts(db_path)==before
    with pytest.raises(ValidationError): HubController(conn).create_hub(4,{**FORM,'code':'HUB-D1'})
    assert facts(db_path)==before
    conn.close()

@pytest.mark.parametrize('state',['PLACED','CONFIRMED','PREPARING','READY','OUT_FOR_DELIVERY'])
def test_every_open_state_blocks_archive(db_path,state):
    conn=connect(db_path);o=place(conn).order
    conn.execute('UPDATE orders SET state=? WHERE id=?',(state,o.id))
    before=facts(db_path)
    with pytest.raises(ConflictError): HubController(conn).archive_hub(4,1)
    assert facts(db_path)==before
    conn.close()

def test_lower_capacity_below_load_then_checkout_refused(db_path):
    conn=connect(db_path);place(conn);place(conn)
    HubController(conn).update_hub(4,1,{**FORM,'code':'HUB-D1','name':'SaigonBite District 1 Hub','max_active_orders':'1'})
    assert conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==2
    with pytest.raises(HubUnavailableError): place(conn)
    assert conn.execute('SELECT COUNT(*) FROM orders').fetchone()[0]==2
    conn.close()

@pytest.mark.parametrize('action',['update','archive'])
def test_stale_conditional_save_rolls_back(db_path,monkeypatch,action):
    conn=connect(db_path);c=HubController(conn);before=facts(db_path)
    monkeypatch.setattr(c.hubs,action,lambda *a:False)
    with pytest.raises(ConflictError):
        c.update_hub(4,1,{**FORM,'code':'HUB-D1'}) if action=='update' else c.archive_hub(4,1)
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()

@pytest.mark.parametrize('action',['create','update','archive'])
def test_hub_commit_failure_no_partial_save(db_path,action):
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    conn.fault='COMMIT';c=HubController(conn);before=facts(db_path)
    with pytest.raises(sqlite3.OperationalError,match='injected COMMIT'):
        if action=='create':c.create_hub(4,FORM)
        elif action=='update':c.update_hub(4,1,{**FORM,'code':'HUB-D1'})
        else:c.archive_hub(4,1)
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()
