"""UC02 durable claim/finish guarantees. Author: 722I0004 · AI-assisted (Codex)."""
import sqlite3
import threading
import pytest
from saigonbite.business.controllers import (DeliveryController,KitchenController,OrderTrackingController,
    UserAdminController,ConflictError,ValidationError,AuthorizationError)
from saigonbite.data_access import connect
from .test_p4_kitchen import oracle_order,offer_for
from .test_p4_foundation import facts,FaultConnection
from .conftest import login


def ready(conn,online=False,partial=False):
    o=oracle_order(conn,online)
    if partial:
        offer=offer_for(conn,o);OrderTrackingController(conn).answer_replacement(1,o.id,offer.id,True)
    k=KitchenController(conn);k.confirm_order(2,o.id);k.start_preparing(2,o.id);k.mark_ready(2,o.id)
    return o


def test_two_shippers_one_ready_order_exactly_one_persisted_claim(db_path):
    conn=connect(db_path);o=ready(conn);conn.close()
    barrier=threading.Barrier(2,timeout=10);results=[];errors=[]
    def contend(actor):
        c=None
        try:
            c=connect(db_path);controller=DeliveryController(c);barrier.wait()
            try:controller.pick_up(actor,o.id);results.append((actor,'won'))
            except ConflictError:results.append((actor,'lost'))
        except BaseException as exc:errors.append(repr(exc));barrier.abort()
        finally:
            if c is not None:c.close()
    threads=[threading.Thread(target=contend,args=(x,)) for x in (3,8)]
    for t in threads:t.start()
    for t in threads:t.join(20);assert not t.is_alive()
    assert not errors and sorted(x[1] for x in results)==['lost','won']
    winner=next(actor for actor,outcome in results if outcome=='won')
    conn=connect(db_path)
    row=conn.execute('SELECT shipper_id,state,picked_up_at FROM delivery WHERE order_id=?',(o.id,)).fetchone()
    assert tuple(row[:2])==(winner,'PICKED_UP') and row['picked_up_at']
    assert conn.execute('SELECT state FROM orders WHERE id=?',(o.id,)).fetchone()[0]=='OUT_FOR_DELIVERY'
    assert conn.execute('SELECT COUNT(*) FROM delivery').fetchone()[0]==1
    conn.close()


@pytest.mark.parametrize('cash',[None,'','99999','100001','-1','one','100000.0'])
def test_cod_requires_exact_whole_cash_and_no_partial_writes(db_path,cash):
    conn=connect(db_path);o=ready(conn);c=DeliveryController(conn);c.pick_up(3,o.id);before=facts(db_path)
    with pytest.raises(ValidationError):c.confirm_delivered(3,o.id,cash)
    assert facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('outcome',['delivered','failed'])
@pytest.mark.parametrize('online,partial',[(False,False),(True,False),(True,True)])
def test_assigned_finish_pair_states_timestamps_refund_and_repeat(db_path,outcome,online,partial):
    conn=connect(db_path);o=ready(conn,online,partial);c=DeliveryController(conn);c.pick_up(3,o.id)
    before=facts(db_path)
    with pytest.raises(AuthorizationError):c.confirm_delivered(8,o.id,'100000')
    with pytest.raises(AuthorizationError):c.report_failure(8,o.id,'failed')
    with pytest.raises(ValidationError):c.report_failure(3,o.id,'   ')
    assert facts(db_path)==before
    if outcome=='delivered':d=c.confirm_delivered(3,o.id,None if online else '100,000')
    else:d=c.report_failure(3,o.id,'No customer at destination')
    assert d.delivery.picked_up_at and d.delivery.finished_at and d.order.closed_at
    assert d.delivery.finished_at==d.order.closed_at
    if outcome=='delivered':
        assert d.order.state.value==d.delivery.state.value=='DELIVERED'
        assert d.payment.state.value=='PAID'
        assert d.delivery.cash_collected==(None if online else 100000)
        assert d.payment.refund_amount==(10000 if partial else 0)
    else:
        assert d.order.state.value=='DELIVERY_FAILED' and d.delivery.state.value=='FAILED'
        assert d.delivery.failure_reason=='No customer at destination'
        assert d.payment.state.value==('REFUND_PENDING' if online else 'VOIDED')
        assert d.payment.refund_amount==(100000 if online else 0)
    before=facts(db_path)
    for command in [lambda:c.confirm_delivered(3,o.id,'100000'),lambda:c.report_failure(3,o.id,'repeat'),lambda:c.pick_up(3,o.id)]:
        with pytest.raises(ConflictError):command()
        assert facts(db_path)==before
    conn.close()


def test_shipper_multiple_assignments_allowed_and_deactivation_guard(db_path):
    conn=connect(db_path);a=ready(conn);b=ready(conn);c=DeliveryController(conn)
    c.pick_up(3,a.id);c.pick_up(3,b.id)
    assert len(c.board(3).mine)==2
    before=facts(db_path)
    with pytest.raises(ConflictError):UserAdminController(conn).set_active(4,3,False)
    assert facts(db_path)==before
    c.confirm_delivered(3,a.id,'100000');c.report_failure(3,b.id,'failed')
    UserAdminController(conn).set_active(4,3,False)
    assert conn.execute('SELECT is_active FROM user_account WHERE id=3').fetchone()[0]==0
    with pytest.raises(AuthorizationError):c.board(3)
    conn.close()


@pytest.mark.parametrize('operation',['pickup','delivered','failed'])
def test_delivery_commit_failure_rolls_back_entire_aggregate(db_path,operation):
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    o=ready(conn,True,True);c=DeliveryController(conn)
    if operation!='pickup':c.pick_up(3,o.id)
    before=facts(db_path);conn.fault='COMMIT'
    with pytest.raises(sqlite3.OperationalError,match='injected COMMIT'):
        if operation=='pickup':c.pick_up(3,o.id)
        elif operation=='delivered':c.confirm_delivered(3,o.id,None)
        else:c.report_failure(3,o.id,'Failed')
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('operation',['pickup','delivered','failed'])
@pytest.mark.parametrize('failure',['zero','write_error'])
def test_delivery_zero_row_outcome_rolls_back(db_path,monkeypatch,operation,failure):
    conn=connect(db_path);o=ready(conn);c=DeliveryController(conn)
    if operation!='pickup':c.pick_up(3,o.id)
    method='take' if operation=='pickup' else 'finish'
    def injected(*args,**kwargs):
        if failure=='write_error':raise sqlite3.OperationalError('injected delivery write')
        return False
    monkeypatch.setattr(c.deliveries,method,injected)
    before=facts(db_path)
    with pytest.raises(ConflictError if failure=='zero' else sqlite3.OperationalError):
        if operation=='pickup':c.pick_up(3,o.id)
        elif operation=='delivered':c.confirm_delivered(3,o.id,'100000')
        else:c.report_failure(3,o.id,'Failed')
    assert facts(db_path)==before
    conn.close()


def test_passport_never_rendered_to_kitchen_shipper_or_logs(app,db_path,caplog):
    conn=connect(db_path);marker='PASSPORT-PRIVATE-SENTINEL'
    conn.execute('UPDATE customer SET passport_no=? WHERE id=1',(marker,))
    o=ready(conn,True);conn.close()
    kitchen=app.test_client();login(kitchen,'kitchen')
    shipper=app.test_client();login(shipper,'shipper')
    for client,path in [(kitchen,'/kitchen/'),(kitchen,f'/kitchen/orders/{o.id}'),
                        (shipper,'/delivery/'),(shipper,f'/delivery/orders/{o.id}')]:
        response=client.get(path);assert response.status_code==200
        assert marker not in response.get_data(as_text=True)
    assert marker not in shipper.post(f'/delivery/orders/{o.id}/failed',data={'reason':''}).get_data(as_text=True)
    assert marker not in caplog.text
