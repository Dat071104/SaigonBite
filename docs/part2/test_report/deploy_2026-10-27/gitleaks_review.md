# Tracked-file secret-scan review, 2026-10-27

- Scanner: `zricethezav/gitleaks:v8.28.0`, digest `sha256:cdbb7c955abce02001a9f6c9f602fb195b7fadc1e812065883f695d1eeaba854`.
- Scope: copies of the 3,538 paths returned by `git ls-files`, using their working-tree bytes, scanned with `gitleaks dir --redact=100`. This scan does not claim to scan Git history or files that were untracked at the time. Raw report is redacted in `gitleaks.json`.
- Result: exit 1, 66 generic-api-key findings. Reviewed against source lines: 64 are 64-character SHA-256 source or module digest entries in historical P4 handoff/audit files; 2 are traceability rows NFR-04 and NFR-08 containing a historical Git revision and test path `test_production_requires_secret_and_secure_settings`. These are audit metadata, not credentials. Confirmed credentials: 0 in these 66 findings.
- Demo account passwords documented in README are intentional public demo credentials; the scanner did not separately flag them. The public demonstration must use synthetic data only.
- The scanner is heuristic; it cannot prove the absence of every possible secret. Re-scan the final tracked release after the new P6 files are committed.
- Release candidate scan: after staging P6 files, 3,549 tracked/staged paths were copied and scanned with the same redaction. `gitleaks_release.json` contains the same 66 rule/file/line findings and no additional findings. The initial review above applies. This is the release candidate before the release commit; later evidence-only files are not included.
