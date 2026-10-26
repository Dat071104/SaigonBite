"""Supporting CRUD/identity/transaction contracts. Author: 722I0004 · AI-assisted (Codex)."""
import sqlite3
import pytest
from saigonbite.business.controllers import AccountController, UserAdminController, VoucherController, OrderArchiveController, ConflictError, ValidationError, NotFoundError
from saigonbite.data_access import connect, UserDAO, CustomerDAO
from saigonbite.data_access.database import StaleWriteError
from .conftest import login
from .test_p4_foundation import facts, FaultConnection
from .p4_helpers import place


def registration(kind='LOCAL', **changes):
    return dict(username='new.customer',password='abcdef',password_again='abcdef',customer_type=kind,
                full_name='New Customer',phone='0901234567',email='visitor@example.test',
                passport_no='AB123456',nationality='Canada',**changes)


@pytest.mark.parametrize('kind',['LOCAL','TOURIST'])
def test_real_registration_profile_hotel_address_and_logout(client,db_path,kind):
    form=registration(kind)
    if kind=='TOURIST':form['phone']=''
    assert client.post('/register',data=form).status_code==303
    conn=connect(db_path); user=UserDAO(conn).get_by_username('new.customer')
    assert user.created_at and user.role.value=='CUSTOMER'
    assert client.get('/account').status_code==200
    form['full_name']='Changed Customer'
    assert client.post('/account',data=form).status_code==303
    p=AccountController(conn).get_profile(user.id)
    assert p.customer.full_name==p.user.display_name=='Changed Customer'
    assert p.customer.customer_type.value==kind
    if kind=='TOURIST':assert p.customer.phone is None and p.customer.nationality=='Canada'
    address=dict(label='Hotel',full_address='20 Synthetic Hotel Road',district='District 1')
    assert client.post('/account/addresses/new',data=address).status_code==303
    a=AccountController(conn).get_profile(user.id).addresses[0]
    assert a.label=='Hotel'
    assert client.post(f'/account/addresses/{a.id}',data={**address,'label':'Office'}).status_code==303
    assert client.post(f'/account/addresses/{a.id}/archive').status_code==303
    assert not AccountController(conn).get_profile(user.id).addresses
    assert client.post('/logout').status_code==302
    assert client.get('/account').status_code==302
    conn.close()


@pytest.mark.parametrize('field,value', [('full_name','x'),('username','x'),('password','x'),('password_again','different'),('phone','123'),('customer_type','ADMIN')])
def test_registration_invalid_fields_zero_writes(db_path,field,value):
    conn=connect(db_path);before=facts(db_path);f=registration();f[field]=value
    with pytest.raises(ValidationError):AccountController(conn).register(f)
    assert facts(db_path)==before;conn.close()


@pytest.mark.parametrize('field,value',[('nationality',''),('passport_no','x'),('email','invalid'),('phone','abc')])
def test_tourist_required_identity(db_path,field,value):
    conn=connect(db_path);before=facts(db_path);f=registration('TOURIST');f[field]=value
    with pytest.raises(ValidationError):AccountController(conn).register(f)
    assert facts(db_path)==before;conn.close()


@pytest.mark.parametrize('sql',[
    "INSERT INTO customer(user_id,full_name,customer_type,passport_no,email) VALUES(3,'Bad','TOURIST','ABC123','a@b.test')",
    "INSERT INTO customer(user_id,full_name,customer_type,phone) VALUES(4,'Bad','LOCAL','0901234567')",
    "UPDATE customer SET user_id=4 WHERE id=1",
    "UPDATE user_account SET role='MANAGER' WHERE id=1",
    "UPDATE customer SET customer_type='OTHER' WHERE id=1",
    "UPDATE customer SET nationality=NULL WHERE customer_type='TOURIST'",
])
def test_sql_type_nationality_and_linked_role_guards(db_path,sql):
    conn=connect(db_path);before=facts(db_path)
    with pytest.raises(sqlite3.IntegrityError):conn.execute(sql)
    assert facts(db_path)==before;conn.close()


def test_foreign_address_inactive_session_admin_customer_read(client,db_path):
    conn=connect(db_path);account=AccountController(conn);u=account.register(registration('TOURIST'))
    address=account.add_address(u.id,dict(label='Hotel',full_address='10 Another Road',district='District 1'))
    login(client,'customer');before=facts(db_path)
    assert client.post(f'/account/addresses/{address.id}/archive').status_code==404
    assert client.get(f'/account/addresses/{address.id}').status_code==404
    assert facts(db_path)==before
    UserAdminController(conn).set_active(4,1,False)
    assert client.get('/account').status_code==302
    assert client.post('/login',data={'username':'customer','password':'123456'}).status_code==401
    login(client,'admin')
    html=client.get(f'/admin/users/{u.id}').get_data(as_text=True)
    assert 'AB123456' in html and 'Canada' in html
    UserAdminController(conn).set_active(4,1,True)
    login(client,'customer');assert client.get(f'/admin/users/{u.id}').status_code==403
    conn.close()


def test_staff_crud_hub_assignment_activation_and_retained_username(client,db_path):
    login(client,'admin');conn=connect(db_path);c=UserAdminController(conn)
    f=dict(username='new.kitchen',password='abcdef',role='KITCHEN_STAFF',display_name='New Kitchen',hub_id='1')
    assert client.post('/admin/users/new',data=f).status_code==303
    u=c.users.get_by_username('new.kitchen');assert u.hub_id==1
    assert client.post(f'/admin/users/{u.id}',data={**f,'hub_id':'2','display_name':'Moved Kitchen'}).status_code==303
    assert c.get_user(4,u.id).hub_id==2
    assert client.post(f'/admin/users/{u.id}/active',data={'active':'0'}).status_code==303
    before=facts(db_path)
    with pytest.raises(ValidationError):c.create_staff(4,f)
    response=client.post(f'/admin/users/{u.id}/active',data={'active':'invalid'},follow_redirects=True)
    assert response.status_code==200 and b'Choose a valid availability or active status' in response.data
    assert facts(db_path)==before
    assert client.post(f'/admin/users/{u.id}/active',data={'active':'1'}).status_code==303
    assert c.get_user(4,u.id).is_active
    conn.execute("UPDATE hub SET archived_at='2026-10-26T00:00:00+00:00' WHERE id=2")
    before=facts(db_path)
    with pytest.raises(ValidationError):c.update_user(4,u.id,{**f,'hub_id':'2'})
    assert facts(db_path)==before;conn.close()


def voucher_form():
    return dict(code='NEW20',description='Synthetic',discount_type='PERCENT',discount_value='20',
                min_subtotal='10000',max_discount='5000',valid_from='2026-01-01',valid_until='2026-12-31')


def test_real_voucher_crud_lifetime_code_and_conditional_save(client,db_path,monkeypatch):
    login(client,'admin');conn=connect(db_path);c=VoucherController(conn);f=voucher_form()
    assert client.post('/admin/vouchers/new',data=f).status_code==303
    v=next(v for v in c.list_vouchers(4) if v.code=='NEW20')
    assert client.get(f'/admin/vouchers/{v.id}').status_code==200
    assert client.post(f'/admin/vouchers/{v.id}',data={**f,'discount_value':'25'}).status_code==303
    assert c.get_voucher(4,v.id).discount_value==25
    before=facts(db_path);monkeypatch.setattr(c.vouchers,'update',lambda _:False)
    with pytest.raises(ConflictError):c.update_voucher(4,v.id,f)
    assert facts(db_path)==before
    assert client.post(f'/admin/vouchers/{v.id}/archive').status_code==303
    with pytest.raises(ValidationError):c.create_voucher(4,f)
    conn.close()


@pytest.mark.parametrize('operation',['register','profile','address','staff_create','staff_update','active','voucher_create','voucher_update','archive_one','archive_batch'])
def test_supporting_commit_failure_rolls_back(db_path,operation):
    setup=connect(db_path)
    if operation.startswith('archive'):
        o=place(setup).order
        setup.execute("UPDATE orders SET state='CANCELLED',closed_at='2026-01-01T00:00:00+00:00' WHERE id=?",(o.id,))
    setup.close();before=facts(db_path)
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON');conn.fault='COMMIT'
    a=AccountController(conn);s=UserAdminController(conn);v=VoucherController(conn);archive=OrderArchiveController(conn)
    calls={
      'register':lambda:a.register(registration()),'profile':lambda:a.update_profile(1,registration()),
      'address':lambda:a.add_address(1,dict(label='Hotel',full_address='123 Test Road',district='District 1')),
      'staff_create':lambda:s.create_staff(4,dict(username='new.staff',password='abcdef',display_name='New Staff',role='SHIPPER')),
      'staff_update':lambda:s.update_user(4,3,dict(display_name='Changed Shipper')),
      'active':lambda:s.set_active(4,3,False),'voucher_create':lambda:v.create_voucher(4,voucher_form()),
      'voucher_update':lambda:v.update_voucher(4,1,voucher_form()),
      'archive_one':lambda:archive.archive_order(4,o.id),'archive_batch':lambda:archive.archive(4,'2026-10-26')}
    with pytest.raises(sqlite3.OperationalError,match='COMMIT'):calls[operation]()
    assert not conn.in_transaction;conn.close();assert facts(db_path)==before


def test_registration_partial_insert_and_stale_dao_updates(db_path,monkeypatch):
    conn=connect(db_path);c=AccountController(conn);before=facts(db_path)
    def fail(_):raise sqlite3.IntegrityError('customer insert failure')
    monkeypatch.setattr(c.customers,'insert',fail)
    with pytest.raises(sqlite3.IntegrityError):c.register(registration())
    assert facts(db_path)==before
    user=c.users.get_by_id(1);user.id=999
    with pytest.raises(StaleWriteError):c.users.update(user)
    profile=c.customers.get_by_user_id(1);profile.user_id=999
    with pytest.raises(StaleWriteError):c.customers.update(profile)
    assert facts(db_path)==before;conn.close()


@pytest.mark.parametrize('state',['DELIVERED','DELIVERY_FAILED','REJECTED','CANCELLED'])
def test_per_id_archive_preserves_children_receipt_and_history(client,db_path,state):
    conn=connect(db_path);o=place(conn).order
    conn.execute('UPDATE orders SET state=?,closed_at=? WHERE id=?',(state,'2026-10-25T01:00:00+00:00',o.id))
    before=facts(db_path);login(client,'admin')
    assert client.post(f'/admin/archive/{o.id}').status_code==303
    after=facts(db_path)
    assert conn.execute('SELECT archived_at FROM orders WHERE id=?',(o.id,)).fetchone()[0]
    for table in before:
        if table!='orders':assert after[table]==before[table]
    assert o.id in [x.id for x in OrderArchiveController(conn).list_archived(4)]
    history=client.get(f'/admin/archive/{o.id}')
    assert history.status_code==200 and b'Refund owed' in history.data and b'Pho bo tai' in history.data
    assert not OrderArchiveController(conn).orders.list_for_customer(1)
    before=facts(db_path)
    response=client.post(f'/admin/archive/{o.id}',follow_redirects=True)
    assert response.status_code==200 and b'Only a closed, unarchived order' in response.data
    assert facts(db_path)==before
    login(client,'customer');assert client.get(f'/order/{o.id}/receipt').status_code==200
    conn.close()


def test_archive_open_missing_and_zero_row_refusal(db_path,monkeypatch):
    conn=connect(db_path);o=place(conn).order;c=OrderArchiveController(conn);before=facts(db_path)
    with pytest.raises(ConflictError):c.archive_order(4,o.id)
    with pytest.raises(NotFoundError):c.archive_order(4,999)
    monkeypatch.setattr(c.orders,'archive_one',lambda *args:False)
    with pytest.raises(ConflictError):c.archive_order(4,o.id)
    assert facts(db_path)==before;conn.close()


def test_profile_second_save_failure_rolls_back_and_http_stale_is_controlled(client,db_path,monkeypatch):
    conn=connect(db_path);c=AccountController(conn);before=facts(db_path)
    def stale(_):raise StaleWriteError('The account changed; reload and retry.')
    monkeypatch.setattr(c.users,'update',stale)
    with pytest.raises(StaleWriteError):c.update_profile(1,registration())
    assert not conn.in_transaction and facts(db_path)==before
    monkeypatch.setattr(UserDAO,'update',lambda self,user:stale(user))
    login(client,'customer')
    assert client.post('/account',data=registration()).status_code==409
    assert facts(db_path)==before;conn.close()


def test_archive_populated_aggregate_keeps_delivery_offer_refund_receipt_and_report(client,db_path):
    from .test_p4_kitchen import oracle_order,offer_for
    from saigonbite.business.controllers import KitchenController,OrderTrackingController,DeliveryController,ReportController
    conn=connect(db_path);o=oracle_order(conn,True);offer=offer_for(conn,o)
    OrderTrackingController(conn).answer_replacement(1,o.id,offer.id,True)
    kitchen=KitchenController(conn);kitchen.confirm_order(2,o.id);kitchen.start_preparing(2,o.id);kitchen.mark_ready(2,o.id)
    delivery=DeliveryController(conn);delivery.pick_up(3,o.id);delivery.confirm_delivered(3,o.id,None)
    before=facts(db_path);login(client,'admin')
    assert client.post(f'/admin/archive/{o.id}').status_code==303
    after=facts(db_path)
    for table in ('order_line','payment','delivery','replacement_offer'):assert before[table]==after[table] and after[table]
    history=client.get(f'/admin/archive/{o.id}').get_data(as_text=True)
    assert 'Accepted' in history and 'Delivered' in history and 'Refund owed' in history and '10,000 VND' in history
    assert OrderArchiveController(conn).orders.list_for_customer(1)==[]
    login(client,'customer');receipt=client.get(f'/order/{o.id}/receipt')
    assert receipt.status_code==200 and b'90,000 VND' in receipt.data and b'10,000 VND' in receipt.data
    day=ReportController(conn)._today_vn();report=ReportController(conn).sales_report(5,day,day)
    assert report.totals.orders==1 and report.totals.total==90000 and report.totals.refunds_owed==10000
    conn.close()
