# P4 consolidated root assessment

Author: 722I0004 · AI-assisted (Codex)

**G4 BLOCKED — P4-B02.** All nine implementation subphases have recorded handoffs. The exact committed executable revision `4a661ea255207842abc4f6e835f0f1e76f21567b` collected 877 tests and passed all 877 in 50.85 seconds, with zero failures, errors, skips or xfail and no exclusions. Root worked sequentially (workers=0). This is one consolidated root assessment, not an independent approval. P5–P8 have not started.

## Required architecture decision

The remaining material flaw is 12 DAO→domain module pairs in 10 DAO/simulator modules. The strict frozen downward package graph forbids them while frozen MATCH DAO return types require domain objects materialised in DAO bodies. Eleven presentation pairs were actually removed through a controller interface and injected navigation. All 23 historical pairs /44 records are individually dispositioned. Domain remains I/O-free, views execute no SQL, controllers own write transactions. The test that asserts 12 known pairs inventories the blocker; it does not qualify architecture compliance. See `implementation/p4_architecture_conflict.md` and `p4_import_disposition.csv`.

G4 cannot become READY without owner authorization for a specific frozen architecture/model revision (neutral DAO DTOs and controller materialisation), or an explicit documented mapper exception with matching design evidence and validation. Neither is adopted. Owner A2 permits only current-schema class/table mapping. Its original P3 snapshot/hash and historical G3 verdict remain preserved. No checker relaxation, incomplete mode or implicit exception was used.

## Implemented behavior and consolidated review

- Foundation: fresh-v2 fixtures, end-to-end created_at, read-only migration refusal, FK/WAL/NORMAL, production secret/cookies, CSRF and BEGIN/body/COMMIT failure handling. No existing DB opened for mutation.
- Hub/ordering: real actor CRUD and archive guards, raw 8km boundary/started-km fees, quiet/capacity rules, voucher/Vietnam-day boundaries, full quote fingerprint, replay isolation, simulated authorization release and independent-connection last-slot/same-token races.
- Kitchen/delivery: current-offer/target guards, offered-price snapshots, exact C/T refund-owed oracle, full captured C on unfulfilled outcomes, serialized races, one delivery at READY, exclusive pickup, assigned actor/exact COD, atomic paired terminal states and privacy.
- Catalogue/account/Admin: scoped actor CRUD, independent per-hub listing state, initial unavailable insert atomicity, retained uniqueness and snapshots, subtype/nationality/linked-role constraints, conditional saves, per-ID terminal archive retaining populated order/line/payment/delivery/offer history.
- Reports: SQL fixture and handwritten expected values sealed before first production query. Sales T=160000 and owed=10000 remain separate; ID-grouped top items retain the four-value tuple. Delivery wait n=3/mean20, successful ride n=2/mean25, failure1/3. Empty periods show n=0/n.a. Workload retains archived hubs and all open-state counters. Actual query connection denies writes; missing relationships fail truthfully.

Root reviewed the consolidated critical money/state/security/concurrency/semantic diffs after P4.9. Serial repairs include discarded failed-rollback connections, strict invalid replacement choices, immutable identity/subtype guards, controlled missing report facts, workload counters/empty rendering, and a real populated replacement→delivery→archive aggregate test. Changed-input suites were rerun; final 877 supersedes earlier 876 receipts. WAL initialization and two test-hook regressions were corrected. No original historical assertion obligation was dropped and no historical verdict was relabelled.

## Reconciled evidence

`implementation/p4_evidence_summary.json` binds exact passing nodes and JUnit. Coverage contains 30 main anchors, 21 supporting PCs, nine guard sections and nine failure sections (69 rows). All 121 frozen input rows /96 elements remain: 109 scoped verified rows and 12 explicit architecture blockers. The frozen SSD denominator remains 41 occurrences /39 UC-operation pairs /38 referenced op IDs (60 catalogue IDs; three listCatalogue occurrences). Counts are denominators, not substitutes for assertions.

All 56 historical test functions remain, with original source hashes/assertion counts retained. The current inventory lists 877 expanded passing nodes. The 78 GET/POST route-method pairs have 546 role cases plus 14 additional foreign-owner/hub/assigned cases. HEAD follows GET; automatic OPTIONS/static are explicitly outside that matrix. There are 52 semantic requirement joins; negative regressions reject the three original nonempty wrong mappings. Status remains Analysed/Planned; NFR04/09 and native/browser/deployment work are not promoted. The 13-table scoped CRUD matrix distinguishes aggregate lifecycle paths and archive from unrestricted delete or seed-based creation.

Raw final output, original receipt and JUnit are `test_report/2026-10-26_4a661ea255207842abc4f6e835f0f1e76f21567b.txt/.json/.xml`, with collection output `.collection.txt`. Raw log SHA-256 `6c16a20649536af09bbc55ce5ae05e8b1f45d70206bc08ffbf885a9f5e1205e9`. JUnit SHA-256 `ad325099fd6f4b458983466b1820dba7ca5b0fdbf42fa23b410b24d5cd138b82`. Project Python3.13.2 and all14 pins were verified. Each source commit has an unchanged Static design-check receipt; the tested revision has 24,835 checks /0 failures. The final evidence-only commit must receive its own check. Executable, auxiliary test-control and semantic-trace-input equivalence are programmatically checked after commit; otherwise this result cannot qualify a later revision.

`p4_source_index.json` hashes controlling and frozen design/analysis inputs. Source reading is not a claim that native PDF/Word/Excel/Figma applications were opened. Original entry assessment is archived as `Part2/notes/P4-root/entry_assessment_c615a80.md`; original independent P3 NOT READY remains unchanged. Nine `P4.n_handoff.json` files bind their actual executions, followed by explicit commits/checks:

```text
c615a80bb3673b10a293ee7630de721b2bc7eb3d Part 2 P4: preserve entry evidence and record frozen mapping blocker
77589e5aa2662db91fd1ef4cc70c3273e4e4d160 P4.1: implement UTC account creation fact under owner mapping exception
42628cd1eb7f8a9cacfafaa79d53841158238aed P4.1: restore v2 fixtures and enforce transaction, fresh-schema and CSRF guarantees
08c1d6d8b26787c063a8b5eb52ff3ab135db4f00 P4.2: enforce retained hub history, checked saves and archive guards
39ab0f0c64962e49449c19e45bc2681dfa064717 P4.3: bind full quote consent and preserve raw distance and payment atomicity
7c1ada3940567fb2dfb0230af7c166ef9bdfe99d P4.4: enforce replacement consent, full refund obligations and stored receipts
2c89af848d3baafe641a61e427f9efa3f0502701 P4.5: verify atomic delivery claims, cash, failure and active-shipper guards
166e5d4f733cb95e610da2c2b83746095a6c5198 P4.6: expose composite catalogue and atomically persist initial listing availability
7948c993f6fce97d5f62037b0f9b2b2b3b19fd67 P4.7: enforce customer identity, checked account saves and per-order archive
487072606df226591daadabc48a9ac22a91035a0 P4.8: correct report identities and net sales against preregistered SQL oracle
5c64e014dabd636195e1f7c8f414c599563f9898 P4.9: verify route permissions, repair semantic trace and retain architecture blocker
b54d91822cbe62935f6a0003530eb8a16b189957 P4 final review: prove workload state counters and rendered empty-report samples
4a661ea255207842abc4f6e835f0f1e76f21567b P4 final review: verify archive of a populated replacement and delivery aggregate
```

## Protection, checklist and final binding

The starting manifest covers 95,359 files, including all 2,329 existing model files (2,327 tracked plus two pre-existing ignored pyc) and 2,328 staging files. Latest pre-closeout verification passed with zero unauthorized mismatches. Only the owner-authorized P4 class/table mapping change is accepted separately, with its P3 snapshot hash verified. Plan, Part1/I1, frozen P2/P3 design/history/checker, workbooks, staging and old database bytes remain protected. The final post-commit rehash is required and reported in `Part2/notes/P4_end_hash_check.json` and `P4_final_receipt.json`.

The external checklist is derived item-by-item from the tests, registers and receipts. At preparation it has 137/144 checked and 7 unchecked: architecture P4-124 plus pending post-commit checks/final delivery. The post-commit receipt and external checklist carry authoritative final counts; this committed report does not pre-claim a future commit hash or receipt. G4 remains BLOCKED regardless of checkbox count. No P5 handoff is authorized.

## Owner facts, measured limits and later evidence

L/Q answers, owner discussion/AI approval, roster changes and official deadline remain unknown/pending. All five client-question slots remain consumed. Keep the 31 October checkpoint and locked defaults. Earlier 92–130h versus84h shortfall is not silently funded; the later plan's154h assumption is not actual hours. Performance ledger records observed receipt windows and test time; interruptions are included, active labor is unmeasured, credits UNAVAILABLE, no mode-efficiency claim.

P5 browser UI/end-to-end screenshots and prototype/Figma linking, P6 native/VM/HTTPS/deployment evidence, and P7 final document/native layout, SQL/code excerpts and final placement remain NOT RUN in this phase. Existing Drive/eLearning/workbook staging is unchanged. No P4 upload, push, tag, merge, deployment, external contact, real payment or spending occurred. Future P5 integration screenshots/steps belong at `docs/part2/test_report/integration_<date>/` under locked plan P5.2. P7 report sections4.3.3/4.3.4/4.3.5 require UI progression, SQL creation/sample queries and tagged code excerpts; section5.2 uses RUNBOOK deployment evidence. No folder creation/upload is required now. Work starts only after the G4 blocker is resolved and the next phase is authorized. STOP at G4.
