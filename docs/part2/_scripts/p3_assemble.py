"""Assemble exact III/IV template headings and resolve single-source includes.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
import json,re
D=Path(__file__).resolve().parents[1];REPORT=D/'report';R=D.parents[1]
AUTHOR='Author: 722I0004 · AI-assisted (Codex)'
def resolve(path,seen=None):
    seen=set() if seen is None else seen
    path=path.resolve();path.relative_to(D.resolve());assert path not in seen,'Include cycle: '+str(path)
    text=path.read_text(encoding='utf-8-sig')
    def include(m):return resolve((path.parent/m[1].strip()),seen|{path})
    return re.sub(r'<!--\s*include:\s*(.*?)\s*-->',include,text)
def normalize(text):
    lines=[]
    for line in text.splitlines():
        m=re.match(r'^#+\s+(.*)',line)
        if m:
            title=m[1]
            if re.match(r'3\.[1-6]\.\d+\s',title):level=3
            elif re.match(r'3\.[1-6]\s|4\.[12]\s',title):level=2
            elif re.match(r'4\.3\.[1-6]\s',title):level=3
            elif re.match(r'(i|ii|iii|iv|v)\.\s',title):level=4
            else:level=5
            line='#'*level+' '+title
        lines.append(line)
    return '\n'.join(lines).strip()
def main():
    parts=['# III. System Requirements Design (15 marks)',AUTHOR,'This section assigns each frozen SSD operation to a view route, controller and collaborating domain objects. MATCH is static correspondence at C0; † P4-TARGET/GAP elements describe the target and its named P4 input. No runtime result is claimed. All landscape figures must retain their specified 230 mm width in the final report.']
    analysis=(REPORT/'II_system_requirements_analysis.md').read_text(encoding='utf-8-sig')
    goals={int(n):name for n,name in re.findall(r'^### 2\.2\.([1-6]) Use Case [1-6]: (.*?) \(author: 722I0004\)$',analysis,re.M)}
    assert set(goals)==set(range(1,7)),'Frozen analysis must declare the six exact goal names'
    for n in range(1,7):
        text=normalize(resolve(REPORT/f'III_3-{n}_UC-{n:02}.md'))
        assert text.splitlines()[0]==f'## 3.{n} Design for Use Case {n}: {goals[n]} (author: 722I0004)',(n,'Exact frozen UC name/title')
        expected=[f'3.{n}.{i} '+title for i,title in enumerate(['Design Classes in Detailed Design','Design Class Diagram','OOD with CRC Cards or Communication Diagram','OOD with Sequence Diagram','Final Design Class Diagram'],1)]
        previous=-1
        for title in expected:
            pos=text.find(title);assert pos>previous,(n,title);previous=pos
        for sub in ['i. Domain design class','ii. Controller','iii. UI (view)','iv. Data access','v. Design class (all layers together)']:assert sub in text,(n,sub)
        assert f'(author: 722I0004)' in text,(n,'author title')
        parts.append(text)
    result='\n\n'.join(parts)+'\n';assert '<!-- include:' not in result
    (REPORT/'III_system_requirements_design.md').write_text(result,encoding='utf-8')
    parts=['# IV. System Requirements Implementation (10 marks)',AUTHOR,'The filled subsections below are design sources for 4.1–4.3.2. Actual UI, SQL/method excerpts and integration evidence are delivered in the named later phases. Diagram targets retain their C0 status.']
    for name in ['IV_4-1_subsystem_dcd.md','IV_4-2_package.md']:parts.append(normalize(resolve(REPORT/name)))
    parts.append('## 4.3 Implementation\n\n'+AUTHOR)
    for name in ['IV_4-3-1_mapping.md','IV_4-3-2_dao_sequences.md']:parts.append(normalize(resolve(REPORT/name)))
    for n,title,pending in [(3,'UI Design','P5, sketch, wireframe, mockup, prototype and SSD-to-UI trace'),(4,'SQL Code','P7, database/table creation and sample SQL data excerpts'),(5,'Software Classes Method Code','P7, verified source excerpts and tagged code links'),(6,'Integration of Use Cases','P5, cross-role integration scenarios and evidence')]:parts.append(f'### 4.3.{n} {title}\n\n⟦PENDING: {pending}⟧')
    result='\n\n'.join(parts)+'\n';assert '<!-- include:' not in result
    (REPORT/'IV_system_requirements_implementation.md').write_text(result,encoding='utf-8')
    print('Assembled III and IV from source parts; includes resolved; exact required heading order checked.')
if __name__=='__main__':main()
