"""Complete route/method × role matrix, valid CSRF and zero-mutation denials.
Author: 722I0004 · AI-assisted (Codex).
"""
import json,re
from pathlib import Path
import pytest
from saigonbite.business.controllers import KitchenController,DeliveryController,OrderTrackingController,OrderArchiveController,PlaceOrderController
from saigonbite.data_access import connect
from saigonbite.business.domain import PaymentMethod
from .p4_helpers import place
from .test_p4_foundation import facts
from .test_p4_accounts import registration,voucher_form
from .test_p4_hubs import FORM

POLICY=json.loads((Path(__file__).parent/'fixtures/p4_route_policy.json').read_text())
ACTORS={'ANONYMOUS':None,'CUSTOMER':1,'KITCHEN_STAFF':2,'SHIPPER':3,'ADMIN':4,'MANAGER':5,'INACTIVE':1}


def test_inventory_detects_every_new_route_and_method(app):
    actual={(r.rule,m,r.endpoint) for r in app.url_map.iter_rules() if r.endpoint!='static' for m in r.methods-{'HEAD','OPTIONS'}}
    expected={(r['rule'],r['method'],r['endpoint']) for r in POLICY}
    assert actual==expected and len(POLICY)==len(expected)==78


def context(conn,case):
    endpoint=case['endpoint'];data={};o=place(conn).order
    k=KitchenController(conn)
    if endpoint in ('kitchen.offer','order.answer_replacement'):
        conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=1')
        data={'replacement':f'{o.lines[0].id}:2'}
        if endpoint=='order.answer_replacement':
            offer=k.offer_replacement(2,o.id,o.lines[0].id,2);data={'offer_id':offer.id,'decision':'accept'}
    if endpoint in ('kitchen.prepare','kitchen.ready') or endpoint.startswith('delivery.'):
        k.confirm_order(2,o.id)
    if endpoint=='kitchen.ready' or endpoint.startswith('delivery.'):k.start_preparing(2,o.id)
    if endpoint.startswith('delivery.'):
        k.mark_ready(2,o.id)
        if endpoint in ('delivery.delivered','delivery.failed'):DeliveryController(conn).pick_up(3,o.id)
    if endpoint.startswith('admin.archive'):
        OrderTrackingController(conn).cancel_order(1,o.id)
        if endpoint=='admin.archived_history':OrderArchiveController(conn).archive_order(4,o.id)
        data={'closed_before':'2026-10-26'}
    if endpoint in ('order.quote','order.confirm'):
        q=PlaceOrderController(conn).request_quote(1,1,1,{1:'1'})
        data=dict(hub_id='1',address_id='1',qty_1='1',payment='COD',quoted_total=str(q.total),quote_fingerprint=q.fingerprint(PaymentMethod.COD),idempotency_token='matrix-checkout')
    if endpoint=='account.register':data=registration()
    if endpoint=='auth.login':data={'username':'customer','password':'123456'}
    if endpoint=='account.update_profile':data=registration()
    if endpoint in ('account.new_address','account.edit_address'):data={'label':'Hotel','full_address':'123 Test Road','district':'District 1'}
    if endpoint in ('admin.new_hub','admin.edit_hub'):data=FORM
    if endpoint in ('admin.create_brand','admin.rename_brand'):data={'name':'Matrix Brand'}
    if endpoint in ('admin.new_item','admin.edit_item'):data=dict(brand_id='1',name='Matrix Dish',description='Synthetic',price='10000')
    if endpoint=='admin.list_item':data={'item_id':'9','available':'0'}
    if endpoint in ('admin.hub_item_availability','kitchen.set_availability'):data={'available':'0'}
    if endpoint in ('admin.new_voucher','admin.edit_voucher'):data=voucher_form()
    if endpoint in ('admin.new_user','admin.edit_user'):data=dict(username='matrix.staff',display_name='Matrix Staff',role='SHIPPER',password='abcdef')
    if endpoint=='admin.edit_user':data=dict(display_name='Matrix Staff',password='abcdef')
    if endpoint=='admin.set_user_active':data={'active':'0'}
    if endpoint in ('kitchen.reject','delivery.failed'):data={'reason':'Synthetic reason'}
    if endpoint=='delivery.delivered':data={'cash_collected':str(o.total)}
    values=dict(order_id=o.id,hub_id=2 if endpoint=='admin.archive_hub' else 1,item_id=1,brand_id=1,address_id=1,user_id=3,voucher_id=1)
    url=re.sub(r'<int:(\w+)>',lambda m:str(values[m[1]]),case['rule'])
    return url,data


@pytest.mark.parametrize('case',POLICY,ids=lambda r:r['method']+' '+r['rule'])
@pytest.mark.parametrize('actor',ACTORS)
def test_route_role_matrix(client,db_path,case,actor):
    conn=connect(db_path);url,data=context(conn,case)
    if actor=='INACTIVE':conn.execute('UPDATE user_account SET is_active=0 WHERE id=1')
    conn.close()
    if ACTORS[actor] is not None:
        with client.session_transaction() as session:session['_user_id']=str(ACTORS[actor]);session['_fresh']=True
    before=facts(db_path)
    response=client.open(url,method=case['method'],data=data if case['method']=='POST' else None)
    protected=case['roles']!='PUBLIC'
    denied=protected and actor!=case['roles']
    if denied:
        expected=302 if actor in ('ANONYMOUS','INACTIVE') else 403
        assert response.status_code==expected
        if expected==302:assert '/login?' in response.location
        assert facts(db_path)==before
    else:
        if actor=='INACTIVE' and case['endpoint']=='auth.login' and case['method']=='POST':
            assert response.status_code==401 and facts(db_path)==before
            return
        assert response.status_code in (200,301,302,303),response.get_data(as_text=True)
        assert b'Form expired' not in response.data
        # GET/public authentication operations never mutate domain rows; valid scoped POSTs have separate aggregate assertions.
        if case['method']=='GET' or case['endpoint'].startswith('auth.'):assert facts(db_path)==before


def test_invalid_replacement_decision_cannot_decline(client,db_path):
    conn=connect(db_path);o=place(conn).order
    conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=1')
    offer=KitchenController(conn).offer_replacement(2,o.id,o.lines[0].id,2);conn.close()
    with client.session_transaction() as s:s['_user_id']='1';s['_fresh']=True
    before=facts(db_path)
    assert client.post(f'/order/{o.id}/replacement',data={'offer_id':offer.id,'decision':'forged'}).status_code==400
    assert facts(db_path)==before


@pytest.mark.parametrize('endpoint,actor',[
    ('order.detail',6),('order.receipt',6),('order.confirmation',6),('order.cancel',6),('order.answer_replacement',6),
    ('kitchen.order',7),('kitchen.confirm',7),('kitchen.reject',7),('kitchen.offer',7),('kitchen.prepare',7),('kitchen.ready',7),
    ('delivery.detail',8),('delivery.delivered',8),('delivery.failed',8),
])
def test_foreign_owner_hub_and_assigned_shipper_paths(client,db_path,endpoint,actor):
    case=next(r for r in POLICY if r['endpoint']==endpoint)
    conn=connect(db_path);url,data=context(conn,case)
    if endpoint=='delivery.detail':DeliveryController(conn).pick_up(3,1)
    conn.close()
    with client.session_transaction() as s:s['_user_id']=str(actor);s['_fresh']=True
    before=facts(db_path);response=client.open(url,method=case['method'],data=data if case['method']=='POST' else None)
    assert response.status_code==(404 if endpoint=='order.receipt' else 403)
    assert facts(db_path)==before
