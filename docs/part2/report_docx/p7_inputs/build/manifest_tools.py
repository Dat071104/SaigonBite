# Helpers to edit docs/part2/latex/figure_manifest.csv (30/10/2026 revision) and refresh pixel size / sha256.
from pathlib import Path
import csv, hashlib
from PIL import Image
R = Path(r'D:\RAD\FINAL\SaigonBite'); M = R / 'docs/part2/latex/figure_manifest.csv'

def load():
    with M.open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f); return r.fieldnames, list(r)

def save(fields, rows):
    with M.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def next_id(rows):
    n = max(int(x['fig_id'][3:]) for x in rows if x['fig_id'].startswith('P7-'))
    return f'P7-{n + 1:04d}'

def new_row(fields, rows, **kw):
    row = {k: '' for k in fields}
    row.update(record_type='figure', author='722I0004', width_mm='230', page_orientation='landscape', body_or_appendix='body', readability='PASS estimate')
    row.update(kw)
    row['fig_id'] = row.get('fig_id') or next_id(rows)
    row['source_section'] = row.get('source_section') or row['section']
    rows.append(row); return row

def refresh(rows):
    for x in rows:
        if x['record_type'] != 'figure' or not x['source_png']:
            continue
        p = R / x['source_png']
        with Image.open(p) as im:
            x['pixel_size'] = f'{im.size[0]}x{im.size[1]}'
        x['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
