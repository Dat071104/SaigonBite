"""Figure 4.2A; same editable JSON/mxGraph + PIL/SVG convention as P3.
Balanced-diagrams: 1800x1360 (1.32), layered four-package graph, short labels.
Author: 722I0004 · AI-assisted (Codex). Native draw.io editing UNTESTED.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
REPO=OUT.parents[3]
spec=importlib.util.spec_from_file_location('frozen_renderer',REPO/'models/shared/use_case_diagram.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
renderer.OUT=OUT


def build():
    policy=json.loads((OUT/'policy.json').read_text())
    audit=json.loads((OUT/'adoption_audit.json').read_text())
    assert audit['pass_'] and audit['exact_dependency_set']
    p=renderer.Page('package_4_2A','Current P4 package amendment | SB-P4-B02-20261026','4.2A',1800,1360)
    p.texts[-1]['text']='Current P4 dependency projection · team decision; no lecturer/client approval'
    p.node('view','«package» presentation\nRoutes, forms and result rendering\nUse the named controller presentation contract\nNo direct DAO / domain / root imports or SQL',450,90,900,210)
    p.node('controller','«package» business.controllers\nAuthorisation, current-state validation and orchestration\nOwns write transactions via immediate_transaction\nInvokes domain behavior and DAO persistence',450,410,900,210,fill='#E9F4EF')
    p.node('domain','«package» business.domain\nEntities, enums, factories, pure rules\nNo outward application dependency\nNo persistence / network / UI I/O',60,760,730,220,fill='#F2EFF9')
    p.node('dao','«package» data_access\nSQL mapping and guarded persistence\nDatabase helper implements caller transaction\nExisting payment simulator enum adapter',1010,760,730,220,fill='#FFF2E6')
    p.edge('request','view','controller',[(900,300),(900,410)],'runtime request',920,340,kind='nav')
    p.edge('behavior','controller','domain',[(600,620),(600,690),(425,690),(425,760)],'runtime domain calls',65,655,kind='nav')
    p.edge('persist','controller','dao',[(1200,620),(1200,690),(1375,690),(1375,760)],'runtime persistence calls',1250,655,kind='nav')
    p.edge('mapper','dao','domain',[(1375,980),(1375,1050),(425,1050),(425,980)],'source dependency: exact policy + use ledger only',530,1010,kind='include')
    pairs=len(audit['pairs']);symbols=sum(len(x['symbols']) for x in audit['pairs'])
    p.node('scope',f'Narrow permission: {pairs} directed pairs / {symbols} imported symbols, recomputed from the application.\nMapper constructors/factory, stored-value properties and enum serialization; terminal/active SQL constants.\nSimulator: OnlineOption contract and .value logging. No workflow, pricing, refund or transaction decision in DAOs.\nSolid open arrow = runtime responsibility; dashed open arrow = admitted source dependency.\nProjection only: exact module/symbol/use details are in policy.json + symbol_use_review.json + dependency_overlay.json.',60,1080,1680,190,kind='note',fill='#FFF8E8')
    data=p.export();data['amendment']=policy['id'];data['frozen_model_sha256']=policy['frozen_model_sha256'];data['actual_pairs']=audit['pairs'];data['native_editing']='UNTESTED';data['scope']='Current P4 projection; frozen P3 model remains declaration authority'
    (OUT/'package_4_2A.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({'figure':'4.2A','nodes':len(data['nodes']),'min_placed_pt':data['min_placed_pt'],'native_editing':'UNTESTED'}))


if __name__=='__main__':build()
