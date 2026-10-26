# P5-root report: UI trace and integration evidence

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5, root). 27/10/2026. Entry HEAD 51e5122 (915 passed). Final runtime commit 252ada1 (928 passed, 0 failed/error/skip; `test_report/2026-10-27_252ada1.txt/.xml`). G5 verdict: **READY-EXCEPT-OWNER**.

**P5.1 (UI trace).** 47 screens (goal screens and key alternatives) cover all 41 SSD occurrences (`ui/coverage_check.md`). Per use case: sketch brief, wireframes and mockups (HTML/CSS, AI-assisted, exported to PNG), implemented screenshots of the real app at 252ada1, and a trace table SSD operation → screen/control → validation (BR ids) → displayed result → controller method (every controller call checked against the view code). Figma kit ready (141 frames, 148 hotspots). The draft screens were photographed and measured first: contrast passed everywhere (lowest 5.25:1) but My orders overflowed on a phone (449 px on 390), the sales table at 768 px (967 px) and every screen had targets under 44 px. Ten UI commits refined the real app (templates, `style.css`, `app.js` only; ids, field names and asserted texts unchanged); after them 47 of 47 screens measure clean (`ui/refinement_log.md`).

**P5.2 (integration).** Seven scenarios and a CSRF check in one fresh demo DB, one Edge profile per role, same order id across roles: final run 60 of 60 steps (`test_report/integration_2026-10-27/README.md`). Expected results were written and hashed first; one wrong edit of mine (S3.6) was restored to the original bytes and its history kept; S7's "-0 VND" expectation was corrected before any run when the template was fixed. Runs t1 to t3 failed only on my script errors.

**Defects (all found in the browser, none visible to the 915 API/DAO tests):** P5-D01 dish price field refused every seed price (b68bfef); P5-D02 false "price changed" on online payment (ce18bf6); P5-D03 lost pick-up ended on a 403 page with no way forward (1776293, partial); P5-D04 raw 0.3897… km (5466f6a); P5-D05 refund wording (252ada1). 13 new tests, each failing before its fix.

**Needs Dat (not fixable inside P5):** P5-D03 remainder (two red boxes after a lost pick-up, `delivery.py`) and P5-D06 (decline banner always mentions an online refund, `order.py`). Both modules are sealed by the G4 dependency policy; changing them needs an owner-reviewed update of the seal in `docs/part2/implementation/` (protected). Neither changes money, state or a rule. A strict reading of "open defect = NOT READY" would turn the verdict into NOT READY until Dat decides.

**Subagents:** worker_A (UC-05, UC-02) and worker_B (UC-03, UC-06, UC-04), Sonnet 5.5, source authoring only, ~5 min each in parallel with the browser runs; root reviewed and patched. No fix subagent, no critique subagent.

**Owner steps left:** sketches (`UC-0x/sketch_brief.md`), Figma file from `ui/figma_kit/FIGMA_STEPS.md`, then the logged-out link check and `links.json`. No push, tag, upload, Drive or external action.
