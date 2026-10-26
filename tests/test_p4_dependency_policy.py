"""Owner-amended architecture acceptance and parsed-only hostile mutations.
Author: 722I0004 · AI-assisted (Codex). Never executes synthetic fixture code.
"""
from copy import deepcopy
from pathlib import Path
import ast, csv, importlib.util, json
import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('b02_audit',ROOT/'docs/part2/_scripts/p4_dependency_policy_audit.py')
AUDIT=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(AUDIT)
POLICY=json.loads((AUDIT.P/'policy.json').read_text())
REVIEWED=json.loads((AUDIT.P/'reviewed_scope.json').read_text())
DAO='saigonbite.data_access.order_dao'
HUB='saigonbite.data_access.hub_dao'
DOMAIN='saigonbite.business.domain'


def run(code): return AUDIT.audit(code,POLICY,REVIEWED)


def test_entire_application_exact_symbols_and_manual_use_seals():
    result=run(AUDIT.sources())
    assert result['pass_'],result['errors']
    assert result['exact_dependency_set']
    assert {x['source'] for x in result['pairs']}=={x['source'] for x in POLICY['dependencies']}
    assert all(x['effective'] for x in result['import_records'] if x['target'].startswith('saigonbite'))
    assert result['module_count']==len(AUDIT.sources())


def test_each_actual_symbol_and_rules_member_has_use_review():
    ledger=json.loads((AUDIT.P/'symbol_use_review.json').read_text())
    required={(d['source'],d['target'],s) for d in POLICY['dependencies'] for s in d['symbols']}
    assert {(x['source'],x['target'],x['symbol']) for x in ledger}==required
    assert all(x['sites'] and x['manual_verdict'].startswith('ACCEPTED_EXPLICIT_POLICY') for x in ledger)
    rules=[x for x in ledger if x['symbol']=='rules']
    assert {x['source'] for x in rules}=={HUB,DAO}
    assert all(x['members']==['TERMINAL_ORDER_STATES'] for x in rules)
    gateway=next(x for x in ledger if x['source'].endswith('payment_gateway'))
    assert gateway['symbol']=='OnlineOption' and 'simulator' in gateway['permitted_use']


def test_all_eleven_removed_presentation_pairs_stay_absent():
    old=list(csv.DictReader((ROOT/'docs/part2/implementation/p4_import_disposition.csv').open(encoding='utf-8-sig',newline='')))
    removed={(r['source'],r['target']) for r in old if r['status']=='RESOLVED'}
    actual={(r['source'],r['target']) for r in run(AUDIT.sources())['import_records']}
    assert removed and removed.isdisjoint(actual)
    assert all(AUDIT.role(s)=='view' for s,t in removed)


@pytest.mark.parametrize('module,addition,reason',[
 ('saigonbite.data_access.thirteenth','from saigonbite.business.domain import Order\n','unapproved symbol/pair'),
 (DAO,'from saigonbite.business.domain import Voucher\n','unapproved symbol/pair'),
 (HUB,'from saigonbite.business.domain.rules import delivery_fee\n','unapproved symbol/pair'),
 (HUB,'rules.delivery_fee(10)\n','unapproved rules member'),
 (HUB,'from saigonbite.business.domain import rules as r\nr.delivery_fee(10)\n','unapproved rules member'),
 (DAO,'from saigonbite.business.controllers import PlaceOrderController\n','forbidden direction'),
 (DAO,'from saigonbite.presentation import order\n','forbidden direction'),
 (DOMAIN+'.models','from saigonbite.data_access import OrderDAO\n','forbidden direction'),
 ('saigonbite.presentation.order','from saigonbite.business.domain import Order\n','forbidden direction'),
 ('saigonbite.presentation.order','from saigonbite.data_access import OrderDAO\n','forbidden direction'),
 ('saigonbite.presentation.order','from saigonbite import NAV\n','forbidden direction'),
 (DAO,'from ..business.domain import Voucher as Innocent\n','unapproved symbol/pair'),
 (DAO,'from saigonbite.business.domain import *\n','wildcard'),
 (DAO,"__import__('saigonbite.business.controllers')\n",'dynamic/unresolved'),
 (DAO,"import importlib as i\ni.import_module('saigonbite.business.controllers')\n",'dynamic/unresolved'),
 (DAO,"from importlib import import_module as load\nload('saigonbite.business.controllers')\n",'dynamic/unresolved'),
 (DAO,"def surprise(conn):\n    conn.commit()\n",'DAO transaction ownership'),
 (DAO,"def surprise(conn):\n    conn.rollback()\n",'DAO transaction ownership'),
 (DAO,"def surprise(order):\n    order.transition(OrderState.READY)\n",'unreviewed semantic body/use'),
 ('saigonbite.data_access.payment_dao',"def surprise(payment):\n    payment.release_for_unfulfilled_order()\n",'unreviewed semantic body/use'),
 ('saigonbite.data_access.payment_dao',"def surprise(payment, total):\n    payment.refund_amount = payment.amount-total\n",'unreviewed semantic body/use'),
 ('saigonbite.data_access.voucher_dao',"def surprise(v, subtotal):\n    return subtotal*v.discount_value//100\n",'unreviewed semantic body/use'),
 (DAO,"def surprise(conn):\n    conn.execute('BEGIN IMMEDIATE')\n",'unreviewed semantic body/use'),
 (DAO,"def surprise(rules):\n    return getattr(rules, 'delivery_fee')(10)\n",'unreviewed semantic body/use'),
 (DOMAIN+'.models',"open('never-created')\n",'domain I/O'),
 ('saigonbite.presentation.order',"conn.execute('SELECT 1')\n",'view SQL'),
 ('saigonbite.business.domain.enums','from saigonbite.business.controllers import PlaceOrderController\n','cross-role cycle'),
 ('saigonbite.data_access.new_without_import',"def refund(p):\n    p.refund_amount=p.amount\n",'unreviewed semantic body/use'),
])
def test_rejects_parsed_negative_without_execution(module,addition,reason):
    code=AUDIT.sources();code[module]=code.get(module,'')+'\n'+addition
    result=run(code)
    assert not result['pass_']
    assert any(reason in e for e in result['errors']), result['errors']


def test_hidden_reexport_cannot_turn_old_pair_into_new_symbol():
    code=AUDIT.sources()
    code['saigonbite.business.domain']+='\nfrom saigonbite.business.controllers import PlaceOrderController as Order\n'
    result=run(code)
    assert not result['pass_']
    assert any('ambiguous export' in e for e in result['errors'])


def test_indirect_reexport_through_new_facade_rejected():
    code=AUDIT.sources();code['saigonbite.business.controllers.fake']='from saigonbite.data_access import OrderDAO\n'
    code['saigonbite.presentation.order']+='\nfrom saigonbite.business.controllers.fake import OrderDAO\n'
    result=run(code)
    assert not result['pass_'] and any('unreviewed view facade' in e for e in result['errors'])


def test_new_symbol_through_existing_named_facade_is_not_grandfathered():
    code=AUDIT.sources();code['saigonbite.business.controllers.presentation_contract']+='\nfrom saigonbite.data_access import OrderDAO\n'
    code['saigonbite.presentation.order']+='\nfrom saigonbite.business.controllers.presentation_contract import OrderDAO\n'
    result=run(code)
    assert not result['pass_'] and any('unreviewed view facade' in e for e in result['errors'])


@pytest.mark.parametrize('change', ['alias','relative','comment'])
def test_explicitly_reviewed_equivalent_fixture_passes(change):
    # This is a small positive fixture disposition, not automatic renewal of app
    # seals. Hostile tests above always use the immutable original review seals.
    code=AUDIT.sources();text=code[HUB]
    if change=='alias':
        text=text.replace('MenuItem, rules','MenuItem, rules as terminal_rules').replace('rules.TERMINAL_ORDER_STATES','terminal_rules.TERMINAL_ORDER_STATES')
    elif change=='relative': text=text.replace('from saigonbite.business.domain import','from ..business.domain import')
    else: text+='\n# harmless comment fixture\n'
    code[HUB]=text;review=deepcopy(REVIEWED)
    review['module_ast'][HUB]=AUDIT.semantic(ast.parse(text))
    result=AUDIT.audit(code,POLICY,review)
    assert result['pass_'] and result['exact_dependency_set'],result['errors']


def test_actual_missing_dependency_does_not_qualify_full_set():
    code=AUDIT.sources();code.pop('saigonbite.data_access.voucher_dao')
    result=run(code)
    assert not result['exact_dependency_set']
    assert not result['pass_']  # Import resolution also reports removed module.
