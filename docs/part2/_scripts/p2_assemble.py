"""Assemble report II from source parts, resolving single-source descriptions.

Optional state-block ranges are explicit integration decisions in the JSON
configuration; no description text is manually copied into report sources.
"""
from pathlib import Path
import json
import re

DOC=Path(__file__).resolve().parents[1]
REPORT=DOC/'report'
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'

def resolve(path):
    text=path.read_text(encoding='utf-8')
    def include(match):
        child=(path.parent/match.group(1).strip()).resolve()
        child.relative_to(DOC.resolve())
        return resolve(child)
    return re.sub(r'<!--\s*include:\s*(.*?)\s*-->',include,text)

def normalize(text):
    out=[]
    for line in text.splitlines():
        m=re.match(r'^#+\s+(.*)',line)
        if m:
            title=m.group(1)
            if re.match(r'2\.[123]\.\d+\s',title): level=3
            elif re.match(r'2\.[123]\s',title): level=2
            elif re.match(r'(?:i|ii|iii|iv)\.\s',title): level=4
            else: level=5
            line='#'*level+' '+title
        out.append(line)
    return '\n'.join(out).strip()

def main():
    config=json.loads((DOC/'_scripts/p2_assembly.json').read_text(encoding='utf-8'))
    state_text=(REPORT/'II_state_machines.md').read_text(encoding='utf-8')
    pieces=['# II. System Requirements Analysis (15 marks)',AUTHOR,'## 2.1 Translate from Business Use Case',
            normalize(resolve(REPORT/'II_2-1_team_analysis.md')),
            normalize(resolve(REPORT/'II_2-1-6_2-1-7_models.md')),
            '## 2.2 Use Case Descriptions',AUTHOR]
    for n in range(1,7):
        uc=f'UC-{n:02}'; part=REPORT/f'II_2-2-{n}_{uc}.md'
        text=resolve(part)
        blocks=[]
        for spec in config['state_blocks'].get(uc,[]):
            start=state_text.index(spec['start'])
            end=state_text.index(spec['end'],start+len(spec['start'])) if spec.get('end') else len(state_text)
            blocks.append(state_text[start:end].strip())
        if blocks:
            # iv is the last required subsection; figures are appended there.
            assert re.search(r'^#+\s+iv\. State machine diagram for Use Case '+str(n),text,re.M),uc
            text=text.rstrip()+'\n\nAll shared state figures below require **230 mm A4 landscape** placement (minimum 9.48 pt); do not shrink them into a portrait column.\n\n'+'\n\n'.join(blocks)+'\n'
        pieces.append(normalize(text))
    pieces.extend(['## 2.3 Verifying Use Cases for Actor (CRUD)',normalize(resolve(REPORT/'II_2-3_crud.md'))])
    result='\n\n'.join(pieces).rstrip()+'\n'
    # Sources may own group headings; keep only the first instance.
    for heading in ['## 2.1 Translate from Business Use Case','## 2.2 Use Case Descriptions','## 2.3 Verifying Use Cases for Actor (CRUD)']:
        first=result.index(heading)+len(heading)
        result=result[:first]+result[first:].replace(heading+'\n','')
    assert '<!-- include:' not in result
    target=REPORT/'II_system_requirements_analysis.md'; target.write_text(result,encoding='utf-8')
    print('Assembled',target,'characters',len(result))

if __name__=='__main__': main()
