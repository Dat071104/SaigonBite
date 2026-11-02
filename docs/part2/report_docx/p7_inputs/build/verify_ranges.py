# Checks that every assembly-plan range starts at the source heading of its row and that ranges of one file
# do not overlap. Prints the rows that need attention; exit 1 if any.
from pathlib import Path
import json, re, sys
B = Path(r'D:\RAD\FINAL'); R = B / 'SaigonBite'
plan = json.loads((B / 'Part2/notes/P7/assembly_plan.json').read_text(encoding='utf-8'))
bad = []; spans = {}
for row in plan['sections']:
    f = row.get('source file', '')
    if not f.startswith('docs/') or not row.get('content_line_ranges'):
        continue
    lines = (R / f).read_text(encoding='utf-8-sig').splitlines()
    a, z = row['content_line_ranges'][0]
    first = lines[a - 1] if 0 < a <= len(lines) else '<out of file>'
    head = row['heading']
    num = re.match(r'^((?:\d+\.)+\d*|[IVX]+\.|Appendix \d+|Executive|Conclusions|References)', head)
    key = num.group(1).rstrip('.') if num else head.split()[0]
    roman = re.match(r'^\d+\.\d+\.\d+ ([ivx]+)\.$', head)
    ok = first.startswith('#') and (key in first or (roman and re.match(r'^#+\s+' + roman.group(1) + r'\.', first)))
    if not ok and not first.startswith('#'):
        ok = False
    if not ok:
        bad.append((head[:45], f.split('/')[-1], a, first[:70]))
    for x, y in row['content_line_ranges'] + row.get('post_content_line_ranges', []):
        spans.setdefault(row.get('post_source_file') if [x, y] in row.get('post_content_line_ranges', []) else f, []).append((x, y, head[:30]))
for f, s in spans.items():
    s.sort()
    for (a1, z1, h1), (a2, z2, h2) in zip(s, s[1:]):
        if a2 <= z1:
            bad.append(('OVERLAP ' + h1 + ' / ' + h2, f, a2, ''))
for b in bad:
    print(b)
print('checked', len(plan['sections']), 'rows; issues', len(bad))
sys.exit(1 if bad else 0)
