"""Independent hand-calculated report oracle, recorded before execution.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import hashlib,json,sqlite3
import pytest
from saigonbite.business.controllers import ReportController,AuthorizationError
from saigonbite.data_access import connect
from .test_p4_foundation import facts
from .conftest import login

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture
def oracle(db_path):
    receipt=json.loads((ROOT.parent/'Part2/notes/P4_report_oracle_preregistered.json').read_text())
    for path,digest in receipt['files'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest
    conn=connect(db_path);conn.executescript((ROOT/'tests/fixtures/report_oracle.sql').read_text(encoding='utf-8'))
    yield conn,ReportController(conn),db_path
    conn.close()


def test_sales_reduced_total_no_double_refund_multiline_and_archived_identity(oracle):
    conn,c,path=oracle;r=c.sales_report(5,'2026-10-20','2026-10-20')
    assert r.period.start_utc=='2026-10-19T17:00:00+00:00' and r.period.end_utc=='2026-10-20T17:00:00+00:00'
    assert [(x.orders,x.item_sales,x.voucher_discounts,x.delivery_fees,x.total,x.refunds_owed,x.net) for x in r.rows]==[
        (1,90000,10000,10000,90000,10000,90000),(1,60000,0,10000,70000,0,70000)]
    t=r.totals
    assert (t.orders,t.item_sales,t.voucher_discounts,t.delivery_fees,t.total,t.refunds_owed,t.net)==(2,150000,10000,20000,160000,10000,160000)
    filtered=c.sales_report(5,'2026-10-20','2026-10-20',2)
    assert filtered.hub.archived_at and filtered.totals.total==70000
    ids=[r['order_id'] for r in c.reports.finished_deliveries(r.period.start_utc,r.period.end_utc,None)]
    assert set(ids)=={101,102,107}


def test_top_items_use_id_and_latest_eligible_snapshot_name(oracle):
    conn,c,path=oracle;r=c.sales_report(5,'2026-10-20','2026-10-20')
    assert r.top_items==[(1,'Renamed snapshot',3,100000),(2,'Shared name',1,50000)]
    rows=c.reports.top_items(r.period.start_utc,r.period.end_utc,None)
    assert [r['menu_item_id'] for r in rows]==[1,2]


def test_delivery_means_sample_sizes_and_failure_denominator(oracle):
    _,c,_=oracle;r=c.delivery_report(5,'2026-10-20','2026-10-20');o=r.overall
    assert (o.delivered,o.failed,o.failure_rate,o.avg_wait,o.avg_ride)==(2,1,33.3,20.0,25.0)
    assert (len(o.waits),len(o.rides))==(3,2)
    assert [(x.delivered,x.failed,x.failure_rate,x.avg_wait,x.avg_ride) for x in r.by_hub]==[(1,0,0.0,10.0,20.0),(1,1,50.0,25.0,30.0)]
    assert len(r.by_shipper)==1 and r.by_shipper[0].rides==o.rides


def test_workload_now_retains_archived_hubs_and_empty_values(oracle):
    conn,c,_=oracle;r=c.workload_report(5)
    assert [(x.status.hub.id,x.status.load) for x in r.rows]==[(1,0),(2,1)]
    assert [{s.value:n for s,n in x.counts.items()} for x in r.rows]==[{}, {'PLACED':1}]
    # Controlled workload-only counterexamples; expected counts are literal, independent of the query.
    conn.execute("UPDATE orders SET state='READY' WHERE id=108")
    ready=c.workload_report(5).rows[1]
    assert ready.status.load==0 and ready.counts.get('READY')==1 and ready.counts.get('OUT_FOR_DELIVERY',0)==0
    conn.execute("UPDATE orders SET state='OUT_FOR_DELIVERY' WHERE id=108")
    riding=c.workload_report(5).rows[1]
    assert riding.status.load==0 and riding.counts.get('OUT_FOR_DELIVERY')==1 and riding.counts.get('READY',0)==0
    empty=c.sales_report(5,'2026-01-01','2026-01-01')
    assert empty.rows==[] and empty.top_items==[] and empty.totals.total==0
    d=c.delivery_report(5,'2026-01-01','2026-01-01').overall
    assert d.delivered==d.failed==0 and d.waits==d.rides==[]
    assert d.failure_rate is d.avg_wait is d.avg_ride is None


def test_half_open_exact_boundaries(oracle):
    conn,c,_=oracle
    conn.execute("UPDATE delivery SET finished_at='2026-10-19T17:00:00+00:00' WHERE order_id=104")
    conn.execute("UPDATE delivery SET finished_at='2026-10-20T17:00:00+00:00' WHERE order_id=103")
    assert c.sales_report(5,'2026-10-20','2026-10-20').totals.total==190000


def test_reports_actual_connection_authorizer_and_unchanged_facts(oracle):
    conn,c,path=oracle;before=facts(path);changes=conn.total_changes;attempts=[]
    writes={sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE,sqlite3.SQLITE_CREATE_TABLE,sqlite3.SQLITE_DROP_TABLE,sqlite3.SQLITE_ALTER_TABLE}
    def authorizer(action,*args):
        if action in writes:attempts.append((action,args));return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK
    conn.set_authorizer(authorizer)
    c.sales_report(5,'2026-10-20','2026-10-20');c.delivery_report(5,'2026-10-20','2026-10-20');c.workload_report(5)
    assert conn.total_changes==changes and not attempts and facts(path)==before
    conn.set_authorizer(None)


def test_report_manager_authorization_and_rendered_truth(client,oracle):
    _,c,path=oracle;before=facts(path)
    for user in (1,2,3,4):
        with pytest.raises(AuthorizationError):c.sales_report(user,'2026-10-20','2026-10-20')
    login(client,'customer');assert client.get('/reports/sales').status_code==403
    login(client,'manager');response=client.get('/reports/sales?from=2026-10-20&to=2026-10-20')
    assert response.status_code==200 and b'160,000 VND' in response.data and b'Refunds owed' in response.data
    assert b'data-item-id="1"' in response.data and b'data-item-id="2"' in response.data
    workload=client.get('/reports/workload?from=1900-01-01&to=1900-01-02&hub=1')
    assert workload.status_code==200 and b'workload-1' in workload.data and b'workload-2' in workload.data and b'(Archived)' in workload.data
    empty=client.get('/reports/delivery?from=2026-01-01&to=2026-01-01')
    assert empty.status_code==200 and b'n/a' in empty.data and b'(n=0)' in empty.data
    assert facts(path)==before


def test_report_unavailable_data_is_controlled_without_figures(client,db_path):
    conn=connect(db_path);conn.execute('DROP TABLE delivery');conn.close()
    login(client,'manager');response=client.get('/reports/sales?from=2026-10-20&to=2026-10-20')
    assert response.status_code==503 and b'Report data unavailable' in response.data
    assert b'id="sales-total"' not in response.data and b'VND' not in response.data


@pytest.mark.parametrize('hub',['abc','0','-1','999','1 OR 1=1'])
def test_invalid_report_hub_never_silently_becomes_all_hubs(client,hub):
    login(client,'manager')
    assert client.get('/reports/sales',query_string={'hub':hub}).status_code==400


def test_missing_report_relationship_never_becomes_zero_sales(client,oracle):
    conn,_,path=oracle;conn.execute('DELETE FROM payment WHERE order_id=101');before=facts(path)
    login(client,'manager');response=client.get('/reports/sales?from=2026-10-20&to=2026-10-20')
    assert response.status_code==503 and b'incomplete' in response.data and b'id="sales-total"' not in response.data
    assert facts(path)==before
