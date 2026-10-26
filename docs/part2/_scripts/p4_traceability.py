"""Semantic, exact-ID P4 trace repair. Historical P3 generators are untouched.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import csv,io,json,re,hashlib,argparse
R=Path(__file__).resolve().parents[3];D=R/'docs/part2'

# Explicit requirement decisions, reviewed against the source prose; never ordinal joins.
METHODS={
'FR-01':'AccountController.register',
'FR-02':'AccountController.get_profile;AccountController.update_profile;AccountController.add_address;AccountController.update_address;AccountController.archive_address',
'FR-03':'AuthController.authenticate;AuthController.get_user;UserAdminController.set_active;auth.logout',
'FR-04':'PlaceOrderController.list_hubs;PlaceOrderController.select_hub;MenuController.list_catalogue;KitchenController.set_availability',
'FR-05':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order',
'FR-06':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order;HubController.update_hub;ReportController.workload_report',
'FR-07':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order',
'FR-08':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order;ReportController.workload_report',
'FR-09':'VoucherController.create_voucher;VoucherController.update_voucher;PlaceOrderController.request_quote',
'FR-10':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order',
'FR-11':'PlaceOrderController.request_quote;PlaceOrderController.confirm_order',
'FR-12':'PlaceOrderController.payment_options;PlaceOrderController.confirm_order;DeliveryController.confirm_delivered',
'FR-13':'PlaceOrderController.confirm_order',
'FR-14':'PlaceOrderController.confirm_order',
'FR-15':'OrderTrackingController.list_my_orders;OrderTrackingController.get_order',
'FR-16':'OrderTrackingController.get_order;order.receipt',
'FR-17':'OrderTrackingController.cancel_order',
'FR-18':'DeliveryController.board;DeliveryController.get_delivery;DeliveryController.pick_up',
'FR-19':'DeliveryController.pick_up',
'FR-20':'DeliveryController.confirm_delivered',
'FR-21':'DeliveryController.report_failure',
'FR-22':'HubController.create_hub;HubController.update_hub;HubController.archive_hub;HubController.list_hubs',
'FR-23':'ReportController.workload_report',
'FR-24':'ReportController.sales_report',
'FR-25':'ReportController.delivery_report',
'FR-26':'KitchenController.board;KitchenController.get_order;KitchenController.confirm_order;KitchenController.reject_order',
'FR-27':'KitchenController.confirm_order;KitchenController.reject_order',
'FR-28':'KitchenController.offer_replacement',
'FR-29':'KitchenController.offer_replacement;OrderTrackingController.get_order;OrderTrackingController.answer_replacement',
'FR-30':'KitchenController.confirm_order;KitchenController.start_preparing',
'FR-31':'OrderTrackingController.answer_replacement',
'FR-32':'OrderTrackingController.answer_replacement',
'FR-33':'OrderTrackingController.answer_replacement',
'FR-34':'KitchenController.start_preparing;KitchenController.mark_ready',
'FR-35':'KitchenController.set_availability;MenuController.set_availability',
'FR-36':'MenuController.create_brand;MenuController.rename_brand;MenuController.archive_brand;MenuController.create_item;MenuController.update_item;MenuController.archive_item',
'FR-37':'MenuController.list_item_at_hub;MenuController.unlist_item_at_hub;MenuController.set_availability',
'FR-38':'VoucherController.list_vouchers;VoucherController.create_voucher;VoucherController.update_voucher;VoucherController.archive_voucher',
'FR-39':'UserAdminController.create_staff;UserAdminController.update_user;UserAdminController.set_active;UserAdminController.get_customer',
'FR-40':'OrderArchiveController.archive_order;OrderArchiveController.archived_history',
'NFR-01':'auth.role_required;AuthController.get_user',
'NFR-02':'PlaceOrderController.confirm_order',
'NFR-03':'database.connect;database.immediate_transaction',
'NFR-04':'create_app (local configuration only; P7 deployment pending)',
'NFR-05':'KitchenController.board;DeliveryController.board;UserAdminController.get_customer',
'NFR-06':'security.init_csrf',
'NFR-07':'_production_config',
'NFR-08':'_production_config (cookie configuration only; P7 HTTPS pending)',
'NFR-09':'presentation/templates (P5/P6 phone-width evidence pending)',
'NFR-10':'p4_architecture_audit.inventory (BLOCKED P4-B02)',
'NFR-11':'OrderArchiveController.archive_order;OrderArchiveController.archived_history;ReportController.sales_report',
'NFR-12':'PlaceOrderController.confirm_order;DeliveryController.pick_up;OrderTrackingController.answer_replacement;database.immediate_transaction',
}


def tokens(value):
    return set(re.findall(r'(?<![A-Z0-9])(?:UC\d{2}-(?:PC|MG)\d{2}|SUC\d{2}-PC\d{2})(?![A-Z0-9])',value))


def validate(rows):
    errors=[]
    if {r['Req ID'] for r in rows}!=set(METHODS) or len(rows)!=52:errors.append('Requirement ID set differs')
    for row in rows:
        req=row['Req ID'];expected=set(METHODS.get(req,'').split(';'));actual=set(row['code method'].split(';'))
        if actual!=expected:errors.append(req+': semantic code mismatch')
        for method in expected:
            if method not in row['design operation']:errors.append(req+': design mismatch '+method)
    return errors


def build():
    current=list(csv.DictReader((D/'traceability.csv').open(encoding='utf-8-sig',newline='')))
    original=json.loads((D/'implementation/p4_traceability_negative_evidence.json').read_text(encoding='utf-8'))
    anchors={r['id'] for r in csv.DictReader((D/'pc_mg_register.csv').open(encoding='utf-8-sig'))}
    suc_text=(D/'SUC.md').read_text(encoding='utf-8');anchors|=tokens(suc_text)
    ops=list(csv.DictReader((D/'design/operation_realisation.csv').open(encoding='utf-8-sig')))
    audit=[]
    for row in current:
        req=row['Req ID'];named=tokens(row['PC/MG ID']);assert named<=anchors,(req,named-anchors)
        methods=METHODS[req].split(';');main=named & {a for a in anchors if a.startswith('UC')}
        supporting=named-main
        # Exact complete tokens only. Operation occurrences are retained separately, not deduplicated.
        matches=[o for o in ops if tokens(o['PC/MG ensured']) & main and any(o['controller.method(signature)'].startswith(m+'(') for m in methods)]
        references=[f"{o['UC']} {o['op_id']} {o['operation']}: {o['note']}" for o in matches]
        scope='Supporting contract; no standalone main-UC diagram claimed' if supporting and not main else 'Exact main-anchor operation join; supporting contracts retained where present'
        row['code method']=';'.join(methods)
        row['design operation']='; '.join(methods)+'; '+scope+('; '+'; '.join(references) if references else '')
        row['screen/control']='; '.join(sorted({o['view function (blueprint.function, METHOD /rule)'] for o in matches})) or 'Supporting routes/contracts; see implementation/p4_route_inventory.json'
        row['test ID']='';row['result evidence']='P4 evidence binding pending final suite; no completion inferred'
        row['status']='Planned' if req in ('NFR-04','NFR-09') else 'Analysed'
        audit.append(dict(req_id=req,uc_suc=row['UC/SUC'],complete_pc_mg_tokens=';'.join(sorted(named)),
            selected_methods=';'.join(methods),matching_operation_occurrences=len(matches),
            scope=scope,semantic_disposition='REPAIRED; P4-B02 architecture remains blocked' if req=='NFR-10' else 'AUDITED_SCOPED_MAPPING',
            later_phase_limit='P5/P6/P7 evidence remains pending' if req in ('NFR-03','NFR-04','NFR-05','NFR-08','NFR-09') else ''))
    assert not validate(current)
    # All three preserved mistakes must be rejected even if their nonempty link counts look valid.
    negative=[]
    for example in original['examples']:
        bad=[dict(r) for r in current];target=next(r for r in bad if r['Req ID']==example['Req ID'])
        target['design operation']=example['design operation']
        errors=validate(bad);assert errors
        negative.append(dict(req_id=example['Req ID'],rejected=True,errors=errors))
    return current,audit,negative


def main():
    rows,audit,negative=build()
    for path,data in [(D/'traceability.csv',rows),(D/'implementation/p4_traceability_audit.csv',audit)]:
        with path.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    (D/'implementation/p4_traceability_regression.json').write_text(json.dumps(dict(rows=52,exact_token_join=True,negative_examples=negative),indent=2),encoding='utf-8')
    print('Audited 52 rows; rejected all three preserved mismatches; later-phase NFR limits retained.')


if __name__=='__main__':main()
