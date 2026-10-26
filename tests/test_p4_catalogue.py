"""UC06 meaningful CRUD, listing identity and immutable snapshots.
Author: 722I0004 · AI-assisted (Codex).
"""
import csv
import sqlite3
from pathlib import Path
import pytest
from saigonbite.business.controllers import MenuController,PlaceOrderController,ConflictError,ValidationError,NotFoundError
from saigonbite.data_access import connect
from .test_p4_foundation import facts,FaultConnection
from .conftest import login
from .p4_helpers import place


def test_real_brand_item_crud_and_composite_reader(client,db_path):
    login(client,'admin')
    assert client.post('/admin/brands',data={'name':'New brand'}).status_code==303
    conn=connect(db_path);c=MenuController(conn)
    brand=next(b for b in c.list_catalogue(4)['brands'] if b.name=='New brand')
    assert client.post(f'/admin/brands/{brand.id}',data={'name':'Renamed brand'}).status_code==303
    assert client.post('/admin/items/new',data={'brand_id':brand.id,'name':'New dish','description':'Synthetic','price':'12000'}).status_code==303
    item=next(i for i in c.list_catalogue(4)['items'] if i.name=='New dish')
    assert client.get(f'/admin/items/{item.id}').status_code==200
    assert client.post(f'/admin/items/{item.id}',data={'brand_id':brand.id,'name':'Renamed dish','description':'Updated','price':'13000'}).status_code==303
    assert c.menu.get_item(item.id).name=='Renamed dish' and c.menu.get_item(item.id).price==13000
    assert client.post(f'/admin/items/{item.id}/archive').status_code==303
    assert c.menu.get_item(item.id).archived_at
    assert client.post(f'/admin/brands/{brand.id}/archive').status_code==303
    with pytest.raises(ValidationError):c.create_brand(4,'Renamed brand')
    with pytest.raises(ConflictError):c.create_item(4,{'brand_id':str(brand.id),'name':'Other','price':'1'})
    all_view=c.list_catalogue(4);selected=c.list_catalogue(4,1)
    assert {h.id for h in all_view['hubs']}=={1,2} and set(all_view['listings'])=={1,2}
    assert selected['hub_menu'].hub.id==1 and set(selected['listings'])=={1}
    ledger=Path(__file__).resolve().parents[1]/'docs/part2/ssd_flow_membership.csv'
    with ledger.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert sum(r['operation']=='listCatalogue' for r in rows)==3
    conn.close()


def test_initial_unavailable_listing_is_atomic_and_two_hubs_independent(db_path,monkeypatch):
    conn=connect(db_path);c=MenuController(conn);statements=[];conn.set_trace_callback(statements.append)
    original=c.menu.add_listing;uncommitted_observations=[]
    def observed(hub,item,available=True):
        original(hub,item,available)
        other=connect(db_path)
        uncommitted_observations.append(other.execute('SELECT is_available FROM hub_menu_item WHERE hub_id=? AND menu_item_id=?',(hub,item)).fetchone())
        other.close()
    monkeypatch.setattr(c.menu,'add_listing',observed)
    c.list_item_at_hub(4,1,9,False)
    assert uncommitted_observations==[None]
    inserts=[x for x in statements if x.startswith('INSERT INTO hub_menu_item')]
    assert len(inserts)==1 and 'VALUES (1, 9, 0)' in inserts[0]
    assert not any(x.startswith('UPDATE hub_menu_item') for x in statements)
    assert conn.execute('SELECT is_available FROM hub_menu_item WHERE hub_id=1 AND menu_item_id=9').fetchone()[0]==0
    assert conn.execute('SELECT is_available FROM hub_menu_item WHERE hub_id=2 AND menu_item_id=9').fetchone()[0]==1
    c.set_availability(4,1,9,True);c.unlist_item_at_hub(4,1,9)
    assert conn.execute('SELECT is_available FROM hub_menu_item WHERE hub_id=2 AND menu_item_id=9').fetchone()[0]==1
    conn.close()


@pytest.mark.parametrize('case',['price_zero','negative','fraction','duplicate','bad_brand','archived_name','forged_parent','invalid_available'])
def test_catalogue_invalid_data_and_lifetime_uniqueness(db_path,case):
    conn=connect(db_path);c=MenuController(conn)
    form={'brand_id':'1','name':'New name','description':'','price':'1000'}
    if case=='archived_name':c.archive_item(4,1);form['name']='Pho bo tai'
    if case=='duplicate':form['name']='Pho bo tai'
    if case=='bad_brand':form['brand_id']='999'
    if case in ('price_zero','negative','fraction'):form['price']={'price_zero':'0','negative':'-1','fraction':'1.5'}[case]
    before=facts(db_path)
    with pytest.raises((ValidationError,ConflictError)):
        if case=='forged_parent':c.update_item(4,1,{**form,'brand_id':'2'})
        elif case=='invalid_available':c.list_item_at_hub(4,1,9,'false')
        else:c.create_item(4,form)
    assert facts(db_path)==before
    conn.close()


def test_parent_archive_excludes_active_child_and_refuses_listing(db_path):
    conn=connect(db_path);c=MenuController(conn);c.archive_brand(4,1)
    assert c.menu.get_item(1).archived_at is None
    assert not any(x.item.id==1 for x in PlaceOrderController(conn).select_hub(1,1).menu)
    before=facts(db_path)
    with pytest.raises(ConflictError):c.list_item_at_hub(4,2,1)
    with pytest.raises(ConflictError):c.set_availability(4,1,1,True)
    assert facts(db_path)==before
    conn.close()


def test_every_catalogue_mutation_preserves_old_snapshot_and_money(db_path):
    conn=connect(db_path);o=place(conn).order;c=MenuController(conn)
    before=facts(db_path)
    for mutate in [lambda:c.update_item(4,1,{'brand_id':'1','name':'New price/name','price':'99999'}),
                   lambda:c.set_availability(4,1,1,False),lambda:c.unlist_item_at_hub(4,1,1),
                   lambda:c.archive_item(4,1),lambda:c.archive_brand(4,1)]:
        mutate();after=facts(db_path)
        for table in ('orders','order_line','payment','replacement_offer','delivery'):assert after[table]==before[table]
    conn.close()


@pytest.mark.parametrize('operation',['rename_brand','archive_brand','update_item','archive_item','remove_listing','set_available'])
def test_catalogue_checked_zero_row_outcomes(db_path,monkeypatch,operation):
    conn=connect(db_path);c=MenuController(conn);before=facts(db_path)
    monkeypatch.setattr(c.menu,operation,lambda *a:False)
    commands={'rename_brand':lambda:c.rename_brand(4,1,'Changed'),'archive_brand':lambda:c.archive_brand(4,1),
        'update_item':lambda:c.update_item(4,1,{'brand_id':'1','name':'Changed','price':'1000'}),
        'archive_item':lambda:c.archive_item(4,1),'remove_listing':lambda:c.unlist_item_at_hub(4,1,1),
        'set_available':lambda:c.set_availability(4,1,1,False)}
    with pytest.raises((ConflictError,NotFoundError)):commands[operation]()
    assert facts(db_path)==before
    conn.close()


@pytest.mark.parametrize('operation',['create_brand','rename_brand','archive_brand','create_item','update_item','archive_item','list','unlist','available'])
def test_catalogue_commit_failure_no_partial_write(db_path,operation):
    conn=sqlite3.connect(db_path,isolation_level=None,factory=FaultConnection);conn.row_factory=sqlite3.Row
    c=MenuController(conn);before=facts(db_path);conn.fault='COMMIT'
    form={'brand_id':'1','name':'Changed','price':'1000'}
    commands={'create_brand':lambda:c.create_brand(4,'New brand'),'rename_brand':lambda:c.rename_brand(4,1,'Changed'),
        'archive_brand':lambda:c.archive_brand(4,1),'create_item':lambda:c.create_item(4,form),
        'update_item':lambda:c.update_item(4,1,form),'archive_item':lambda:c.archive_item(4,1),
        'list':lambda:c.list_item_at_hub(4,1,9,False),'unlist':lambda:c.unlist_item_at_hub(4,1,1),
        'available':lambda:c.set_availability(4,1,1,False)}
    with pytest.raises(sqlite3.OperationalError):commands[operation]()
    assert not conn.in_transaction and facts(db_path)==before
    conn.close()
