"""Adapt valid I1 submissions to explicit BR-10 consent, preserving negative cases.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[3]
for p in (R/'tests').glob('test_*.py'):
    if p.name.startswith('test_p4_'):continue
    source=p.read_text(encoding='utf-8'); tree=ast.parse(source); lines=source.splitlines(keepends=True)
    for node in reversed(tree.body):
        if not isinstance(node,ast.FunctionDef):continue
        args={a.arg for a in node.args.args}
        client='customer_client' if 'customer_client' in args else 'client' if 'client' in args else None
        if client:
            block=''.join(lines[node.lineno-1:node.end_lineno])
            if 'checkout_form(' in block:
                block=block.replace('checkout_form(',f'checkout_form(client={client}, ')
                # Avoid trailing empty argument for empty-call forms.
                block=block.replace(f'checkout_form(client={client}, )',f'checkout_form(client={client})')
                lines[node.lineno-1:node.end_lineno]=[block]
    p.write_text(''.join(lines),encoding='utf-8')
