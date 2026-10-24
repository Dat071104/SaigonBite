"""Root-owned explicit responsibility and target-design annotations.
Author: 722I0004 · AI-assisted (Codex). No application execution.
"""
from pathlib import Path
import csv,json,re,collections
R=Path(__file__).resolve().parents[3];D=R/'docs/part2/design';D.mkdir(exist_ok=True)
inv=json.loads((D/'code_inventory.json').read_text(encoding='utf-8'))
classes={c['name']:c for m in inv['modules'].values() for c in m['classes']}
lookup={c['name']:{m['name']:m for m in c['methods']} for c in classes.values()}
ops={o['op_id']:o for o in csv.DictReader((R/'docs/part2/ssd_operations.csv').open(encoding='utf-8-sig',newline=''))}
members=list(csv.DictReader((R/'docs/part2/ssd_flow_membership.csv').open(encoding='utf-8-sig',newline='')))
anchors=list(csv.DictReader((R/'docs/part2/pc_mg_register.csv').open(encoding='utf-8-sig',newline='')))
annotations={'author':inv['author'],'C0':inv['commit'],'elements':{},'responsibilities':{},'associations':[],'target_dependencies':[],'P4_inputs':[]}
def target(cls,name,ids,phase,reason,signature=None,status='P4-TARGET',kind='method',type=None):
    entry={'name':name,'kind':kind,'status':status,'P4_input':ids,'P4_subphase':phase,'reason':reason}
    if signature:entry['signature']=signature
    if kind=='attribute':entry.update(type=type or 'str',visibility='+',annotated=True)
    annotations['elements'].setdefault(cls,[]).append(entry)
    annotations['P4_inputs'].append({'element':cls+'.'+name,'P4 input':ids,'P4 subphase':phase,'reason':reason,'status':status})
target('PlaceOrderController','request_quote','F-04; F-07; P3-S01','P4.3','Use raw distance; include payment choice and a full quote fingerprint; rank suggestions by load ratio, distance and ID.',"request_quote(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None) -> Quote")
target('PlaceOrderController','confirm_order','F-04; F-07; P2-S05; P2-S13','P4.3','Compare full fingerprint and T; release simulator authorization on every failure through COMMIT.',"confirm_order(self, user_id: int, hub_id: int, address_id: Optional[int], quantities: Mapping[int, str], idempotency_token: str, quoted_total: Optional[int] = None, voucher_code: Optional[str] = None, payment: Optional[PaymentChoice] = None, quote_fingerprint: Optional[str] = None) -> OrderConfirmation")
target('PlaceOrderController','suggest_hubs','P3-S01; F-04','P4.3','Draft sorts by load ratio then ID; BR-04 requires distance as the second key and raw distance for range.')
target('Quote','fingerprint','F-07','P4.3','Canonical content fingerprint binds hub, address, line IDs/quantities/prices, voucher+D, F, Q and payment choice.',"fingerprint(self, payment: PaymentChoice) -> str",status='GAP')
target('Hub','distance_to','F-04','P4.3','Keep raw Haversine precision through the radius and fee decisions; round only presentation/storage.')
target('Payment','release_for_unfulfilled_order','F-02; P2-S01','P4.4','Set refund_amount=C with REFUND_PENDING; preserve COD VOIDED; no payout operation.')
target('OrderTrackingController','answer_replacement','F-05; F-02; P2-S09; P2-S11; P2-S13','P4.4','Recheck PLACED and exact open offer; recheck target; invalid target withdraws only the offer; valid accept uses offered price; controlled rollback through COMMIT.')
for c,m in [('KitchenController','reject_order'),('OrderTrackingController','cancel_order'),('DeliveryController','report_failure')]:target(c,m,'F-02; P2-S13','P4.4 / P4.5' if c=='DeliveryController' else 'P4.4','BR-17 full C refund owed and atomic state/amount writes, including COMMIT rollback.')
target('KitchenController','offer_replacement','F-05; P2-S09; P2-S13','P4.4','Require currently unavailable source; target active/listed/available; one open offer; check every conditional save result.')
target('ReportController','sales_report','F-03; F-09','P4.8','Expose T without subtracting refund owed twice; top items retain menu_item_id identity.')
target('ReportController','workload_report','P2-S18','P4.8','Use all retained hub identities, including archived hubs with zero open work.')
target('SalesRow','net','F-03','P4.8','Return total T; refunds_owed is disclosed separately.')
target('HubController','list_hubs','P3-S02','P4.2','Honor optional includeArchived explicitly; draft always includes archived hubs.',"list_hubs(self, user_id: int, include_archived: bool = True) -> list[HubAdminView]")
target('MenuController','list_catalogue','P2-S14','P4.6','One public SSD operation composes catalogue, all hubs, and optional hub listings; retain catalogue/hub_menu as helpers.',"list_catalogue(self, user_id: int, hub_id: Optional[int] = None) -> dict[str, object]",status='GAP')
target('MenuController','list_item_at_hub','P2-S15; P2-S13','P4.6','Insert the requested initial availability in the same transaction.',"list_item_at_hub(self, user_id: int, hub_id: int, item_id: int, available: bool = True) -> None")
target('MenuDAO','add_listing','P2-S15','P4.6','Set available in the INSERT, never as a second independently committed operation.',"add_listing(self, hub_id: int, item_id: int, available: bool = True) -> None")
target('OrderDAO','save_lines_and_totals','P2-S09; P2-S11; P3-S03','P4.4','Apply replacement only to expected PLACED order and check each affected line/header rowcount.',"save_lines_and_totals(self, order: Order) -> bool")
target('PaymentDAO','set_amounts','F-02; P3-S03','P4.4','Persist full/partial refund obligations atomically and expose the conditional save outcome.',"set_amounts(self, order_id: int, amount: int, refund_amount: int, now: str) -> bool")
target('OrderArchiveController','archive_order','P2-S06','P4.7','Minimal per-ID closed-order archive preserves history and child rows; existing batch operation remains separately named.',"archive_order(self, user_id: int, order_id: int) -> Order",status='GAP')
target('OrderDAO','archive_one','P2-S06','P4.7','Conditional per-ID terminal archive; return whether exactly one row changed.',"archive_one(self, order_id: int, now: str) -> bool",status='GAP')
for cls in ['HubController','MenuController','KitchenController','DeliveryController']:
    for method in classes[cls]['methods']:
        if method['immediate_transaction'] and not any(x['name']==method['name'] for x in annotations['elements'].get(cls,[])):
            target(cls,method['name'],'P2-S13; P3-S03','P4.1 + '+{'HubController':'P4.2','MenuController':'P4.6','KitchenController':'P4.4','DeliveryController':'P4.5'}[cls],'Guarded writes must check rowcount and handle busy / commit failure without partial effects; shared helper is currently incomplete.')
target('UserAccount','created_at','P2-S02','P4.1','Required by schema contract; missing from code and SQL at C0.',status='GAP',kind='attribute',type='str')
for key,text in {'Order':'Own the order lifecycle, snapshots and accepted replacement totals.','Payment':'Hold captured amount C and refund obligations without claiming payout.','Quote':'Compute and bind the complete consented price; not persisted.','Hub':'Represent a kitchen location, capacity and fee.','HubMenuItem':'Represent one hub listing and its independent availability.','ReplacementOffer':'Hold one proposed whole-line replacement and its decision history.','Customer':'Represent customer identity and permitted online payment choices.','ReportController':'Authorize Manager requests and construct operational reports without writes.','order':'Translate authenticated customer routes and render quote, receipt and order results.','admin':'Translate administrator maintenance routes; never provide business decisions.','delivery':'Translate shipper requests and render contact and cash information.','kitchen':'Translate own-hub kitchen actions and render their results.','reports':'Translate Manager filters and render read-only report results.'}.items():annotations['responsibilities'][key]=text
def assoc(a,b,ma,mb,role,kind='association',nav=True):annotations['associations'].append({'source':a,'target':b,'source_multiplicity':ma,'target_multiplicity':mb,'role':role,'kind':kind,'navigable':nav,'status':'MATCH','evidence':'domain model 2.1.7; code identifiers / typed fields'})
for args in [('Customer','UserAccount','0..1','1','linked account'),('Customer','Address','1','0..*','owns'),('Hub','HubMenuItem','1','0..*','listings'),('HubMenuItem','MenuItem','0..*','1','item'),('Brand','MenuItem','1','0..*','offers'),('Order','Customer','0..*','1','customer'),('Order','Hub','0..*','1','hub'),('Order','Address','0..*','1','address'),('Order','Voucher','0..*','0..1','voucher'),('Order','OrderLine','1','1..*','lines','composition'),('Order','Payment','1','1','payment'),('Order','Delivery','1','0..1','delivery'),('Order','ReplacementOffer','1','0..*','offers'),('ReplacementOffer','OrderLine','0..*','1','for line'),('ReplacementOffer','MenuItem','0..*','1','target item'),('OrderLine','MenuItem','0..*','1','snapshot source'),('Delivery','UserAccount','0..*','0..1','assigned shipper'),('UserAccount','Hub','0..*','0..1','kitchen hub')]:assoc(*args)
for child in ['LocalCustomer','TouristCustomer']:assoc(child,'Customer','1','1','is a','generalization')
for a,b in [('PlaceOrderController','Quote'),('MenuController','MenuDAO'),('OrderArchiveController','OrderDAO')]:annotations['target_dependencies'].append({'source':a,'target':b,'kind':'dependency','status':'P4-TARGET','P4_input':'F-07' if b=='Quote' else 'P2-S14' if a=='MenuController' else 'P2-S06','allowed_on_layered_diagram':True})
mapping={
'OP-13':('order.choose_hub','PlaceOrderController.list_hubs'), 'OP-14':('order.choose_items','PlaceOrderController.select_hub'),'OP-15':('order.quote','PlaceOrderController.request_quote'),'OP-01':('order.confirm','PlaceOrderController.confirm_order'),'OP-16':('order.detail','OrderTrackingController.get_order'),'OP-17':('order.my_orders','OrderTrackingController.list_my_orders'),'OP-07':('order.cancel','OrderTrackingController.cancel_order'),
'OP-19':('kitchen.board','KitchenController.board'),'OP-20':('kitchen.order','KitchenController.get_order'),'OP-02':('kitchen.confirm','KitchenController.confirm_order'),'OP-03':('kitchen.reject','KitchenController.reject_order'),'OP-04':('kitchen.offer','KitchenController.offer_replacement'),'OP-18':('order.detail','OrderTrackingController.get_order'),'OP-05':('order.answer_replacement','OrderTrackingController.answer_replacement'),'OP-06':('order.answer_replacement','OrderTrackingController.answer_replacement'),
'OP-21':('delivery.board','DeliveryController.board'),'OP-22':('delivery.detail','DeliveryController.get_delivery'),'OP-10':('delivery.pick_up','DeliveryController.pick_up'),'OP-11':('delivery.delivered','DeliveryController.confirm_delivered'),'OP-12':('delivery.failed','DeliveryController.report_failure'),
'OP-26':('reports.sales','ReportController.sales_report'),'OP-27':('reports.workload','ReportController.workload_report'),'OP-28':('reports.delivery','ReportController.delivery_report'),
'OP-23':('admin.hubs','HubController.list_hubs'),'OP-24':('admin.edit_hub','HubController.get_hub'),'OP-34':('admin.new_hub','HubController.create_hub'),'OP-35':('admin.edit_hub','HubController.update_hub'),'OP-36':('admin.archive_hub','HubController.archive_hub'),
'OP-25':('admin.catalogue; admin.hub_menu','MenuController.list_catalogue'),'OP-37':('admin.create_brand','MenuController.create_brand'),'OP-38':('admin.rename_brand','MenuController.rename_brand'),'OP-39':('admin.archive_brand','MenuController.archive_brand'),'OP-40':('admin.new_item','MenuController.create_item'),'OP-41':('admin.edit_item','MenuController.update_item'),'OP-42':('admin.archive_item','MenuController.archive_item'),'OP-43':('admin.list_item','MenuController.list_item_at_hub'),'OP-44':('admin.hub_item_availability','MenuController.set_availability'),'OP-45':('admin.unlist_item','MenuController.unlist_item_at_hub')}
route_lookup={route['blueprint']+'.'+route['view_function']:route for m in inv['modules'].values() for route in m['routes']}
def closure(cls,method,seen=None):
    seen=set() if seen is None else seen
    if (cls,method) in seen:return set(),set()
    seen.add((cls,method));m=lookup.get(cls,{}).get(method);dao=set();domain=set()
    if not m:return dao,domain
    attrs={a['name']:a['type'] for a in classes[cls]['attributes']}
    for call in m['calls']:
        parts=call['target'].split('.')
        if len(parts)>2 and parts[0]=='self' and attrs.get(parts[1],'').endswith('DAO'):dao.add(attrs[parts[1]]+'.'+parts[2])
        elif len(parts)==2 and parts[0]=='self':
            subdao,subdomain=closure(cls,parts[1],seen);dao|=subdao;domain|=subdomain
        elif len(parts)==2 and parts[0] in classes and not parts[0].endswith('DAO'):domain.add(parts[0]+'.'+parts[1])
    dao.add('UserDAO.get_by_id') if cls!='PlaceOrderController' or method!='list_hubs' else None
    return dao,domain
domain_extra={'OP-13':['HubStatus.busy','HubStatus.quiet'],'OP-14':['HubStatus.busy'],'OP-15':['Hub.distance_to','Voucher.problem','Voucher.discount_for','Quote.fingerprint','Quote.total'],'OP-01':['Hub.distance_to','Quote.fingerprint','Order.place','PaymentGatewaySimulator.authorise','PaymentGatewaySimulator.release'],'OP-02':['Order.move_to'],'OP-03':['Order.move_to','Payment.release_for_unfulfilled_order'],'OP-04':['Order.line'],'OP-05':['Order.replace_line','Order.total'],'OP-06':['Order.move_to','Payment.release_for_unfulfilled_order'],'OP-07':['Order.move_to','Payment.release_for_unfulfilled_order'],'OP-10':['Order.move_to'],'OP-11':['Payment.move_to','Delivery.move_to','Order.move_to'],'OP-12':['Delivery.move_to','Order.move_to','Payment.release_for_unfulfilled_order'],'OP-26':['SalesRow.add','SalesRow.net'],'OP-27':['HubStatus.busy','HubStatus.quiet'],'OP-28':['DeliveryRow.failure_rate','DeliveryRow.avg_wait','DeliveryRow.avg_ride'],'OP-18':['OrderDetail.total_if_accepted']}
rows=[];occ=collections.Counter()
for membership in members:
    oid=membership['catalogue_id'];uc=membership['UC'];op=ops[oid];view,method=mapping[oid];cls,meth=method.split('.');base=lookup.get(cls,{}).get(meth,{});entry=next((x for x in annotations['elements'].get(cls,[]) if x['name']==meth),None)
    dao,domain=closure(cls,meth);domain|=set(domain_extra.get(oid,[]));status=entry['status'] if entry else 'MATCH';ids=entry['P4_input'] if entry else '';notes=[]
    if 'Order.move_to' in domain:dao.add('OrderDAO.change_state')
    if 'Payment.release_for_unfulfilled_order' in domain:dao|={'PaymentDAO.get_by_order_id','PaymentDAO.change_state','PaymentDAO.set_amounts'}
    # Include each DAO's own helper reads (e.g. OrderDAO._load -> order_line).
    for ref in list(dao):
        dc,dm=ref.split('.');todo=[dm];seen=set()
        while todo:
            method_name=todo.pop()
            if method_name in seen:continue
            seen.add(method_name)
            for call in lookup.get(dc,{}).get(method_name,{}).get('calls',[]):
                if call['target'].startswith('self.') and len(call['target'].split('.'))==2:
                    helper=call['target'].split('.')[1]
                    if helper in lookup.get(dc,{}):dao.add(dc+'.'+helper);todo.append(helper)
    if oid=='OP-25':dao|={'MenuDAO.list_brands','MenuDAO.list_items','HubDAO.list_all','MenuDAO.list_hub_items'};notes.append('Composite wrapper proposed; one optional hubId; no separate public SSD op added.')
    if oid=='OP-43':dao.add('MenuDAO.add_listing');notes.append('Initial available flag written by INSERT atomically (P2-S15).')
    if oid=='OP-41':notes.append('brandId is current-parent context in form; update_item pins current.brand_id; no reparenting.')
    if oid=='OP-16':status='P4-TARGET';ids='F-06';notes.append('Read method is present; receipt wording must say refund owed, not paid out.')
    if oid=='OP-06':status='P4-TARGET';ids='F-02; P2-S13'
    if oid=='OP-18':status='P4-TARGET';ids='F-06';notes.append('Preview is OrderDetail.total_if_accepted; all money is owed, not refunded.')
    if oid=='OP-26':dao|={'ReportDAO.sales_by_hub','ReportDAO.top_items'}
    if oid=='OP-27':dao.discard('HubDAO.list_active');dao.add('HubDAO.list_all')
    if oid=='OP-15':notes.append('Payment method/online option adapt to PaymentChoice; user_id comes from authenticated context.')
    if oid=='OP-01':notes.append('checkoutToken→idempotency_token; quoteFingerprint→quote_fingerprint; lines→quantities; payment fields→PaymentChoice. Simulator choice precedes transaction.')
    if oid in ('OP-05','OP-06'):notes.append('accept is '+('True' if oid=='OP-05' else 'False')+'; same answer_replacement receiver, separate SSD operation.')
    tx='BEGIN IMMEDIATE' if base.get('immediate_transaction') else 'read'
    tables={}
    for ref in sorted(dao):
        dc,dm=ref.split('.');dmeth=lookup.get(dc,{}).get(dm,{})
        for statement in dmeth.get('sql',[]):
            for table in statement['tables']:tables.setdefault(table,set()).update('W' if any(k in statement['kinds'] for k in ('INSERT','UPDATE','DELETE')) else 'R')
    ensured=[a['id'] for a in anchors if a['UC']==uc and membership['operation'] in [s.strip() for s in a['ssd op'].split(';')]]
    routes=[]
    for v in view.split('; '):
        rt=route_lookup[v];routes.append(v+', '+('/'.join(rt['methods']))+' '+rt['rule'])
    occ[(uc,oid)]+=1;notes.append('SSD occurrence: '+membership['SSD message'])
    signature=entry.get('signature',base.get('signature','')) if entry else base.get('signature','')
    row={'op_id':oid,'operation':membership['operation'],'UC':uc,'view function (blueprint.function, METHOD /rule)':' ; '.join(routes),'controller.method(signature)':cls+'.'+signature,'domain calls':'; '.join(sorted(domain)) or 'Construct/read typed values; no domain behavior call','DAO calls':'; '.join(sorted(dao)),'tables R/W':'; '.join(f'{t}:{"/".join(sorted(m))}' for t,m in sorted(tables.items())),'transaction (none | read | BEGIN IMMEDIATE)':tx,'PC/MG ensured':'; '.join(ensured) or 'Read authorization / no persistent effect; named main anchors remain on their realizing write/report operation','status':status,'P4 input':ids,'note':' '.join(notes)};rows.append(row)
with (D/'operation_realisation.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
annotations['count_interpretation']={'membership_rows':len(members),'distinct_UC_operation_pairs':len({(m['UC'],m['operation']) for m in members}),'UC06_occurrences':12,'UC06_distinct_operations':10,'resolution':'Preserve all 41 SSD occurrences: listCatalogue occurs separately in UC06 SSD Parts A/B/C, with three design-sequence views. The 39 distinct UC/operation pairs are never misreported as 41 distinct operations.'}
(D/'design_annotations.json').write_text(json.dumps(annotations,indent=2,ensure_ascii=False),encoding='utf-8')
print('Responsibilities:',len(rows),'rows;',dict(collections.Counter(r['status'] for r in rows)))
