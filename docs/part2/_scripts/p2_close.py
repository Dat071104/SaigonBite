"""Build evidence-led local Phase 2 closure; never commits, pushes or uploads.

Run prepare before the explicit root closure commit, then receipt on clean HEAD.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,subprocess

ROOT=Path('D:/RAD/FINAL');R=ROOT/'SaigonBite';B=ROOT/'Part2';N=B/'notes'
P=Path('C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf-8').strip()
def jsonread(p):return json.loads(p.read_text(encoding='utf-8'))
def audit():
 stage=jsonread(N/'P2_staging_manifest.json');protected=jsonread(N/'P2_end_hash_check.json')
 assert protected['pass'] and sum(protected['counts'].values())==1368
 assert stage['model_files']==339 and len(stage['moves'])==39 and stage['eLearning_files']==0
 for row in stage['records']:assert sha(Path(row['source']))==sha(Path(row['target']))==row['sha256'],row
 for row in stage['moves']:assert Path(row['to']).is_file() and sha(Path(row['to']))==row['sha256'],row
 assert not list((B/'drive_upload/Part2/models').glob('*.*'))
 assert not any(p.is_file() for p in (B/'drive_upload/eLearning').rglob('*'))
 assert not git('diff','657089b','--','saigonbite','tests','db','app.py','init_db.py')
 assert git('branch','--show-current')=='part2'
 return stage,protected
def checklist(final=None):
 path=N/'P2_checklist_evidence.json';e=jsonread(path)
 def put(n,evidence,done=True):e[f'P2-{n:02}']={'done':done,'evidence':evidence}
 commits=['bb19e79','79c6566','2cc6db2','297eeda','4cce9b4','46a69e4']
 for uc in range(1,7):
  start=31+(uc-1)*5;code=f'UC-{uc:02}';owner='E' if uc in (1,5) else 'F' if uc in (2,4) else 'G'
  refs=[f'docs/part2/{code}/description.md',f'models/{code}/activity_uc{uc:02}*.drawio + PNG/SVG',f'models/{code}/ssd_uc{uc:02}*.drawio + PNG/SVG',f'docs/part2/report/II_2-2-{uc}_{code}.md; resolved state blocks in assembled II',f'docs/part2/_agent_reports/P2-{owner}.md (pre-integration); P2-root.md closes integration/review corrections']
  for i,ref in enumerate(refs):put(start+i,ref+f'; package {commits[uc-1]}, final corrections fe2fe67; D:/RAD/FINAL/Part2/notes/P2-root/review_visual_receipt.json and analysis_structural_audit.json')
 values={
 61:'P2-root.md Wave 3; E/F/G reports read together only after all finished; every request disposition recorded',
 62:'analysis_consistency.csv (30 anchors); ssd_flow_membership.csv (41 occurrences, exact parameters); Part2/notes/P2-root/consistency_audit.json @ fe2fe67',
 63:'report/II_system_requirements_analysis.md; _scripts/p2_assemble.py + p2_assembly.json; exact ordered headings/includes/state ownership; analysis_structural_audit.json @ fe2fe67',
 64:'traceability.csv @ fe2fe67: 44 anchored Analysed, 8 Planned NFRs, future evidence columns blank',
 65:'Part2/workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx; P2_workbook_preservation.json: 118 formulas,321 green cells,25 validations,13 OK rows; final views verified',
 66:'docs/part2/ai_usage_log.md @ fe2fe67: root,A–G,sole reviewer and interruption/resume/correction history; archived actual prompts',
 67:'13 meaningful local commits through fe2fe67; six UC package commits and 3097dca integration; full log in P2-closure.md',
 70:'P2-review.md NOT READY at 3097dca retained; P2-root.md accepts/fixes R1–R6; p2_review_audit.py and final PNG/SVG inspections close B5 gaps @ fe2fe67',
 71:'30-anchor/41-request ledgers; P2-root.md review dispositions; review_corrections_audit.json + analysis_structural_audit.json; domain/CRUD Static differences remain P4 inputs',
 72:'P2-review.md provenance/English/author checks; P2-root.md corrections; ai_usage_log.md; no invented feedback/member work/app result',
 73:'P2-root.md and P2-review.md: items14–20 physical rows27–33; Rubric Guide P2-II row8; item17 Partial under J2',
 74:'Part2/notes/P2_end_hash_check.json: 1368 protected files equal start, no additions/removals; git app diff vs657089b exits0',
 75:'P2-root.md Wave 4 dispositions: R1–R6 all fixed and verified; original reviewer assessment retained; final visual/semantic receipts',
 80:'Part2/notes/P2_staging_manifest.json: published workbook SHA256 eb9a97714afa92cfdab30943f827883b3de996045d62c340e4268d1159ba31d9; target matches working copy',
 81:'Part2/notes/P2_staging_manifest.json: 339 model files mirrored with shared/UC-01…06;39 flat P1 files moved without deletion; links unchanged;eLearning0;no upload/push'}
 for n,v in values.items():put(n,v)
 put(76,f'{final}: Part 2 Phase 2: close G2 analysis and record submission staging; Part2/notes/P2_final_receipt.json' if final else 'PENDING: explicit root closure commit, then _scripts/p2_close.py receipt',bool(final))
 assert len(e)==74
 path.write_text(json.dumps(e,indent=2,ensure_ascii=False),encoding='utf-8')
 subprocess.run([str(P),'-X','utf8','-I',str(R/'docs/part2/_scripts/p2_checklist.py'),'--evidence',str(path)],cwd=R,check=True)

def main():
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','receipt']);args=p.parse_args()
 stage,protected=audit()
 if args.mode=='prepare':
  checklist()
  history=git('log','--reverse','--format=%h|%s','657089b..HEAD').splitlines()
  lines=['# Phase 2 closure and handoff','','Author: 722I0004 · AI-assisted (Codex)','','Root post-correction disposition: **G2 analysis-ready**. The independent review remains NOT READY at its historical revision 3097dca; R1–R6 were subsequently fixed and checked by root at fe2fe67. This is not a fabricated second independent pass or an application qualification.','','All 74 checklist records have evidence; the final-commit checkbox is completed by the clean-HEAD receipt after the explicit closure commit. Item 17 remains **Partial** under J2: actual author 722I0004 only. Native draw.io, native Excel and final PDF placement are UNTESTED.','','## Outputs and validation','','- Assembled Section II: report/II_system_requirements_analysis.md, with team analysis, six UC packages and five actor CRUD tables.','- Versioned operation/anchor/consistency/request/traceability sources; 60 operations,30 verbatim anchors,41 request occurrences,44 Analysed rows,8 deliberately Planned NFRs.','- 60 new draw.io/source-export sets,52 unique placed views; all exports inspected. All13 revised unique PNG/SVG pairs were reopened by root after review.','- Guarded workbook:118 formulas,321 lecturer cells,25 validations unchanged;20 events,13 union rows OK.','- All1,368 protected files match start; app diff against657089b exits0. Part1,Section I,plan and links unchanged. No application tests run.','','## Local commits','','| Hash | Message |','|---|---|']
  lines += ['| '+row.replace('|',' | ',1)+' |' for row in history]
  lines += ['','The final closure commit is recorded in Part2/notes/P2_final_receipt.json after this source is committed, avoiding a self-referential commit hash.','','## Plan issues and pending owner facts','','See P2-root.md Plan issues and Wave1/4 dispositions: five actor subsections extend the three-row template; workbook uses the13-class union; seven existing-scope Read qualifiers reconcile the two plan tables with no added write grants. Locked plan unchanged.','','- ⟦PENDING: L1–L6 actual answers or unanswered status, planned26/10 discussion and31/10 checkpoint⟧. A differing L1/L3/L6 answer requires replan.','- ⟦PENDING: Q1–Q5 answers and original submission dates, Dat by31/10⟧. No invented approval or extra client allowance.','- ⟦PENDING: real lecturer feedback and official Part2 date, when received / eLearning slot opens⟧.15/11 remains the team target.','','## Exact local Drive staging','','| Source to upload | Verified content |','|---|---|',f'| D:/RAD/FINAL/Part2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx | SHA256 `{stage["records"][-1]["sha256"]}` |','| D:/RAD/FINAL/Part2/drive_upload/Part2/models/ |339 files; shared/ and UC-01/ through UC-06/;39 Phase1 flat copies moved without deletion |','','Manifest: D:/RAD/FINAL/Part2/notes/P2_staging_manifest.json. eLearning remains empty. No external upload,GitHub push,tag or merge. Prompts and nine actual transcripts are archived privately in Part2/notes, outside upload staging.','','## Next phase','','P4 inputs remain **Static** in P2-root.md: F-01…09 and P2-S01…18. They cover fixture/schema versioning, raw distance/full quote fingerprint, replacement guards and full-C obligations, commit rollback/simulator release, report grouping/refunds/archive visibility, SQL/domain constraints and supporting-operation mapping. No application repair or runtime result was made in P2.','','The next prompt may be **P4.1** code foundation or **P3** design; they run independently.']
  spacing={'operations,30':'operations, 30','anchors,41':'anchors, 41','occurrences,44':'occurrences, 44','rows,8':'rows, 8','sets,52':'sets, 52','All13':'All 13','workbook:118':'workbook: 118','formulas,321':'formulas, 321','cells,25':'cells, 25','unchanged;20':'unchanged; 20','events,13':'events, 13','All1,368':'All 1,368','against657089b':'against 657089b','exits0':'exits 0','Part1,Section I,plan':'Part 1, Section I, plan','Wave1/4':'Wave 1/4','the13-class':'the 13-class','planned26/10':'planned 26/10','and31/10':'and 31/10','by31/10':'by 31/10','official Part2':'official Part 2','⟧.15/11':'⟧. 15/11','|339':'| 339','/;39':'/; 39','Phase1':'Phase 1','upload,GitHub push,tag':'upload, GitHub push, tag'}
  for a,b in spacing.items():lines=[line.replace(a,b) for line in lines]
  (R/'docs/part2/_agent_reports/P2-closure.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 else:
  assert not git('status','--porcelain'),'Receipt requires clean repository'
  head=git('rev-parse','HEAD');assert git('log','-1','--format=%s')=='Part 2 Phase 2: close G2 analysis and record submission staging'
  checklist(head[:7]);summary=jsonread(N/'P2_checklist_summary.json');assert summary['checked']==74 and not summary['unchecked']
  receipt={'completed_at_utc':datetime.now(timezone.utc).isoformat(),'branch':'part2','head':head,'commits':git('log','--reverse','--format=%h %s','657089b..HEAD').splitlines(),'checklist':summary,'protected':protected,'staging':{'model_files':stage['model_files'],'preserved_moves':len(stage['moves']),'eLearning_files':0,'workbook_sha256':stage['records'][-1]['sha256']},'evidence_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [N/'P2_staging_manifest.json',N/'P2_start_hashes.json',N/'P2_end_hash_check.json',N/'P2_workbook_preservation.json',N/'P2_prompt_archive.json',N/'P2-root/review_visual_receipt.json',N/'P2-root/review_corrections_audit.json']},'no_external_upload':True,'app_tests_run':False,'root_post_fix_G2':'analysis-ready','marking_item17':'Partial under J2'}
  (N/'P2_final_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps({'final_head':head,'checklist_done':74,'staged_models':339,'protected_files_unchanged':1368,'receipt':str(N/'P2_final_receipt.json')},indent=2))

if __name__=='__main__':main()
