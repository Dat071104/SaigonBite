# Fresh v2 only

Author: 722I0004 · AI-assisted (Codex).

No migration scripts exist. `python init_db.py --db NEW_ABSOLUTE_PATH --no-demo` creates a fresh v2 database. Preserve existing files and their WAL/SHM companions; never use `--force` on retained data.

`--migrate --db EXISTING_PATH` opens read-only to check `user_version`. Version 2 succeeds without changes. Versions 0, 1 and future versions return nonzero with a fresh-v2 refusal; a missing path returns nonzero without creation. This validates, never upgrades. No deployment is claimed.

Run P4 tests through `docs/part2/_scripts/p4_execute.py MODE [pytest arguments]`; it uses fresh file-backed DBs under `Part2/notes/P4_test_scratch/` and records commands and executable hashes.
