# Re-anchors assembly_plan.json line ranges after report sources are edited.
# Anchors come from the committed version (git HEAD by default, or --base <rev>): each range's first line and
# the line after it. Contiguous ranges end where the next range starts; a range ending at EOF stays at EOF.
# A range may also be pinned by an override heading (see OVERRIDES) when its anchor text itself was rewritten.
from pathlib import Path
import json, subprocess, sys
B = Path(r'D:\RAD\FINAL'); R = B / 'SaigonBite'; PLAN = B / 'Part2/notes/P7/assembly_plan.json'
base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else 'HEAD'
# The input ranges are those of the plan committed at the same revision (docs/part2/report_docx/p7_inputs), so the
# script is idempotent: running it twice before a commit gives the same result.
plan = json.loads(subprocess.run(['git', '-C', str(R), 'show', f'{base}:docs/part2/report_docx/p7_inputs/assembly_plan.json'],
                                 capture_output=True, text=True, encoding='utf-8', check=True).stdout)
work = json.loads(PLAN.read_text(encoding='utf-8'))
assert [r['heading'] for r in plan['sections']] == [r['heading'] for r in work['sections']], 'plan rows changed since the base commit'
plan['template_styled_headings'] = work['template_styled_headings']
old_cache, new_cache = {}, {}

def old_lines(f):
    if f not in old_cache:
        old_cache[f] = subprocess.run(['git', '-C', str(R), 'show', f'{base}:{f}'], capture_output=True, text=True, encoding='utf-8').stdout.lstrip('\ufeff').splitlines()
    return old_cache[f]

def new_lines(f):
    if f not in new_cache:
        new_cache[f] = (R / f).read_text(encoding='utf-8-sig').splitlines()
    return new_cache[f]

def occurrence(lines, i):
    return sum(1 for x in lines[:i] if x == lines[i])

def find(lines, text, occ):
    hits = [i for i, x in enumerate(lines) if x == text]
    if len(hits) <= occ:
        raise LookupError(text[:80])
    return hits[occ]

# Collect every range with its owner so contiguous neighbours can be resolved.
entries = []
for row in plan['sections']:
    for key, fkey in (('content_line_ranges', 'source file'), ('post_content_line_ranges', 'post_source_file')):
        f = row.get(fkey)
        if not f or not f.startswith('docs/') or not row.get(key):
            continue
        for idx, (a, z) in enumerate(row[key]):
            entries.append((f, a, z, row, key, idx))

problems = []
starts = {}
for f, a, z, row, key, idx in entries:
    ol = old_lines(f)
    try:
        starts[(f, a)] = find(new_lines(f), ol[a - 1], occurrence(ol, a - 1)) + 1
    except LookupError as e:
        problems.append((row['heading'], 'start', str(e)))
old_starts = {}
for f, a, z, *_ in entries:
    old_starts.setdefault(f, set()).add(a)
changed = 0
for f, a, z, row, key, idx in entries:
    if (f, a) not in starts:
        continue
    ol, nl = old_lines(f), new_lines(f)
    na = starts[(f, a)]
    if z >= len(ol):
        nz = len(nl)
    elif (z + 1) in old_starts[f] and (f, z + 1) in starts:
        nz = starts[(f, z + 1)] - 1
    else:
        try:
            nz = find(nl, ol[z], occurrence(ol, z))  # line after the range, 0-based == 1-based end
        except LookupError as e:
            problems.append((row['heading'], 'end', str(e))); continue
    if [na, nz] != row[key][idx]:
        changed += 1
    row[key][idx] = [na, nz]
if problems:
    for p in problems: print('PROBLEM', p)
    sys.exit(1)
PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('ranges re-anchored; changed', changed, 'of', len(entries))
