"""Root-only adoption of the completed Wave 1 request bundle.
Author: 722I0004 · AI-assisted (Codex). Never imports/executes the app.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,collections,csv,hashlib,importlib.util,json,subprocess,sys,zipfile
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[3];B=R.parent/'Part2';D=R/'docs/part2/design';N=B/'notes/P3-root'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['snapshot','adopt']);a=p.parse_args()
    assert read(N/'CURRENT_STATE.json').get('barrier_released') is True,'All four successful final reports are required'
    if a.mode=='snapshot':
        target=B/'notes/P3_trash/wave1_preintegration.zip';assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True)
        paths=[p for p in (R/'models').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
        paths += [p for base in [D,R/'docs/part2/UC-01',R/'docs/part2/UC-02',R/'docs/part2/UC-03',R/'docs/part2/UC-04',R/'docs/part2/UC-05',R/'docs/part2/UC-06'] for p in base.glob('*') if p.is_file()]
        paths += [p for p in (R/'docs/part2/report').glob('*.md') if p.name.startswith(('III_','IV_'))]
        paths += [R/f'docs/part2/_agent_reports/P3-{x}.md' for x in 'ABCD']
        paths=sorted(set(paths));records=[]
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for path in paths:z.write(path,path.relative_to(R));records.append({'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        dump(N/'wave1_preintegration_manifest.json',{'author':'722I0004 · AI-assisted (Codex)','at_utc':datetime.now(timezone.utc).isoformat(),'archive':str(target),'files':records});print('Preserved pre-integration files:',len(records));return
    assert (B/'notes/P3_trash/wave1_preintegration.zip').is_file()
    annotations=read(D/'design_annotations.json');inventory=read(D/'code_inventory.json')
    def put(cls,name,ids,phase,reason,kind='method',**kwargs):
        values=annotations['elements'].setdefault(cls,[]);item=next((v for v in values if v['name']==name and v.get('kind','method')==kind),None)
        if item is None:item={'name':name,'kind':kind,'status':'P4-TARGET'};values.append(item)
        item.update(P4_input=ids,P4_subphase=phase,reason=reason,**kwargs)
    put('Quote','fingerprint','F-07','P4.3','Bind all consent fields with pure-domain enum inputs; the controller adapts PaymentChoice.',signature='fingerprint(self, payment_method: PaymentMethod, online_option: Optional[OnlineOption] = None) -> str',status='GAP')
    put('controllers.common','release_payment','F-02; P2-S01; P3-S03','P4.4','Persist full captured C as refund_amount together with state; changing only the domain object does not save the amount. Check conditional save results in the same transaction.')
    put('domain.rules','distance_km','F-04','P4.3','Return raw Haversine distance for radius and fee decisions; round only display/storage after checks.')
    put('data_access.database','connect','P2-S12','P4.1 / P6','Apply the required per-connection WAL/NORMAL/foreign-key/busy-timeout configuration; timeout=10 already exists.')
    put('data_access.database','immediate_transaction','P2-S13; P3-S03','P4.1','Rollback and surface a controlled failure for BEGIN/write/COMMIT failures; current COMMIT occurs outside its except block.')
    put('ReportDAO','top_items','F-09','P4.8','Select and group by menu_item_id; snapshot name is a label, never the grouping identity.')
    put('SalesReport','top_items','F-09','P4.8','Carry (menu_item_id, snapshot_name, quantity, revenue) through the controller and presentation.',kind='attribute',type='list[tuple[int, str, int, int]]',visibility='+',annotated=True)
    sales=next(x for x in annotations['elements']['ReportController'] if x['name']=='sales_report')
    if 'Carry menu_item_id into' not in sales['reason']:sales['reason']+=' Carry menu_item_id into SalesReport.top_items and presentation.'
    for name,ids,phase,reason in [('confirm','F-07; P2-S05','P4.3','Bind the posted fingerprint/payment choice to the target confirm method; retain controlled results through COMMIT.'),('quote','F-07','P4.3','Pass payment choice into target quoting and render the full fingerprint.')]:put('order',name,ids,phase,reason)
    for name,ids,phase,reason in [('hubs','P3-S02','P4.2','Read optional includeArchived and pass it to the target controller parameter.'),('catalogue','P2-S14','P4.6','Delegate the composite catalogue request to list_catalogue.'),('hub_menu','P2-S14','P4.6','Delegate optional hub catalogue projection to list_catalogue.'),('list_item','P2-S15','P4.6','Pass initial available into one atomic listing insert.')]:put('admin',name,ids,phase,reason)
    put('reports','sales','F-09','P4.8','Render the new identity-preserving top-items shape; template unpacking must retain the item identity.')
    phases={'AccountController':'P4.7','VoucherController':'P4.7','UserAdminController':'P4.7','OrderArchiveController':'P4.7','PlaceOrderController':'P4.3','OrderTrackingController':'P4.4','KitchenController':'P4.4','DeliveryController':'P4.5','HubController':'P4.2','MenuController':'P4.6'}
    for module in inventory['modules'].values():
        for cls in module['classes']:
            if cls['name'] not in phases:continue
            for method in cls['methods']:
                if method['immediate_transaction'] and not any(e['name']==method['name'] for e in annotations['elements'].get(cls['name'],[])):put(cls['name'],method['name'],'P2-S13; P3-S03','P4.1 + '+phases[cls['name']],'Controlled commit/busy handling is inherited from the target transaction helper; check conditional update outcomes.')
    annotations.setdefault('class_annotations',{})['HubMenuItem']={'association_class':True,'association_class_note':'Association class of Hub and MenuItem; one hub_menu_item row per pair, with independent is_available.'}
    explicit=[('controllers.common','Order','C0 order.move_to via typed Order parameter'),('controllers.common','Payment','C0 payment.release_for_unfulfilled_order'),('PlaceOrderController','Hub','C0 hub.distance_to'),('PlaceOrderController','Voucher','C0 voucher.problem / discount_for'),('PlaceOrderController','domain.rules','C0 fee / quiet / busy rule calls'),('OrderTrackingController','Order','C0 order.replace_line'),('KitchenController','Order','C0 order.line'),('DeliveryController','Delivery','C0 local delivery.move_to'),('DeliveryController','Payment','C0 local payment.move_to in confirm_delivered'),('Quote','PaymentMethod','Pure-domain fingerprint parameter'),('Quote','OnlineOption','Pure-domain fingerprint parameter'),('MenuController','HubMenuItem','Logical persistence responsibility mediated by MenuDAO; attribute note, not a direct Python method call')]
    for source,target,evidence in explicit:
        if not any(e['source']==source and e['target']==target for e in annotations['target_dependencies']):annotations['target_dependencies'].append({'source':source,'target':target,'kind':'dependency','status':'MATCH' if 'C0' in evidence else 'P4-TARGET' if source=='Quote' else 'MATCH','P4_input':'F-07' if source=='Quote' else 'P2-S15' if source=='MenuController' else '', 'allowed_on_layered_diagram':True,'source_evidence':evidence})
    responsibilities={'UserAccount':'Hold account identity, role, active flag and optional kitchen-hub assignment.','Address':'Hold an owned delivery location and archive flag.','Brand':'Group menu items and retain the archived brand identity.','MenuItem':'Hold current catalogue text, whole-VND price and archive flag.','Voucher':'Check date/subtotal eligibility and calculate the bounded discount.','OrderLine':'Retain item/name/price/quantity snapshots and derive the line total.','Delivery':'Hold assignment, paired lifecycle times, cash and failure outcome.','LocalCustomer':'Specialize the Customer type and permitted payment options for a local customer.','TouristCustomer':'Specialize Customer identity and permitted payment options for a tourist.','HubStatus':'Derive busy, quiet and load percentage from current load and capacity.','Authorisation':'Carry the local simulator decision, reference and message; not persisted.'}
    annotations['responsibilities'].update(responsibilities)
    spec=importlib.util.spec_from_file_location('p3_root_imports',Path(__file__).with_name('p3_design_crosscheck.py'));checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    violations=[r for r in checker.import_graph(inventory) if not r['allowed']];grouped=collections.defaultdict(list)
    for row in violations:grouped[(row['source'],row['target'])].append(row)
    annotations['import_violations']=[{'source':source,'target':target,'records':len(rows),'lines':sorted({r['line'] for r in rows}),'P4_input':'P3-S04','P4_subphase':'P4.9','status':'P4-TARGET','reason':'Strict package boundary requires explicit disposition; a type/materialisation import is not claimed to be an observed runtime failure. No mapper exception is assumed.'} for (source,target),rows in sorted(grouped.items())]
    annotations['P4_inputs']=[{'element':cls+'.'+e['name'],'P4 input':e['P4_input'],'P4 subphase':e['P4_subphase'],'reason':e['reason'],'status':e['status']} for cls,entries in annotations['elements'].items() for e in entries]
    annotations['P4_inputs'] += [{'element':e['source']+' -> '+e['target'],'P4 input':e['P4_input'],'P4 subphase':e['P4_subphase'],'reason':e['reason'],'status':e['status']} for e in annotations['import_violations']]
    dump(D/'design_annotations.json',annotations)
    dump(N/'wave1_adoption.json',{'author':'722I0004 · AI-assisted (Codex)','requests':{'R-A01':'accepted pure-domain signature','R-A02':'accepted typed receiver/dependency correction','R-A03':'accepted downward DCD filter; mapper imports remain explicit static policy findings, not runtime failures','R-A04':'accepted atomic checked amount/state persistence','R-A05':'accepted SUC guarantees without altering frozen anchors','B-1':'accepted Delivery receiver identity','B-2':'accepted identity-preserving tuple and DAO grouping','B-3':'accepted synchronized signature metadata','C-R1':'accepted mediated logical dependency, not an invented method','C-R2':'accepted association-class metadata','C-R3':'accepted literal SQL extraction; not an app defect','C-message-kinds':'accepted exact SSD/call/return/create/note semantics','D-1':'accepted P3-S04/P4.9 explicit strict-boundary disposition; no exception adopted','D-2':'accepted P2-S03/S07 P4.7; S02 P4.1; S08 resolved without a fix'},'strict_import_records':len(violations),'strict_import_module_pairs':len(grouped)})
    print('Adopted completed wave requests; strict import findings:',len(violations),'records /',len(grouped),'module pairs')
if __name__=='__main__':main()
