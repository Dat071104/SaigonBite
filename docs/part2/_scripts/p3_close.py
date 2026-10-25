"""Verify and record local G3 closure; commits and uploads remain root actions.
Author: 722I0004 · AI-assisted (Codex).
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess
R=Path(__file__).resolve().parents[3];B=R.parent/'Part2';N=B/'notes'
P=Path('C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf-8').strip()
def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','receipt']);a=p.parse_args();start=read(N/'P3_start_hashes.json');protected=read(N/'P3_end_hash_check.json');stage=read(N/'P3_staging_manifest.json');cross=read(N/'P3-root'/f'design_crosscheck_{start["C0"][:7]}.json')
    assert protected['pass'] and cross['pass'] and not cross['incomplete_mode']
    assert cross.get('evidence_hashes'),'Closure requires the post-review checker with current-source hash bindings'
    for relative,digest in cross['evidence_hashes'].items():assert sha(R/relative)==digest,'Cross-check evidence changed; rerun full C6: '+relative
    artifact=read(N/'P3-root/artifact_audit.json');assert artifact['pass'],'Assembled report artifact audit must pass'
    assert artifact.get('source_hashes'),'Artifact audit must bind the final assembled report sources'
    for relative,digest in artifact['source_hashes'].items():assert sha(R/relative)==digest,'Assembled report audit is stale: '+relative
    assert len(artifact['figures'])==cross['figure_files'],'Artifact and cross-check figure sets differ'
    visual=read(N/'P3-root/final_visual_coverage.json')
    assert visual['pass'] and visual['figures']==cross['figure_files'],'Current visual inspection coverage is incomplete'
    for record in visual['records'].values():
        for ext,digest in record['hashes'].items():assert sha((R/record['source']).with_suffix('.'+ext))==digest,'Inspected diagram changed: '+record['source']
        assert sha(Path(record['independent_raster']))==record['independent_raster_sha256'],'Independent visual proof changed'
    assert git('branch','--show-current')=='part2'
    assert not git('diff',start['C0'],'--','saigonbite','tests','db','app.py','init_db.py')
    assert stage['workbook_unchanged'] and stage['eLearning_files']==0 and stage['no_external_upload']
    assert git('rev-parse','HEAD:models')==stage['models_tree_oid'],'Model tree changed after staging; mirror it again'
    expected={str((R/p).resolve()) for p in git('ls-files','--','models').splitlines()}
    assert {str(Path(row['source']).resolve()) for row in stage['records']}==expected,'Staging must cover the entire current committed model tree'
    for row in stage['records']:assert sha(Path(row['source']))==sha(Path(row['target']))==row['sha256'],row
    for row in stage['preserved']:assert sha(Path(row['saved']))==row['sha256'],row
    evidence=read(N/'P3_checklist_evidence.json')
    if a.mode=='prepare':
        history=git('log','--reverse','--format=%h|%s',start['C0']+'..HEAD').splitlines()
        lines=['# Phase 3 closure and P4 handoff','','Author: 722I0004 · AI-assisted (Codex)','','Root final disposition and independent review are recorded separately in P3-root.md and P3-review.md. This is target-design readiness at the fixed committed baseline, not application qualification.','','## Scope and evidence','',f'- Committed application baseline C0: `{start["C0"]}`.',f'- Frozen SSD ledger: 41 occurrences; 39 distinct UC-operation pairs; 38 op IDs. Cross-check covers {cross["SSD_occurrences_covered"]} occurrences and {cross["anchor_count"]} main PC/MG anchors.',f'- New figure/source sets audited: {cross["figure_files"]}; design-sequence views {cross["design_sequence_views"]}; DAO-sequence views {cross["DAO_sequence_views"]}.',f'- Responsibility statuses: {json.dumps(cross["status_counts"])}. Targets/GAPs remain named P4 inputs, not implemented claims.',f'- Protected files unchanged: {sum(protected["counts"].values())}; workbook staged SHA256 `{stage["workbook_sha256"]}`.',f'- Models mirrored locally: {stage["model_files"]} files. Nothing to eLearning; no upload, push, tag or merge.','- Assembled Markdown: report/III_system_requirements_design.md and IV_system_requirements_implementation.md. UI, SQL/method code and integration placeholders name P5/P7.','- Native draw.io editing, native Excel and final DOCX/PDF placement: UNTESTED. App imported/executed/tests run: no.','','## Local commits','','| Hash | Message |','|---|---|']
        lines+=['| '+x.replace('|',' | ',1)+' |' for x in history]
        lines+=['','The final closure commit is written to Part2/notes/P3_final_receipt.json after committing this source.','','## Handoff','',r'P4 element/operation register: `docs/part2/design/P4_design_inputs.csv`; retained F-01…09 and P2-S01…18 are in P2-root.md. Exact rerun command:', '', '```powershell',r"Set-Location -LiteralPath 'D:\RAD\FINAL\SaigonBite'",r"& 'C:\Users\ADMIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 -I 'docs/part2/_scripts/p3_design_crosscheck.py' --commit HEAD",'```','','Targets with behavioral obligations retain their marker until the corresponding committed behavior is reviewed; a matching symbol/signature alone does not establish a behavioral contract.','','Next prompt: P4.1 code foundation unless P4 has already started. Owner facts remain pending: L1–L6 discussion 26/10 and checkpoint31/10; Q1–Q5 dates/answers by31/10; real lecturer feedback and official submission date when known. No new client question or approval is invented.','','## Exact local submission staging','',r'Upload models when ready from `D:\RAD\FINAL\Part2\drive_upload\Part2\models\` (shared/ and UC-01/…UC-06/). The already-staged workbook is unchanged at `D:\RAD\FINAL\Part2\drive_upload\Team02_RAD_Sem01_2627_Team_Workbook.xlsx`. Nothing is prepared for eLearning in P3. Source report sections remain versioned locally until P7 assembly/release.']
        (R/'docs/part2/_agent_reports/P3-closure.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    else:
        assert not git('status','--porcelain'),'Final receipt requires a clean repo'
        head=git('rev-parse','HEAD');evidence['P3-75']={'done':True,'evidence':head[:7]+': '+git('log','-1','--format=%s')+'; D:/RAD/FINAL/Part2/notes/P3_final_receipt.json'}
        (N/'P3_checklist_evidence.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False),encoding='utf-8');subprocess.run([str(P),'-X','utf8','-I',str(Path(__file__).with_name('p3_checklist.py'))],cwd=R,check=True)
        checklist=read(N/'P3_checklist_summary.json');assert checklist['checked']==checklist['total']==69 and not checklist['unchecked']
        out={'author':'722I0004 · AI-assisted (Codex)','completed_at_utc':datetime.now(timezone.utc).isoformat(),'C0':start['C0'],'head':head,'branch':'part2','commits':git('log','--reverse','--format=%h %s',start['C0']+'..HEAD').splitlines(),'checklist':checklist,'protected':protected,'crosscheck':{k:v for k,v in cross.items() if k not in ('results','import_violations')},'staging':{k:v for k,v in stage.items() if k not in ('records','preserved')},'evidence_hashes':{str(path.relative_to(B)):sha(path) for path in [N/'P3_start_hashes.json',N/'P3_end_hash_check.json',N/'P3_staging_manifest.json',N/'P3_prompt_archive.json',N/'P3-root'/f'design_crosscheck_{start["C0"][:7]}.json']},'app_tests_run':False,'native_drawio_Excel_final_DOCX_PDF':'UNTESTED','no_external_upload_push_tag_merge':True}
        (N/'P3_final_receipt.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'head':head,'checklist':checklist['checked'],'protected':sum(protected['counts'].values()),'staged_models':stage['model_files'],'receipt':str(N/'P3_final_receipt.json')},indent=2))
if __name__=='__main__':main()
