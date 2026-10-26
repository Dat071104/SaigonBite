"""Bind reviewed obligations to actual passing JUnit nodes and source assertions.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import ast,csv,hashlib,json,re,sys,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[3];D=R/'docs/part2';I=D/'implementation'

ANCHORS={
'UC01-PC01':'T_UC01_10_confirm_creates_placed_order_lines_and_pending_cod_payment',
'UC01-PC02':'T_UC01_14_read_back_through_new_connection_same_lines_and_total;receipt_stored_snapshot_read_only_own_and_truthful',
'UC01-PC03':'receipt_stored_snapshot_read_only_own_and_truthful;raw_radius_and_started_km_independent_sphere_fixture',
'UC01-PC04':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c;quiet_strict_boundary_capped_fee_and_snapshot;voucher_independent_integer_oracle',
'UC01-PC05':'T_UC01_10_confirm_creates_placed_order_lines_and_pending_cod_payment;local_and_tourist_online_allowed_options_and_decline',
'UC01-PC06':'two_customers_race_last_slot_one_durable_winner;lower_capacity_below_load_then_checkout_refused',
'UC01-MG01':'equal_total_content_changes_require_new_quote;online_approval_then_failure_releases_authorization_and_rolls_back;T_UC01_20_confirm_rejects_invalid_input_without_creating_an_order',
'UC01-MG02':'T_UC01_34_concurrent_submits_with_one_token_still_create_one_order;replay_ignores_changed_current_input_but_foreign_token_never_discloses',
'UC01-MG03':'suggestion_ratio_raw_distance_id_ties_limit_and_empty;two_customers_race_last_slot_one_durable_winner',
'UC02-PC01':'two_shippers_one_ready_order_exactly_one_persisted_claim',
'UC02-PC02':'assigned_finish_pair_states_timestamps_refund_and_repeat',
'UC02-PC03':'assigned_finish_pair_states_timestamps_refund_and_repeat',
'UC02-MG01':'cod_requires_exact_whole_cash_and_no_partial_writes;assigned_finish_pair_states_timestamps_refund_and_repeat;foreign_owner_hub_and_assigned_shipper_paths',
'UC03-PC01':'admin_real_crud_and_archived_history',
'UC03-PC02':'admin_real_crud_and_archived_history;sales_reduced_total_no_double_refund_multiline_and_archived_identity',
'UC03-MG01':'invalid_fields_and_duplicate_code_change_nothing;every_open_state_blocks_archive;stale_conditional_save_rolls_back;hub_commit_failure_no_partial_save',
'UC04-PC01':'sales_reduced_total_no_double_refund_multiline_and_archived_identity;top_items_use_id_and_latest_eligible_snapshot_name;delivery_means_sample_sizes_and_failure_denominator;workload_now_retains_archived_hubs_and_empty_values;half_open_exact_boundaries',
'UC04-PC02':'workload_now_retains_archived_hubs_and_empty_values',
'UC04-MG01':'reports_actual_connection_authorizer_and_unchanged_facts',
'UC04-MG02':'report_manager_authorization_and_rendered_truth;route_role_matrix',
'UC05-PC01':'main_kitchen_confirm_and_reject_have_exact_durable_effects',
'UC05-PC02':'main_kitchen_confirm_and_reject_have_exact_durable_effects;fixed_money_oracle_partial_then_unfulfilled_owes_full_c',
'UC05-PC03':'offer_guard_one_negative_per_condition;open_offer_confirmation_preparing_stale_and_foreign_answers',
'UC05-PC04':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c;invalid_target_withdraws_only_exact_offer',
'UC05-MG01':'offer_guard_one_negative_per_condition;open_offer_confirmation_preparing_stale_and_foreign_answers;invalid_target_withdraws_only_exact_offer;foreign_owner_hub_and_assigned_shipper_paths',
'UC06-PC01':'real_brand_item_crud_and_composite_reader',
'UC06-PC02':'initial_unavailable_listing_is_atomic_and_two_hubs_independent;real_brand_item_crud_and_composite_reader',
'UC06-PC03':'parent_archive_excludes_active_child_and_refuses_listing;initial_unavailable_listing_is_atomic_and_two_hubs_independent',
'UC06-MG01':'every_catalogue_mutation_preserves_old_snapshot_and_money',
'UC06-MG02':'catalogue_invalid_data_and_lifetime_uniqueness;catalogue_checked_zero_row_outcomes',
'SUC01-PC01':'T_UC01_45_login_with_wrong_password_is_refused;real_registration_profile_hotel_address_and_logout;route_role_matrix',
'SUC01-PC02':'foreign_address_inactive_session_admin_customer_read;T_UC01_47_logout_ends_the_session;route_role_matrix',
'SUC02-PC01':'real_registration_profile_hotel_address_and_logout;sql_type_nationality_and_linked_role_guards',
'SUC02-PC02':'real_registration_profile_hotel_address_and_logout;registered_subtype_forgery_cannot_alter_profile',
'SUC02-PC03':'real_registration_profile_hotel_address_and_logout;foreign_address_inactive_session_admin_customer_read;receipt_stored_snapshot_read_only_own_and_truthful',
'SUC03-PC01':'route_role_matrix;per_id_archive_preserves_children_receipt_and_history',
'SUC03-PC02':'receipt_stored_snapshot_read_only_own_and_truthful',
'SUC03-PC03':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c',
'SUC03-PC04':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c',
'SUC03-PC05':'invalid_target_withdraws_only_exact_offer',
'SUC04-PC01':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c;open_offer_confirmation_preparing_stale_and_foreign_answers',
'SUC04-PC02':'fixed_money_oracle_partial_then_unfulfilled_owes_full_c',
'SUC05-PC01':'ready_creates_one_delivery_and_insert_failure_rolls_back;customer_kitchen_races_admit_valid_serializations',
'SUC05-PC02':'ready_creates_one_delivery_and_insert_failure_rolls_back',
'SUC06-PC01':'initial_unavailable_listing_is_atomic_and_two_hubs_independent;every_catalogue_mutation_preserves_old_snapshot_and_money;route_role_matrix',
'SUC07-PC01':'real_voucher_crud_lifetime_code_and_conditional_save',
'SUC07-PC02':'real_voucher_crud_lifetime_code_and_conditional_save;voucher_independent_integer_oracle;every_catalogue_mutation_preserves_old_snapshot_and_money',
'SUC08-PC01':'staff_crud_hub_assignment_activation_and_retained_username;immutable_staff_identity_forgery_refused_without_other_edits',
'SUC08-PC02':'foreign_address_inactive_session_admin_customer_read;staff_crud_hub_assignment_activation_and_retained_username',
'SUC09-PC01':'per_id_archive_preserves_children_receipt_and_history;archive_open_missing_and_zero_row_refusal;archive_populated_aggregate_keeps_delivery_offer_refund_receipt_and_report',
'SUC09-PC02':'per_id_archive_preserves_children_receipt_and_history;sales_reduced_total_no_double_refund_multiline_and_archived_identity;archive_populated_aggregate_keeps_delivery_offer_refund_receipt_and_report',
}
SUPPORT={
'SUC-01':'route_role_matrix;T_UC01_45_login_with_wrong_password_is_refused;foreign_address_inactive_session_admin_customer_read',
'SUC-02':'registration_invalid_fields_zero_writes;tourist_required_identity;foreign_address_inactive_session_admin_customer_read;registration_partial_insert_and_stale_dao_updates;foreign_owner_hub_and_assigned_shipper_paths',
'SUC-03':'open_offer_confirmation_preparing_stale_and_foreign_answers;invalid_target_withdraws_only_exact_offer;foreign_owner_hub_and_assigned_shipper_paths',
'SUC-04':'customer_kitchen_races_admit_valid_serializations;foreign_owner_hub_and_assigned_shipper_paths;fixed_money_oracle_partial_then_unfulfilled_owes_full_c',
'SUC-05':'ready_creates_one_delivery_and_insert_failure_rolls_back;preparing_blocked_with_open_offer_even_if_confirmed_state;foreign_owner_hub_and_assigned_shipper_paths',
'SUC-06':'parent_archive_excludes_active_child_and_refuses_listing;route_role_matrix;initial_unavailable_listing_is_atomic_and_two_hubs_independent',
'SUC-07':'voucher_independent_integer_oracle;vietnam_inclusive_voucher_day_edges;real_voucher_crud_lifetime_code_and_conditional_save',
'SUC-08':'shipper_multiple_assignments_allowed_and_deactivation_guard;immutable_staff_identity_forgery_refused_without_other_edits;staff_crud_hub_assignment_activation_and_retained_username;route_role_matrix',
'SUC-09':'archive_open_missing_and_zero_row_refusal;per_id_archive_preserves_children_receipt_and_history;route_role_matrix',
}
PHASE_FILES={1:'test_p4_foundation.py',2:'test_p4_hubs.py',3:'test_p4_ordering.py',4:'test_p4_kitchen.py',5:'test_p4_delivery.py',6:'test_p4_catalogue.py',7:'test_p4_accounts.py',8:'test_p4_report_oracle.py',9:'test_p4_permissions.py;test_p4_regression_evidence.py'}


def readcsv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))


def save(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def bind(receipt_path):
    receipt=json.loads(Path(receipt_path).read_text(encoding='utf-8'));assert receipt['exit']==0
    assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in receipt['executable_inputs'].items())
    xml=Path(next(x.split('=',1)[1] for x in receipt['command'] if x.startswith('--junitxml=')))
    root=ET.parse(xml).getroot();cases=list(root.iter('testcase'));assert all(not list(c) for c in cases)
    nodes=[c.attrib['classname'].replace('.','/')+'.py::'+c.attrib['name'] for c in cases]
    funcs={};assertions={}
    for p in (R/'tests').glob('test_*.py'):
        for f in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig'))):
            if isinstance(f,ast.FunctionDef) and f.name.startswith('test_'):
                key=p.relative_to(R).as_posix()+'::'+f.name
                funcs[key]=f;assertions[key]=[ast.unparse(a) for a in ast.walk(f) if isinstance(a,ast.Assert)]
    def resolve(patterns):
        output=[]
        for name in patterns.split(';'):
            if not name:continue
            full='test_'+name if not name.startswith('test_') else name
            matches=[n for n in nodes if n.split('::')[1].split('[',1)[0]==full]
            assert matches,full
            output+=matches
        return sorted(set(output))
    coverage=readcsv(I/'p4_test_coverage.csv')
    for row in coverage:
        patterns=ANCHORS.get(row['id']) or SUPPORT[row['id'].split('/')[0]]
        selected=resolve(patterns)
        proof={n.split('[',1)[0]:'; '.join(assertions[n.split('[',1)[0]]) for n in selected}
        row.update(tests=';'.join(selected),meaningful_assertions=json.dumps(proof,ensure_ascii=False),
            passing_execution=str(Path(receipt_path).resolve()),log=receipt['log'],commit=receipt['head'],status='PASS (scoped assertions; not G4 readiness)')
    assert len(coverage)==69
    save(I/'p4_test_coverage.csv',coverage)
    save(I/'p4_current_test_nodes.csv',[dict(node=n,result='PASS',commit=receipt['head'],log=receipt['log']) for n in nodes])
    inventory=readcsv(I/'p4_test_inventory.csv')
    reduced=[]
    for row in inventory:
        key=row['historical_node'];assert key in funcs,key
        if len(assertions[key])<int(row['assert_count']):reduced.append((key,row['assert_count'],len(assertions[key])))
        selected=[n for n in nodes if n.split('[',1)[0]==key];assert selected
        row.update(retained='YES; historical function and obligations retained',
            expectation_change='BR-03/07 quiet and started-km fees; BR-10 consent; BR-12 v2 subtypes; D-5 retired Vercel assets; I1 schema assertion scoped to frozen i1-evidence. Only applicable changes; see commit diffs.',
            after='PASS: '+str(len(selected))+' expanded nodes; '+receipt['head']+'; '+receipt['log'])
    assert not reduced,reduced
    save(I/'p4_test_inventory.csv',inventory)
    matrix=[]
    for c,n in zip(cases,nodes):
        if '::test_route_role_matrix[' in n:
            params=n.split('test_route_role_matrix[',1)[1][:-1];actor,request=params.split('-',1)
            matrix.append(dict(actor=actor,request=request,node=n,result='PASS; valid session CSRF; denied requests compare all domain facts',commit=receipt['head'],log=receipt['log']))
    assert len(matrix)==78*7
    save(I/'p4_route_role_matrix.csv',matrix)
    policy=json.loads((R/'tests/fixtures/p4_route_policy.json').read_text())
    (I/'p4_route_inventory.json').write_text(json.dumps(dict(routes=policy,count=len(policy),method_scope='GET/POST; HEAD follows GET; automatic OPTIONS and static assets excluded',source=receipt['head']),indent=2),encoding='utf-8')
    # Every original source-row identity is retained, including repetitions and shared dependencies.
    inputs=readcsv(I/'p4_design_resolution.csv');frozen=readcsv(D/'design/P4_design_inputs.csv')
    assert len(inputs)==len(frozen)==121 and len({x['element'] for x in inputs})==96
    import_rows=readcsv(I/'p4_import_disposition.csv')
    for row,source in zip(inputs,frozen):
        assert all(row[k]==v for k,v in source.items())
        phases={int(n) for n in re.findall(r'P4\.(\d)',row['P4 subphase'])}
        filenames={f for phase in phases for f in PHASE_FILES[phase].split(';')}
        selected=[n for n in nodes if Path(n.split('::')[0]).name in filenames]
        assert selected,row['element']
        blocked='P3-S04' in row['P4 input'] and row['element'].startswith('saigonbite.data_access')
        row.update(implementation=row['element']+'; current implementation diff and subphase handoff; original source row/hash retained',
            test_nodes=';'.join(selected),code_revision=receipt['head'],
            disposition='BLOCKED P4-B02' if blocked else 'VERIFIED P4 scoped runtime/static evidence',
            remaining_limitations='Frozen strict DAO materialisation contract; no mapper exception' if blocked else 'Static dependency/type facts are not independent runtime assertions; operation/subphase cases and exact hashes are attached; P5/P6/P7 evidence not claimed')
    save(I/'p4_design_resolution.csv',inputs)
    # Semantic row evidence is derived by exact complete PC/MG tokens, never digits or ordinal positions.
    trace=readcsv(D/'traceability.csv');lookup={r['id']:r['tests'] for r in coverage}
    nfr={'NFR-03':'created_at_and_connection_policy;transaction_failures_preserve_error_and_durable_state',
         'NFR-04':'production_requires_secret_and_secure_settings','NFR-05':'passport_never_rendered_to_kitchen_shipper_or_logs',
         'NFR-06':'every_mutating_route_rejects_invalid_csrf_without_domain_writes',
         'NFR-07':'production_requires_secret_and_secure_settings','NFR-08':'production_requires_secret_and_secure_settings',
         'NFR-09':'','NFR-10':'architecture_inventory_is_truthful_and_domain_views_respect_io_boundary'}
    for row in trace:
        named=re.findall(r'(?:SUC\d{2}-PC\d{2}|UC\d{2}-(?:PC|MG)\d{2})',row['PC/MG ID'])
        selected=sorted({n for token in named for n in lookup[token].split(';')})
        if row['Req ID'] in nfr:selected=resolve(nfr[row['Req ID']])
        row['test ID']=';'.join(selected)
        row['result evidence']=(receipt['head']+'; '+receipt['log']+'; P4 scoped pass only' if selected else 'NOT RUN: P5/P6 browser phone-width evidence')
        if row['Req ID'] in ('NFR-03','NFR-04','NFR-05','NFR-08','NFR-09'):row['result evidence']+='; later P5/P6/P7 qualification pending'
        if row['Req ID']=='NFR-10':row['result evidence']+='; G4 BLOCKED P4-B02; remaining 12 forbidden import pairs'
    save(D/'traceability.csv',trace)
    summary=dict(author='722I0004 · AI-assisted (Codex)',tested_commit=receipt['head'],tests=len(nodes),errors=0,failures=0,skipped=0,xfail=0,
        main_anchors=30,supporting_pcs=21,supporting_guard_sections=9,supporting_failure_sections=9,
        coverage_rows=len(coverage),input_rows=len(inputs),elements=96,blocked_input_rows=sum(r['disposition'].startswith('BLOCKED') for r in inputs),
        historical_functions=len(inventory),historical_obligations_retained=True,route_method_pairs=78,role_matrix_cases=len(matrix),requirements_audited=52,
        receipt=str(Path(receipt_path).resolve()),junit=str(xml),junit_sha256=hashlib.sha256(xml.read_bytes()).hexdigest(),
        G4='BLOCKED P4-B02; no blanket completeness claim from counts')
    (I/'p4_evidence_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(summary)


if __name__=='__main__':bind(sys.argv[1])
