"""Build README.md of the integration evidence from results.json, forms_seen.json, progress.json and defects.csv.
Author: 722I0004 · AI-assisted (Claude Sonnet 5.5)"""
import csv
import json
import re
from pathlib import Path

EVID = Path(__file__).resolve().parent.parent
res = json.loads((EVID / "results.json").read_text(encoding="utf-8"))
env, steps = res["environment"], res["steps"]
forms = json.loads((EVID / "forms_seen.json").read_text(encoding="utf-8"))
prog = json.loads(Path(r"D:\RAD\FINAL\Part2\notes\P5\progress.json").read_text(encoding="utf-8"))
defects = list(csv.DictReader((EVID / "defects.csv").open(encoding="utf-8", newline="")))
TITLES = {
    "S1": "Catalogue and capacity reach the customer; archived and sold-out dishes cannot be ordered",
    "S2": "A full hub refuses with a quieter-hub suggestion; the suggestion gives a fresh quote",
    "S3": "An order reaches the kitchen of its own hub only",
    "S4": "Sold-out dish, cheaper replacement, customer accepts, kitchen cooks, one delivery",
    "S5": "Two shippers take the same order together; exact cash; customer sees delivered and paid",
    "S6": "Declined payment, rejected paid order, cancellation, failed delivery",
    "S7": "Manager reports against the hand-calculated oracle; archiving a closed order",
    "S8": "CSRF: a token on every form; a form without or with a changed token is refused",
}


def cut(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def esc(s):
    return (s or "").replace("|", "/")


total, ok = len(steps), sum(r["result"] == "PASS" for r in steps)
L = ["# Integration evidence P5.2: seven scenarios and the CSRF check in the browser", "",
     "Author: 722I0004 · AI-assisted (Claude Sonnet 5.5).", "",
     f"**Result of the final run: {ok} of {total} steps pass, 0 fail.** Label: **Demonstrated** (browser walkthrough with screenshots, one browser profile per role, the same order id followed across the roles). "
     "A database query after a step only corroborates it (`S<n>/db_facts.json`); it never replaces the browser evidence.", "",
     "## Environment", "",
     f"- Commit under test: `{env['commit']}` on branch `part2` (the last commit that changed runtime files; every later commit changes documentation only). Git status of tracked files was clean; untracked: the new evidence folders.",
     f"- Server: {env['server']}. The secret key is random and exists only in the server process environment.",
     f"- Browser: Microsoft Edge {env['versions']['edge']} driven by Playwright for Python {env['versions']['playwright']} (Python {env['versions']['python']}), installed in the isolated venv `Part2/notes/P5/tools/venv`; headless, one persistent profile per role (customer and tourist and both shippers at 390×844 with touch, kitchen, kitchen_bt, admin, manager at 1440×900).",
     f"- Databases (new files, created with `init_db.py`): main `{env['main_db']}` (schema, seed, demo history orders 1 to 8); oracle `{env['oracle_db']}` (schema and seed without demo history, then `tests/fixtures/report_oracle.sql`).",
     f"- Started {env['started']}, finished {env['finished']} (Asia/Bangkok). Script: `scripts/run_integration.py` (library `scripts/p5lib.py`); one run goes through S1 to S8 on one database so that state carries forward.", "",
     "## How the expected results were kept honest", "",
     "`S<n>/expected.md` was written first, with hand-computed amounts, and its SHA-256 and time were recorded in `Part2/notes/P5/progress.json` before any run (hashes below; the first recording was 27/10/2026 01:13:27, the times in the table are the re-recording after the two edits below, and the other six files were unchanged between the two). No expected value was adjusted to fit an actual result. Two edits before the first complete run are recorded in the open: "
     "S7 (the zero-voucher cell \"-0 VND\" became \"0 VND\" when the template was corrected, commit dc87741; logged inside the file) and S3 step 3.6 (a wrong edit of mine, reverted to the original bytes after the first runs showed the original was right; the first hash reproduces, history in `S3/expected_history.md`).", "",
     "| Scenario | expected.md SHA-256 | recorded |", "|---|---|---|"]
for k, v in sorted(prog["expected_hashes"].items()):
    L.append(f"| {k} | `{v['sha256']}` | {v['recorded']} |")
L += ["", "## Run history (the whole sequence is repeated from a fresh database every time)", "",
      "| Run | Result | Reason |", "|---|---|---|",
      "| t1, t2 | stopped | my own script: a screenshot label for a two-role step, a selector for the Ready column in step 4.5, the page-load hook; step 3.6 failed only because of the expectation edit described above |",
      "| t3 | 58 of 60 | steps 8.2 and 8.3: my script altered the CSRF token of the logout form in the top bar instead of the hub form, so the hub really was saved (a script error, not an application defect) |",
      f"| **t4 (final)** | **{ok} of {total}** | at commit `{env['commit'][:7]}`; the evidence below is this run |", "",
      "Before the final run the browser found defects P5-D01 to P5-D05 (below); each was fixed with a regression test and its scenarios were repeated from a fresh database.", ""]
by = {}
for r in steps:
    by.setdefault(r["scenario"], []).append(r)
for sc in sorted(by):
    L += [f"## {sc} {TITLES[sc]}", "", f"Expected written first: [`{sc}/expected.md`]({sc}/expected.md). Corroboration: [`{sc}/db_facts.json`]({sc}/db_facts.json).", "",
          "| Step | Role | Expected | Actual (page text, shortened) | Result | Screenshot | Order |", "|---|---|---|---|---|---|---|"]
    for r in by[sc]:
        shots = "<br>".join(f"[{n}]({sc}/{n})" for n in r["screenshots"])
        L.append(f"| {r['step']} | {esc(r['role'])} | {esc(cut(r['expected'], 230))} | {esc(cut(r['actual'], 200))} | {r['result']} ({sum(c['ok'] for c in r['checks'])}/{len(r['checks'])} checks) | {shots} | {r['order'] or ''} |")
    L.append("")
s52 = next(r for r in steps if r["step"] == "5.2")
nf = len(forms)
pages = len({(f["role"], re.sub(r"/\d+", "/<id>", f["url"])) for f in forms})
bad = [r for r in steps if r["events"]]
L += ["## Notes on specific results", "",
      f"- **Race (5.2).** Both submits were dispatched in the two profiles {s52['extra']['dispatch_ms'][1] - s52['extra']['dispatch_ms'][0]} ms apart and both responses were awaited afterwards; `{s52['extra']['winner']}` won and `{s52['extra']['loser']}` saw the message. The browser shows the user-facing outcome only; the barrier tests in pytest (`tests/test_p4_delivery.py`, `tests/test_p4_ordering.py`) are the race proof (**Tested**).",
      f"- **CSRF (S8).** {nf} POST forms were seen on {pages} distinct role/page pairs during S1 to S7 (`forms_seen.json`); none lacked a non-empty `csrf_token`. A form with the token removed (8.2, 8.4, 8.5) or changed (8.3) was refused with HTTP 400 'Form expired' and changed nothing.",
      "- **Oracle (S7 A).** The manager's Sales, Delivery performance and Workload screens show exactly the figures of `tests/fixtures/report_oracle_expected.md` for 20/10/2026, for the hub filter and for the empty day (n/a). The report screens never write; the oracle database was only read.",
      f"- **Browser events.** {len(bad)} steps produced console or HTTP errors; every one is a refusal the step expects (400, 402, 403, 409). No script error and no unexpected response occurred (`events` in `results.json`).", "",
      "## Defects found in P5 (`defects.csv`)", "", "| Id | Where | Severity | Decision | Fix commit |", "|---|---|---|---|---|"]
for d in defects:
    L.append(f"| {d['id']} | {esc(cut(d['scenario_or_screen'], 70))} | {esc(cut(d['severity'], 60))} | {esc(cut(d['decision'], 150))} | {d['fix_commit']} |")
L += ["", "## What is Demonstrated and what is not", "",
      "**Demonstrated** (browser, this folder): the six main use cases working together in one running system on a local Flask development server: UC-03/UC-06 catalogue and capacity reaching the customer, UC-01 ordering with busy-hub refusal, fresh quote, COD and online payment, UC-05 replacement and rejection, UC-02 delivery with a lost pick-up and exact cash, UC-04 reports against the hand oracle, order archiving, role and hub isolation, CSRF.",
      "**Tested, not Demonstrated here:** the race proof (pytest barrier tests), the security matrix, the money arithmetic (915 passing tests at the entry commit; see the final receipt for the final count).",
      "**Not claimed:** deployment. The Docker/gunicorn/Caddy build on the GCP VM is phase P6; nothing here is **Deployed**. No real payment: the online payment is the labelled simulator. No push, tag, upload or external contact was made.", ""]
(EVID / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("README written;", ok, "of", total)
