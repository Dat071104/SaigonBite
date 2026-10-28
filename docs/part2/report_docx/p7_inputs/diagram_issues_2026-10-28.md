# P7 figure issues — candidate audit, 28 October 2026

This is a candidate-source audit, not a finalized placement manifest. No protected diagram was changed. The ten source PNGs listed below were opened in the Codex viewer, not in a compiled report; this does not establish final DOCX/PDF placement.

Decided 28/10 (Dat/Claude): the passing threshold is 9.0 pt. The 53 candidates previously flagged at 9.5 pt estimate 9.071–9.483 pt at 230 mm and therefore pass at that width. The final placement width must still be used for each selected figure. The calculation can include captions or footers; it does not by itself identify a broken or illegible diagram. Screenshots without vector text sizes remain unmeasured.

Candidate details: `Part2/notes/P7/figure_font_candidates.csv`.

Ten opened source samples:

- `models/shared/business_process_v2.png`
- `models/UC-01/activity_uc01_PartA.png`
- `models/shared/sm_order.png`
- `models/UC-01/dcd_uc01_domain_PartA.png`
- `models/UC-02/dcd_uc02_domain_PartA.png`
- `models/UC-04/dcd_uc04_domain.png`
- `models/shared/dcd_subsystem_PartA.png`
- `models/UC-01/seqdao_uc01_confirmCheckout_PartA.png`
- `docs/part2/ui/UC-01/wireframes/UC-01-S01.png`
- `models/shared/stakeholder_chart.png`

Several design diagrams visibly retain the historical C0 target notation in the figure itself. These are frozen source diagrams; the report needs a current-status explanation linked to the resolution register. Do not infer that a figure has been updated to P4.

## Whole-view PNG conflict — 28 October 2026

Eight checked base PNGs (shared use-case and domain models; UC-01, UC-05 and UC-06 activity and SSD views) are byte-identical to their PartA exports; they are not whole views. Each has three split parts. P2 records state that the unsuffixed editable draw.io contains the pages while the unsuffixed PNG is a first-page alias. A stem and filename inventory did not identify a separate whole-view PNG for these diagrams. Details and SHA-256 values: `Part2/notes/P7/panorama_conflict.json`. The existing split views cannot also be duplicated in an appendix under B3; exporting new whole views conflicts with the 28 October no-re-export decision. No diagram was changed.

## Selection and placed-size checks — 28 October 2026

Dat’s decision replaces the earlier panorama conflict: team-wide PartA appears in both body and appendix, the remaining team-wide parts appear in the appendix, and per-use-case figures appear in the body with appendix references. No new PNG was exported. The subsystem has 68 parts (A–BP), all selected.

The selected figures with no hash-matched P2/P3 receipt were opened as 17 contact sheets. This demonstrates that their images could be viewed, not that every character is readable at the eventual printed size. Ten prospective page placements were also opened as 96-dpi page simulations; these are not the final Word or LaTeX layout. One 230-mm landscape simulation overflowed the page (`seq_uc03_listHubs.png`). Seventy-seven selected model placements were changed to portrait widths to fit a 250-mm image height; 12 estimate below 9.0 pt at that width (minimum 6.96 pt), based on their SVG font sizes and viewBox.

For screenshots, a simple estimate using the application’s 16-px default body font and the selected image width puts 123 below 9.0 pt; smaller labels and notes can be smaller still. This estimate is not a measurement of every embedded character. The manifest marks these exceptions, which require layout or scope resolution before claiming the B3 readability criterion is met. Model sources and UI screenshots remain unmodified.

## Placement refinement — 28 October 2026

The previous screenshot widths were conservative. Allowing each screenshot to use the larger of a 170 x 250 mm portrait image box or a 230 x 180 mm landscape image box reduces the number with nominal 16-px body text estimated below 9 pt from 123 to 110. The 12 model placements estimated below 9 pt remain, so 122 figure placements are flagged in total. These are estimates; final Word/LaTeX margins, captions and rendered text are not verified.

## Readability exceptions — owner decision 28 October 2026

Screenshots are evidence images and are exempt from the 9 pt diagram threshold. Original PNGs use the largest selected box without downsampling; captions or surrounding text describe the evidence. Stage 2 checks final pages at 100% and 200%. The following 12 model placements remain at their maximum selected size without re-export; their captions identify the editable source. Estimates are not rendered-page measurements.

- P7-0282: 7.886 pt; `models/UC-02/activity_uc02_PartA.drawio`
- P7-0283: 7.886 pt; `models/UC-02/activity_uc02_PartB.drawio`
- P7-0284: 7.886 pt; `models/UC-02/activity_uc02_PartC.drawio`
- P7-0285: 7.886 pt; `models/UC-02/ssd_uc02_PartA.drawio`
- P7-0286: 7.886 pt; `models/UC-02/ssd_uc02_PartB.drawio`
- P7-0289: 7.886 pt; `models/UC-04/activity_uc04_PartA.drawio`
- P7-0290: 7.886 pt; `models/UC-04/activity_uc04_PartB.drawio`
- P7-0291: 7.886 pt; `models/UC-04/activity_uc04_PartC.drawio`
- P7-0292: 7.886 pt; `models/UC-04/ssd_uc04.drawio`
- P7-0514: 8.581 pt; `models/shared/stakeholder_chart.drawio`
- A1.3: 7.83 pt; `models/shared/use_case_diagram_PartC.drawio`
- A3.3: 6.96 pt; `models/shared/domain_model_PartC.drawio`
