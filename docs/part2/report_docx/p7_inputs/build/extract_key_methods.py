# Writes report 4.3.5 from the source: complete methods (def line to the last line of the body, found with ast),
# one realisation chain per main use case (view -> controller -> domain -> DAO), plus a receipt with hashes.
# Revised 30/10/2026: whole methods instead of fragments; acceptReplacement and confirmDelivered added.
from pathlib import Path
import ast, hashlib, json
root = Path(r'D:\RAD\FINAL\SaigonBite'); notes = Path(r'D:\RAD\FINAL\Part2\notes\P7'); out = root / 'docs/part2/report/IV_4-3-5_key_methods.md'
C = 'saigonbite/business/controllers/'; DM = 'saigonbite/business/domain/models.py'; DA = 'saigonbite/data_access/'
spec = [
 ('UC-01', 'OP-01', 'confirmCheckout', 'The customer confirms the quote: the controller re-prices, checks consent and capacity inside one transaction, the domain creates the order, and the DAO stores it.',
  [(C + 'place_order_controller.py', 'PlaceOrderController', 'confirm_order'), (DM, 'Order', 'place'), (DA + 'order_dao.py', 'OrderDAO', 'insert')]),
 ('UC-02', 'OP-10', 'takeDelivery', 'A shipper takes a READY order; the guarded UPDATE lets only one of two competing shippers succeed.',
  [(C + 'delivery_controller.py', 'DeliveryController', 'pick_up'), (DA + 'delivery_dao.py', 'DeliveryDAO', 'take')]),
 ('UC-02', 'OP-11', 'confirmDelivered', 'The assigned shipper finishes the delivery; for COD the cash collected must equal the order total.',
  [(C + 'delivery_controller.py', 'DeliveryController', 'confirm_delivered'), (DA + 'delivery_dao.py', 'DeliveryDAO', 'finish')]),
 ('UC-03', 'OP-36', 'archiveHub', 'The admin archives a hub; the controller refuses while the hub still has open orders.',
  [(C + 'hub_controller.py', 'HubController', 'archive_hub'), (DA + 'hub_dao.py', 'HubDAO', 'archive')]),
 ('UC-04', 'OP-26', 'salesReport', 'The manager asks for sales in a Vietnam-date range; the DAO aggregates delivered orders by hub.',
  [(C + 'report_controller.py', 'ReportController', 'sales_report'), (DA + 'report_dao.py', 'ReportDAO', 'sales_by_hub')]),
 ('UC-05', 'OP-03', 'rejectOrder', 'Kitchen staff reject an own-hub PLACED order; the payment is released (COD voided, online amount owed back).',
  [(C + 'kitchen_controller.py', 'KitchenController', 'reject_order'), (DM, 'Payment', 'release_for_unfulfilled_order')]),
 ('UC-05', 'OP-05', 'acceptReplacement', 'The customer answers an open replacement offer; the controller re-checks the exact offer and the target before the line is replaced.',
  [(C + 'order_tracking_controller.py', 'OrderTrackingController', 'answer_replacement'), (DM, 'Order', 'replace_line')]),
 ('UC-06', 'OP-41', 'updateMenuItem', 'The admin edits a menu item; earlier orders keep their own name and price snapshot.',
  [(C + 'menu_controller.py', 'MenuController', 'update_item'), (DA + 'menu_dao.py', 'MenuDAO', 'update_item')]),
]
lines = ['# 4.3.5 Software Classes Method Code', '', 'Author: 722I0004 · AI-assisted (Codex, Claude)', '',
         'For every main use case, the methods that realise one important system operation are printed in full, in the order of its sequence diagram (controller, then domain, then data access). '
         'They are copied unchanged from the source files of release v0.9-part2; the line numbers refer to that release. '
         'All other classes and methods are in the repository (`saigonbite/`); the design class tables in 3.x.1 list every method signature.', '']
receipts = []
for uc, op, operation, intro, methods in spec:
    lines += [f'## {uc} — {operation} ({op})', '', intro, '']
    for rel, cl, fn in methods:
        raw = (root / rel).read_bytes(); src = raw.decode('utf-8'); tree = ast.parse(src)
        obj = next(x for x in tree.body if isinstance(x, ast.ClassDef) and x.name == cl)
        m = next(x for x in obj.body if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef)) and x.name == fn)
        start = min([m.lineno] + [d.lineno for d in m.decorator_list]); end = m.end_lineno
        text = src.splitlines()[start - 1:end]
        indent = min(len(x) - len(x.lstrip()) for x in text if x.strip())
        chunk = '\n'.join(x[indent:] for x in text)
        lines += [f'**{cl}.{fn}** — `{rel}`, lines {start}–{end}; [source at release v0.9-part2]({{{{LinkRepo}}}}/blob/v0.9-part2/{rel}#L{start}-L{end}).', '', '```python', chunk, '```', '']
        receipts.append({'uc': uc, 'operation': op, 'class': cl, 'method': fn, 'path': rel, 'start': start, 'end': end,
                         'source_sha256': hashlib.sha256(raw).hexdigest(), 'excerpt_sha256': hashlib.sha256('\n'.join(text).encode()).hexdigest()})
out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
(notes / 'code_excerpt_receipt.json').write_text(json.dumps(receipts, indent=2) + '\n', encoding='utf-8')
print('wrote', len(receipts), 'complete methods for', len({r["uc"] for r in receipts}), 'use cases')
