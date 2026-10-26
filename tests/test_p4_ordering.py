"""UC01 postconditions, independent money/distance boundaries and real contenders.
Author: 722I0004 · AI-assisted (Codex).
"""
import copy
import math
import sqlite3
import threading
from datetime import datetime,timezone
import pytest
from saigonbite.business.controllers import (PlaceOrderController,PaymentChoice,QuoteChangedError,
    PaymentDeclinedError,HubUnavailableError,AuthorizationError,ValidationError)
from saigonbite.business.domain import PaymentMethod,OnlineOption,Voucher,DiscountType
from saigonbite.data_access import connect,PaymentGatewaySimulator
from .p4_helpers import place
from .test_p4_foundation import facts,FaultConnection
from .conftest import add_second_customer,login,checkout_form


def accept(c,q,**kwargs):
    choice=kwargs.pop('payment',PaymentChoice())
    return c.confirm_order(1,1,1,{1:'1'},'accepted',q.total,payment=choice,
        quote_fingerprint=q.fingerprint(choice.method,choice.option),**kwargs)


@pytest.mark.parametrize('km,allowed,fee',[(0,True,15000),(3.2,True,24000),(7.99,True,36000),(8.0,True,36000),(8.004,False,None)])
def test_raw_radius_and_started_km_independent_sphere_fixture(db_path,km,allowed,fee):
    # Independent spherical meridian fixture: angular separation d/R, R=6371 km.
    # Float tolerance 1e-11 km is diagnostic only; the application's comparison stays raw <=8.
    conn=connect(db_path)
    conn.execute('UPDATE hub SET latitude=0,longitude=0 WHERE id=1')
    conn.execute('UPDATE address SET latitude=?,longitude=0 WHERE id=1',(math.degrees(km/6371),))
    c=PlaceOrderController(conn)
    if allowed:
        q=c.request_quote(1,1,1,{1:'1'})
        assert abs(q.distance_km-km)<1e-11 and q.delivery_fee==fee
        o=accept(c,q).order
        assert o.total==55000+fee-5000 and o.distance_km==round(km,2)
    else:
        with pytest.raises(HubUnavailableError):c.request_quote(1,1,1,{1:'1'})
        assert facts(db_path)['orders']==[] and facts(db_path)['payment']==[]
    conn.close()


@pytest.mark.parametrize('mutation',[
    "UPDATE menu_item SET name='changed same price' WHERE id=1",
    "UPDATE address SET full_address='changed address' WHERE id=1",
    "UPDATE address SET label='Hotel' WHERE id=1",
    "UPDATE hub SET name='changed hub' WHERE id=1",
    "UPDATE hub SET latitude=latitude+0.00001 WHERE id=1"])
def test_equal_total_content_changes_require_new_quote(db_path,mutation):
    conn=connect(db_path);c=PlaceOrderController(conn);q=c.request_quote(1,1,1,{1:'1'})
    conn.execute(mutation)
    assert c.request_quote(1,1,1,{1:'1'}).total==q.total
    before=facts(db_path)
    with pytest.raises(QuoteChangedError):accept(c,q)
    assert facts(db_path)==before and not conn.in_transaction
    conn.close()


def test_equal_price_different_item_and_payment_are_not_same_consent(db_path):
    conn=connect(db_path);conn.execute('UPDATE hub_menu_item SET is_available=1 WHERE hub_id=1 AND menu_item_id=5')
    c=PlaceOrderController(conn);q=c.request_quote(1,1,1,{1:'1'})
    with pytest.raises(QuoteChangedError):
        c.confirm_order(1,1,1,{5:'1'},'different',q.total,quote_fingerprint=q.fingerprint(PaymentMethod.COD))
    with pytest.raises(QuoteChangedError):
        c.confirm_order(1,1,1,{1:'1'},'online',q.total,payment=PaymentChoice(PaymentMethod.ONLINE,OnlineOption.E_WALLET,'APPROVE'),
            quote_fingerprint=q.fingerprint(PaymentMethod.COD))
    assert facts(db_path)['orders']==[] and facts(db_path)['payment']==[]
    conn.close()


def test_offsetting_fee_and_voucher_changes_requote_same_total(db_path):
    conn=connect(db_path)
    conn.execute("INSERT INTO voucher(code,discount_type,discount_value,min_subtotal,valid_from,valid_until) VALUES('SAME','FIXED',10000,0,'2000-01-01','2099-01-01')")
    c=PlaceOrderController(conn);q=c.request_quote(1,1,1,{1:'1'},'SAME')
    conn.execute('UPDATE hub SET base_delivery_fee=base_delivery_fee+1000 WHERE id=1')
    conn.execute("UPDATE voucher SET discount_value=11000 WHERE code='SAME'")
    assert c.request_quote(1,1,1,{1:'1'},'SAME').total==q.total
    with pytest.raises(QuoteChangedError):
        c.confirm_order(1,1,1,{1:'1'},'offset',q.total,'SAME',quote_fingerprint=q.fingerprint(PaymentMethod.COD))
    assert facts(db_path)['orders']==[]
    conn.close()


def test_fingerprint_binds_all_required_fields(db_path):
    conn=connect(db_path);q=PlaceOrderController(conn).request_quote(1,1,1,{1:'2'},'WELCOME20K')
    original=q.fingerprint(PaymentMethod.ONLINE,OnlineOption.E_WALLET)
    changes=[('hub','id'),('hub','name'),('hub','base_delivery_fee'),('address','id'),('address','full_address'),
             ('address','latitude'),('lines','quantity'),('lines','unit_price'),('lines','menu_item_id'),
             ('voucher','code'),(None,'delivery_fee'),(None,'quiet_discount'),(None,'voucher_discount')]
    for parent,key in changes:
        candidate=copy.deepcopy(q)
        obj=candidate if parent is None else candidate.lines[0] if parent=='lines' else getattr(candidate,parent)
        value=getattr(obj,key);setattr(obj,key,value+' changed' if isinstance(value,str) else value+1)
        assert candidate.fingerprint(PaymentMethod.ONLINE,OnlineOption.E_WALLET)!=original,(parent,key)
    assert q.fingerprint(PaymentMethod.COD)!=original
    assert q.fingerprint(PaymentMethod.ONLINE,OnlineOption.BANK_QR)!=original
    conn.close()


def test_quiet_strict_boundary_capped_fee_and_snapshot(db_path):
    conn=connect(db_path);conn.execute('UPDATE hub SET max_active_orders=4 WHERE id=1')
    first=place(conn).order
    assert first.quiet_discount==5000 and first.total==65000
    q=PlaceOrderController(conn).request_quote(1,1,1,{1:'1'})
    assert q.quiet_discount==0 and q.total==70000
    place(conn)
    assert conn.execute('SELECT total_amount FROM orders WHERE id=?',(first.id,)).fetchone()[0]==65000
    conn.execute('UPDATE hub SET base_delivery_fee=0 WHERE id=2')
    conn.execute('UPDATE address SET latitude=10.8106,longitude=106.7091 WHERE id=1')
    q=PlaceOrderController(conn).request_quote(1,2,1,{9:'1'})
    assert q.delivery_fee==3000 and q.quiet_discount==3000 and q.total==30000
    conn.close()


@pytest.mark.parametrize('kind,value,cap,subtotal,expected',[
    ('FIXED',5000,None,10000,5000),('FIXED',20000,None,10000,10000),
    ('PERCENT',33,None,101,33),('PERCENT',50,10,100,10),('PERCENT',100,None,0,0)])
def test_voucher_independent_integer_oracle(kind,value,cap,subtotal,expected):
    v=Voucher(1,'T','',DiscountType(kind),value,0,cap,'2026-10-26','2026-10-26')
    assert v.discount_for(subtotal)==expected
    assert v.problem(subtotal,'2026-10-26') is None
    assert v.problem(subtotal,'2026-10-25') and v.problem(subtotal,'2026-10-27')
    v.archived_at='2026-10-26T00:00:00+00:00';assert v.problem(subtotal,'2026-10-26')


def test_vietnam_inclusive_voucher_day_edges(db_path):
    conn=connect(db_path)
    conn.execute("UPDATE voucher SET min_subtotal=0,valid_from='2026-10-26',valid_until='2026-10-26' WHERE code='WELCOME20K'")
    for stamp,valid in [('2026-10-25T16:59:59+00:00',False),('2026-10-25T17:00:00+00:00',True),
                        ('2026-10-26T16:59:59+00:00',True),('2026-10-26T17:00:00+00:00',False)]:
        c=PlaceOrderController(conn,clock=lambda:datetime.fromisoformat(stamp))
        if valid: assert c.request_quote(1,1,1,{1:'1'},'WELCOME20K').voucher_discount==20000
        else:
            with pytest.raises(ValidationError):c.request_quote(1,1,1,{1:'1'},'WELCOME20K')
    conn.close()


class RecordingGateway(PaymentGatewaySimulator):
    def __init__(self,conn):self.events=[];self.conn=conn
    def authorise(self,*args):
        assert self.conn.in_transaction
        a=super().authorise(*args);self.events.append(('authorise',a.reference));return a
    def release(self,ref):self.events.append(('release',ref));super().release(ref)


@pytest.mark.parametrize('failure',['insert','COMMIT'])
def test_online_approval_then_failure_releases_authorization_and_rolls_back(db_path,monkeypatch,failure):
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    c=PlaceOrderController(conn,gateway=RecordingGateway(conn));choice=PaymentChoice(PaymentMethod.ONLINE,OnlineOption.E_WALLET,'APPROVE')
    q=c.request_quote(1,1,1,{1:'1'},payment=choice);before=facts(db_path)
    if failure=='COMMIT':conn.fault='COMMIT'
    else:monkeypatch.setattr(c.payments,'insert',lambda *a:(_ for _ in ()).throw(sqlite3.OperationalError('injected insert')))
    with pytest.raises(sqlite3.OperationalError):accept(c,q,payment=choice)
    assert [x[0] for x in c.gateway.events]==['authorise','release']
    assert c.gateway.events[0][1]==c.gateway.events[1][1]
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('user,address,option',[(1,1,OnlineOption.E_WALLET),(1,1,OnlineOption.BANK_QR),(6,3,OnlineOption.INTERNATIONAL_CARD)])
@pytest.mark.parametrize('outcome',['APPROVE','DECLINE'])
def test_local_and_tourist_online_allowed_options_and_decline(db_path,user,address,option,outcome):
    conn=connect(db_path);choice=PaymentChoice(PaymentMethod.ONLINE,option,outcome)
    if outcome=='DECLINE':
        with pytest.raises(PaymentDeclinedError):place(conn,user=user,address=address,payment=choice)
        assert facts(db_path)['orders']==[] and facts(db_path)['payment']==[] and facts(db_path)['order_line']==[]
    else:
        result=place(conn,user=user,address=address,payment=choice)
        assert result.payment.state.value=='PAID' and result.payment.amount==result.order.total
        assert result.payment.provider_ref.startswith('SIM-')
    conn.close()


def test_replay_ignores_changed_current_input_but_foreign_token_never_discloses(db_path):
    add_second_customer(db_path);conn=connect(db_path)
    first=place(conn,token='own-replay');before=facts(db_path)
    repeated=PlaceOrderController(conn).confirm_order(1,999,999,{},'own-replay',None,payment=PaymentChoice('invalid'))
    assert repeated.order.id==first.order.id and not repeated.created and facts(db_path)==before
    with pytest.raises(AuthorizationError):PlaceOrderController(conn).confirm_order(10,1,10,{},'own-replay')
    assert facts(db_path)==before
    conn.close()


def test_two_customers_race_last_slot_one_durable_winner(db_path):
    add_second_customer(db_path);setup=connect(db_path)
    setup.execute('UPDATE hub SET max_active_orders=1 WHERE id=1');setup.close()
    barrier=threading.Barrier(2,timeout=10);results=[];errors=[]
    def contend(user,address):
        conn=None
        try:
            conn=connect(db_path);c=PlaceOrderController(conn);q=c.request_quote(user,1,address,{1:'1'})
            barrier.wait()
            try:
                r=c.confirm_order(user,1,address,{1:'1'},'slot-'+str(user),q.total,quote_fingerprint=q.fingerprint(PaymentMethod.COD))
                results.append(('placed',r.order.id))
            except HubUnavailableError:results.append(('busy',None))
        except BaseException as exc:errors.append(repr(exc));barrier.abort()
        finally:
            if conn is not None:conn.close()
    threads=[threading.Thread(target=contend,args=x) for x in [(1,1),(10,10)]]
    for t in threads:t.start()
    for t in threads:t.join(20);assert not t.is_alive()
    assert not errors and sorted(r[0] for r in results)==['busy','placed']
    state=facts(db_path)
    assert len(state['orders'])==len(state['order_line'])==len(state['payment'])==1


def test_suggestion_ratio_raw_distance_id_ties_limit_and_empty(db_path):
    conn=connect(db_path)
    conn.execute('UPDATE address SET latitude=0,longitude=0 WHERE id=1')
    conn.execute('UPDATE hub SET latitude=?,longitude=0 WHERE id=2',(math.degrees(3/6371),))
    for ident,km in [(3,1),(4,1),(5,2),(6,9)]:
        conn.execute('INSERT INTO hub(id,code,name,address_text,latitude,longitude,max_active_orders,base_delivery_fee) VALUES(?,?,?,?,?,0,4,0)',
            (ident,'HUB-T'+str(ident),'Test'+str(ident),'Test',math.degrees(km/6371)))
        conn.execute('INSERT INTO hub_menu_item VALUES(?,1,1)',(ident,))
    c=PlaceOrderController(conn);address=c.customers.get_address(1,1)
    assert [s.hub.id for s in c.suggest_hubs(1,address)]==[3,4,5]
    place(conn,hub=3)
    assert [s.hub.id for s in c.suggest_hubs(1,address)]==[4,5,2]
    conn.execute('UPDATE hub SET archived_at="2026-10-26T00:00:00+00:00" WHERE id IN (2,3,4,5)')
    assert c.suggest_hubs(1,address)==[]  # remaining active hub 6 is out of range
    conn.close()


def test_http_unmodified_quote_forged_fields_and_pretransaction_online_choice(client,db_path):
    import re
    login(client,'customer')
    form=checkout_form(client=client,token='route-fp',quantities={1:'1'})
    before=facts(db_path)
    assert client.post('/order/confirm',data={**form,'quote_fingerprint':'forged','quoted_total':1,'unit_price':1}).status_code==409
    assert facts(db_path)==before
    assert client.post('/order/confirm',data={**form,'unit_price':1,'total_amount':1}).status_code==303
    assert facts(db_path)['orders'][0][0]>=1
    conn=connect(db_path)
    assert conn.execute('SELECT amount FROM payment').fetchone()[0]==65000  # Server prices prevail.
    conn.close()
    # A valid online quote includes its payment choice before the simulator interaction.
    page=client.post('/order/quote',data={'hub_id':1,'address_id':1,'qty_1':'1','payment':'ONLINE:E_WALLET'}).get_data(as_text=True)
    fields=dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"',page))
    fields['payment']='ONLINE:E_WALLET'
    before=facts(db_path)
    simulator=client.post('/order/confirm',data=fields)
    assert simulator.status_code==200 and 'Payment simulator' in simulator.get_data(as_text=True)
    assert facts(db_path)==before
    approved=client.post('/order/confirm',data={**fields,'sim_outcome':'APPROVE'})
    assert approved.status_code==303
    conn=connect(db_path)
    assert conn.execute("SELECT COUNT(*) FROM payment WHERE method='ONLINE' AND state='PAID'").fetchone()[0]==1
    conn.close()
