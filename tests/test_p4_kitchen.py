"""UC05/SUC03–06: money oracle, guards, snapshots, atomicity and serialized races.
Author: 722I0004 · AI-assisted (Codex).
"""
import sqlite3
import threading
import pytest
from saigonbite.business.controllers import (KitchenController,OrderTrackingController,PaymentChoice,
    ConflictError,ValidationError,AuthorizationError)
from saigonbite.business.domain import PaymentMethod,OnlineOption,PaymentState,PAYMENT_TRANSITIONS
from saigonbite.data_access import connect
from .p4_helpers import place
from .test_p4_foundation import facts,FaultConnection
from .conftest import add_second_customer,login


def oracle_order(conn,online=True):
    # Locked hand oracle: S=100000, D=10000, F=15000, Q=5000, T=C=100000.
    conn.execute('UPDATE menu_item SET price=50000 WHERE id=1')
    conn.execute('UPDATE menu_item SET price=45000 WHERE id=2')
    choice=PaymentChoice(PaymentMethod.ONLINE,OnlineOption.E_WALLET,'APPROVE') if online else None
    o=place(conn,lines={1:'2'},payment=choice,voucher='LUNCH10').order
    assert (o.item_subtotal,o.voucher_discount,o.delivery_fee,o.quiet_discount,o.total)==(100000,10000,15000,5000,100000)
    return o


def offer_for(conn,o):
    conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=1')
    return KitchenController(conn).offer_replacement(2,o.id,o.lines[0].id,2)


@pytest.mark.parametrize('online',[True,False])
@pytest.mark.parametrize('outcome',['cancel','reject','decline'])
def test_fixed_money_oracle_partial_then_unfulfilled_owes_full_c(db_path,online,outcome):
    conn=connect(db_path);o=oracle_order(conn,online);offer=offer_for(conn,o)
    # Offered price is retained after a later catalogue change.
    conn.execute('UPDATE menu_item SET price=80000 WHERE id=2')
    t=OrderTrackingController(conn);detail=t.answer_replacement(1,o.id,offer.id,True)
    assert (detail.order.item_subtotal,detail.order.voucher_discount,detail.order.total)==(90000,10000,90000)
    assert detail.order.lines[0].quantity==2 and detail.order.lines[0].unit_price==45000
    assert detail.payment.amount==(100000 if online else 90000)
    assert detail.payment.refund_amount==(10000 if online else 0)
    if outcome=='cancel':detail=t.cancel_order(1,o.id)
    elif outcome=='reject':KitchenController(conn).reject_order(2,o.id,'Cannot fulfil');detail=t.get_order(1,o.id)
    else:
        conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=2')
        next_offer=KitchenController(conn).offer_replacement(2,o.id,detail.order.lines[0].id,6)
        detail=t.answer_replacement(1,o.id,next_offer.id,False)
    assert detail.payment.state is (PaymentState.REFUND_PENDING if online else PaymentState.VOIDED)
    assert detail.payment.refund_amount==(100000 if online else 0)
    assert detail.order.state.value in ('CANCELLED','REJECTED')
    assert PaymentState.REFUNDED not in PAYMENT_TRANSITIONS[PaymentState.REFUND_PENDING]
    conn.close()


@pytest.mark.parametrize('mutation',[
    'UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=2',
    'DELETE FROM hub_menu_item WHERE hub_id=1 AND menu_item_id=2',
    "UPDATE menu_item SET archived_at='2026-10-26' WHERE id=2",
    "UPDATE brand SET archived_at='2026-10-26' WHERE id=1"])
def test_invalid_target_withdraws_only_exact_offer(db_path,mutation):
    conn=connect(db_path);o=oracle_order(conn);offer=offer_for(conn,o);conn.execute(mutation)
    before=facts(db_path)
    result=OrderTrackingController(conn).answer_replacement(1,o.id,offer.id,True)
    after=facts(db_path)
    assert result.notice and 'withdrawn' in result.notice
    assert conn.execute('SELECT state FROM replacement_offer WHERE id=?',(offer.id,)).fetchone()[0]=='WITHDRAWN'
    assert all(after[table]==before[table] for table in before if table!='replacement_offer')
    assert result.order.total==100000 and result.payment.amount==100000 and result.payment.refund_amount==0
    with pytest.raises(ConflictError):OrderTrackingController(conn).answer_replacement(1,o.id,offer.id,True)
    assert facts(db_path)==after
    conn.close()


@pytest.mark.parametrize('scenario',['available_source','foreign_hub','foreign_line','expensive','unlisted','sold_out','same_item','archived_target','archived_brand'])
def test_offer_guard_one_negative_per_condition(db_path,scenario):
    conn=connect(db_path);o=oracle_order(conn);staff,line,target=2,o.lines[0].id,2
    if scenario!='available_source':conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=1')
    if scenario=='foreign_hub':staff=7
    elif scenario=='foreign_line':line=999
    elif scenario=='expensive':target=4
    elif scenario=='unlisted':target=9
    elif scenario=='sold_out':target=5
    elif scenario=='same_item':target=1
    elif scenario=='archived_target':conn.execute("UPDATE menu_item SET archived_at='2026-10-26' WHERE id=2")
    elif scenario=='archived_brand':conn.execute("UPDATE brand SET archived_at='2026-10-26' WHERE id=1")
    before=facts(db_path)
    with pytest.raises((ValidationError,AuthorizationError)):KitchenController(conn).offer_replacement(staff,o.id,line,target)
    assert facts(db_path)==before
    conn.close()


def test_open_offer_confirmation_preparing_stale_and_foreign_answers(db_path):
    add_second_customer(db_path);conn=connect(db_path);o=oracle_order(conn);offer=offer_for(conn,o)
    k=KitchenController(conn);t=OrderTrackingController(conn);before=facts(db_path)
    with pytest.raises(ConflictError):k.offer_replacement(2,o.id,o.lines[0].id,6)
    with pytest.raises(ConflictError):k.confirm_order(2,o.id)
    with pytest.raises(ConflictError):k.start_preparing(2,o.id)
    with pytest.raises(ConflictError):t.answer_replacement(1,o.id,999,True)
    with pytest.raises(AuthorizationError):t.answer_replacement(10,o.id,offer.id,True)
    assert facts(db_path)==before
    t.cancel_order(1,o.id);before=facts(db_path)
    with pytest.raises(ConflictError):t.answer_replacement(1,o.id,offer.id,True)
    with pytest.raises(ConflictError):t.cancel_order(1,o.id)
    assert facts(db_path)==before
    conn.close()


def test_preparing_blocked_with_open_offer_even_if_confirmed_state(db_path):
    conn=connect(db_path);o=oracle_order(conn);offer_for(conn,o)
    conn.execute("UPDATE orders SET state='CONFIRMED' WHERE id=?",(o.id,));before=facts(db_path)
    with pytest.raises(ConflictError):KitchenController(conn).start_preparing(2,o.id)
    assert facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('action',['confirm','reject','offer','prepare','ready','accept','decline','cancel'])
def test_each_kitchen_aggregate_rolls_back_through_commit(db_path,action):
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    o=oracle_order(conn);k=KitchenController(conn);t=OrderTrackingController(conn);offer=None
    if action in ('accept','decline'):offer=offer_for(conn,o)
    elif action=='offer':conn.execute('UPDATE hub_menu_item SET is_available=0 WHERE hub_id=1 AND menu_item_id=1')
    elif action in ('prepare','ready'):
        k.confirm_order(2,o.id)
        if action=='ready':k.start_preparing(2,o.id)
    before=facts(db_path);conn.fault='COMMIT'
    commands={'confirm':lambda:k.confirm_order(2,o.id),'reject':lambda:k.reject_order(2,o.id,'Reason'),
        'offer':lambda:k.offer_replacement(2,o.id,o.lines[0].id,2),'prepare':lambda:k.start_preparing(2,o.id),
        'ready':lambda:k.mark_ready(2,o.id),'accept':lambda:t.answer_replacement(1,o.id,offer.id,True),
        'decline':lambda:t.answer_replacement(1,o.id,offer.id,False),'cancel':lambda:t.cancel_order(1,o.id)}
    with pytest.raises(sqlite3.OperationalError,match='injected COMMIT'):commands[action]()
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('component',['order','payment','offer'])
def test_accept_zero_row_outcome_rolls_back_every_component(db_path,monkeypatch,component):
    conn=connect(db_path);o=oracle_order(conn);offer=offer_for(conn,o);c=OrderTrackingController(conn)
    obj,method={'order':(c.orders,'save_lines_and_totals'),'payment':(c.payments,'set_amounts'),'offer':(c.offers,'decide')}[component]
    monkeypatch.setattr(obj,method,lambda *a:False);before=facts(db_path)
    with pytest.raises(ConflictError):c.answer_replacement(1,o.id,offer.id,True)
    assert facts(db_path)==before and not conn.in_transaction
    conn.close()


def test_ready_creates_one_delivery_and_insert_failure_rolls_back(db_path,monkeypatch):
    conn=connect(db_path);o=oracle_order(conn);k=KitchenController(conn);k.confirm_order(2,o.id);k.start_preparing(2,o.id)
    before=facts(db_path);original=k.deliveries.insert
    monkeypatch.setattr(k.deliveries,'insert',lambda *a:(_ for _ in ()).throw(sqlite3.OperationalError('insert failure')))
    with pytest.raises(sqlite3.OperationalError):k.mark_ready(2,o.id)
    assert facts(db_path)==before
    monkeypatch.setattr(k.deliveries,'insert',original);k.mark_ready(2,o.id);before=facts(db_path)
    assert len(before['delivery'])==1
    with pytest.raises(ConflictError):k.mark_ready(2,o.id)
    assert facts(db_path)==before
    conn.close()


def test_receipt_stored_snapshot_read_only_own_and_truthful(client,app,db_path,monkeypatch):
    import saigonbite.presentation.db as db_module
    add_second_customer(db_path);conn=connect(db_path);o=oracle_order(conn);offer=offer_for(conn,o)
    t=OrderTrackingController(conn);t.answer_replacement(1,o.id,offer.id,True)
    conn.execute("UPDATE menu_item SET name='New master name',price=99999 WHERE id=2")
    conn.close();login(client,'customer');before=facts(db_path);attempts=[]
    original=db_module.connect
    def observed(path):
        c=original(path)
        def authorize(action,*args):
            if action in (sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE):attempts.append(action);return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        c.set_authorizer(authorize);return c
    monkeypatch.setattr(db_module,'connect',observed)
    response=client.get(f'/order/{o.id}/receipt');page=response.get_data(as_text=True)
    assert response.status_code==200 and not attempts and facts(db_path)==before
    for text in ['Pho ga','90,000 VND','10,000 VND','100,000 VND','Simulated payment','Approximate',
                 'Item subtotal S','Voucher discount D','Delivery fee F','Quiet discount Q','Total T','PAID','E_WALLET']:
        assert text in page,text
    assert 'New master name' not in page and 'already refunded' not in page
    foreign=app.test_client();foreign.post('/login',data={'username':'other','password':'dev-other'})
    assert foreign.get(f'/order/{o.id}/receipt').status_code==404
    assert not attempts


@pytest.mark.parametrize('race',['accept_cancel','cancel_prepare'])
def test_customer_kitchen_races_admit_valid_serializations(db_path,race):
    setup=connect(db_path);o=oracle_order(setup)
    if race=='accept_cancel':offer=offer_for(setup,o)
    else:KitchenController(setup).confirm_order(2,o.id)
    setup.close();barrier=threading.Barrier(2,timeout=10);results=[];errors=[]
    def contend(which):
        conn=None
        try:
            conn=connect(db_path);t=OrderTrackingController(conn);k=KitchenController(conn)
            barrier.wait()
            try:
                if which=='cancel':t.cancel_order(1,o.id)
                elif which=='accept':t.answer_replacement(1,o.id,offer.id,True)
                else:k.start_preparing(2,o.id)
                results.append((which,'ok'))
            except ConflictError:results.append((which,'stale'))
        except BaseException as exc:errors.append(repr(exc));barrier.abort()
        finally:
            if conn is not None:conn.close()
    choices=['cancel','accept' if race=='accept_cancel' else 'prepare']
    threads=[threading.Thread(target=contend,args=(x,)) for x in choices]
    for t in threads:t.start()
    for t in threads:t.join(20);assert not t.is_alive()
    assert not errors and len(results)==2
    conn=connect(db_path);d=OrderTrackingController(conn).get_order(1,o.id)
    if race=='accept_cancel':
        assert d.order.state.value=='CANCELLED' and d.payment.refund_amount==100000
        assert ('cancel','ok') in results
        # accept-then-cancel may both succeed; cancel-first makes the answer stale.
    else:
        assert d.order.state.value in ('CANCELLED','PREPARING')
        assert sum(status=='ok' for _,status in results)==1
    conn.close()
