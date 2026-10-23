# P1-C completion report - Process diagrams

Author: 722I0004 · AI-assisted (Codex)

Date: 23/10/2026. Scope: P1-13-P1-15 only. No git commands, application/test/workbook changes, Part 1 writes, other worker report reads or further delegation occurred. The existing copied `business_process_v2.drawio` was inspected and then regenerated to apply the locked Part 2 contracts and A4 geometry. This report is a single completed-workstream handoff.

## Checklist evidence

| ID | Status within this write set | Evidence |
|---|---|---|
| P1-13 | Complete | `models/shared/business_process_v2.drawio`, `.svg`, `.png`; six main UCs and nine SUCs visible; supporting operations are in scope; complaint/refund decision/payout/rating grey; future features explicitly unimplemented. The original Part 1 source was read only. |
| P1-14 | Complete | `models/shared/swimlane_v2.drawio` has Overview + Parts A-G; `.svg` / `.png` overview plus separate source and exports for each detail. Six required lanes appear in Overview. Details contain guarded radius, busy, declined payment, kitchen confirm/reject/replace, customer accept/decline, delivery success/failure and cancellation paths with the plan's states. |
| P1-15 | Complete under the shared common caption instruction | `docs/part2/report/I_1-5_1-6_process.md` links all nine figures and their sources. All nine SVG-rendered PNGs and all nine A4 proof images were visually inspected. Minimum 16-unit text becomes 9.48 pt at 230 mm wide on A4 landscape. Common exact caption is `Author: 722I0004 · AI-assisted (Codex)`. See caption normalization below. |

## Files written

Final model sources and exports (27 files):

- `models/shared/business_process_v2.drawio`, `business_process_v2.svg`, `business_process_v2.png`.
- `models/shared/swimlane_v2.drawio`, `swimlane_v2.svg`, `swimlane_v2.png`. The draw.io file bundles all eight swim-lane pages.
- `models/shared/swimlane_v2_PartA.{drawio,svg,png}`: quote, raw radius and busy-hub refusal.
- `models/shared/swimlane_v2_PartB.{drawio,svg,png}`: checkout revalidation and simulator.
- `models/shared/swimlane_v2_PartC.{drawio,svg,png}`: kitchen decision, preparation and READY.
- `models/shared/swimlane_v2_PartD.{drawio,svg,png}`: replacement consent and amount effects.
- `models/shared/swimlane_v2_PartE.{drawio,svg,png}`: delivery, cash, failure and receipt.
- `models/shared/swimlane_v2_PartF.{drawio,svg,png}`: cancellation.
- `models/shared/swimlane_v2_PartG.{drawio,svg,png}`: independent administration and manager reports.

Reproduction and verification sources:

- `models/shared/business_process_v2.py` (shared renderer/builder; no original builder is imported or run).
- `models/shared/business_process_v2.json` (business model specification).
- `models/shared/swimlane_v2.json` (swim-lane model specifications).
- `models/shared/business_process_v2.qa.json` (structural results, original-source SHA-256, export hashes, legibility and visual-review record).
- `models/shared/business_process_v2.a4.png`, `swimlane_v2.a4.png`, `swimlane_v2_PartA.a4.png` through `swimlane_v2_PartG.a4.png` (nine internal A4 review proofs; not required submission exports).
- `docs/part2/report/I_1-5_1-6_process.md` (exact template headings, captions, explanation, scope and placement instructions).
- `docs/part2/_agent_reports/P1-C.md` (this handoff).

Temporary export tooling also created `models/shared/business_process_v2.browser/`, a new isolated headless Edge profile. **Do not stage or upload that directory.** It is not an existing user browser profile. Cleanup status is recorded below.

## Actual verification

Executed with bundled Python `C:/Users/ADMIN/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -I -X utf8`:

1. Built through `models/shared/business_process_v2.py`; the command printed all nine SVG basenames with PNG size `(2200, 1520)` and exited 0. Headless Edge was launched with `CREATE_NO_WINDOW`, captured stdout/stderr, an isolated profile and a bounded timeout.
2. Parsed the final SVGs and draw.io XML. The checker printed: `PASS: 9 SVG/PNG pairs; 1 + 8 draw.io pages; all cell references valid; 27 report links resolved; 16-unit minimum = 9.48 pt at 230 mm.`
3. The builder checked action/decision incoming flows, decisions' outgoing guarded paths, initial/final constraints and references for every activity detail A-G. Overviews are explicitly maps/indexes and were not falsely passed as detailed UML activities.
4. Every page passed node overlap, action/decision text-fit, guard label overlap and edge-through-unrelated-node checks. All viewBoxes are 1100 x 760 (ratio 1.447, within the balanced-diagrams range). The business overview uses the skill helper's adapted grid-wrap calculation; activity details use deterministic lane/column grids and orthogonal obstacle-aware routing. No claim of zero edge-edge intersections is made: C/E contain short shared incident-edge stems, with distinct guard labels and explicit endpoint references in XML.
5. Opened every matching SVG-rendered PNG with `view_image`; corrected label/notes interference, delivery-to-receipt overlapping arrows, and snake direction before the final pass. All nine final figures were subsequently reviewed again as A4 landscape proofs (1123 x 794 px at 96 dpi, image width 230 mm). No clipped text, overlapping node text or unreadable labels were observed at that placement.
6. The 16-unit minimum at width 230 mm is `16 * 230 / 25.4 * 72 / 1100 = 9.483 pt`. Figure height is 158.9 mm. Width 218.3 mm is the minimum 9 pt placement. **Root must retain landscape pages and this minimum width when assembling the final report; a portrait-width insertion fails the gate.** Actual final PDF placement is still P7 work.
7. Original Part 1 source SHA-256 read during generation: `b6f04669cbfdb10685c83b43efaa435624d8b5d4d9312f8d6aa4b2e84624934c`. It is also stored as `sourcePart1SHA256` in `business_process_v2.drawio` and in QA JSON. The worker performed no Part 1 writes; the root owns comparison against the preserved start manifest.

No application tests were run or claimed: this workstream creates process documentation only. XML was parsed and all endpoints resolved, but no native draw.io application opening is claimed. PNGs are actual browser rasterizations of the supplied SVGs, not independently redrawn pictures.

## Contract decisions represented

- Order: PLACED, CONFIRMED, PREPARING, READY, OUT_FOR_DELIVERY, DELIVERED, DELIVERY_FAILED, REJECTED, CANCELLED. No stored waiting/busy state.
- Delivery: AWAITING_PICKUP, PICKED_UP, DELIVERED, FAILED. Invalid finish leaves OUT_FOR_DELIVERY and permits another valid finish request; there is no redelivery loop.
- ReplacementOffer: OFFERED -> ACCEPTED / DECLINED / WITHDRAWN. Accepted/withdrawn offers return a PLACED order to the kitchen decision; stale responses never revive a closed order.
- COD starts PENDING, finishes PAID on exact delivered cash, otherwise becomes VOIDED on an unfulfilled terminal outcome.
- ONLINE starts PAID through an explicitly labelled simulator; unfulfilled terminal outcomes become REFUND_PENDING with full captured C owed. A cheaper replacement leaves PAID plus partial refund owed. Payout is grey/deferred; no REFUNDED path is supplied.
- Cancellation and management/report requests are separate activities. Flow finals end refused/invalid request paths; activity finals end the activity shown. Continuation circles connect page fragments without creating concurrency.
- Admin and Manager remain separate lanes and roles. Reports read archived records without writing data. Order archiving preserves history, receipt and refund liabilities.

## BLOCKED / ASSUMED

- **Caption normalization:** P1 checklist wording says `AI-assisted (Codex/Sol 6.1)`, while the common phase prompt, shared brief and direct delegation require `AI-assisted (Codex)` and prohibit inventing a runtime model. Applied the common exact caption everywhere. Root can record this checklist text normalization; no model identity was inferred.
- L3 scope defaults remain unconfirmed. Grey activities are business context, not claims of lecturer approval or working features. The source still requires root's independent review before checklist integration.
- The overall swim-lane page is a readable six-role responsibility index; seven linked detail pages carry the activity guards. The business overview is readable without splits. This avoids shrinking a giant single activity to illegible A4 text.
- Native draw.io rendering remains unverified. Editable XML uses standard shapes and explicit geometry; SVG/PNG visuals, XML references and text sizing are verified. A final native app review may be useful if a renderer changes the state-final stencil.
- **Temporary profile cleanup blocked:** automatic command approval review rejected the cleanup command for `models/shared/business_process_v2.browser/` (and temporary A4 proofs), reporting `blocked by policy` without a more specific reason. No deletion workaround was attempted. The isolated profile and useful A4 proofs remain. Exclude the profile from explicit staging/upload; the root may retain proofs as internal QA or remove them with an approved method. This does not change the 27 final diagram deliverables.

## Sources used

- `docs/part2/_agent_reports/P1-brief.md`.
- `D:/RAD/FINAL/Part2/codex/P1_PROMPT.md` (entire prompt), `P1_CHECKLIST.md` (P1-13-P1-15 and integration boundaries).
- `D:/RAD/FINAL/PLAN_SaigonBite_Part2_Final.md` sections 1-4 and P1.
- `D:/RAD/FINAL/Part2/README.md`, `content/links.json` (read only).
- Primary `Lec_re/RAD_Sem01_2627_Case_Study_SaigonBite.pdf`, both pages; primary `RAD_Sem01_2627_FinalProject_Requirements_SaigonBite.pdf`, relevant sections including pp.2-4 and 8, extracted directly with pypdf.
- `Part2_Plan_Review/source_evidence/Report_Template.txt` for the exact 1.5 and 1.6 headings.
- Frozen `Part1_v2/models/SaigonBite_Business_Process.drawio`, `build/proc_build.py`, `proc_geom.py`, `proc_views.py`, `notes/diagram_changes.md`, read without executing original builders.
- `D:/RAD/FINAL/balanced-diagrams.skill.txt`, opened with zipfile: `balanced-diagrams/SKILL.md` and `scripts/layout_drawio.py`; adapted grid search and style/geometry conventions into the owned builder.
- Bundled PDF skill read for primary-source extraction/verification guidance. No PDF artifact was authored.

## Root next steps

Review these files only after all worker reports arrive; merge consistency once. Stage the 27 final diagram files, the builder/specifications/QA JSON and report section explicitly as desired. Exclude the headless browser profile. Stage/upload the final exports to the Part 2 models folder, retain landscape placement instructions, add this AI work to the root-owned usage log, then mark P1-13-P1-15 with the evidence above. Root owns the frozen-boundary hash comparison, workbook/checklist updates, commits and final report integration.
