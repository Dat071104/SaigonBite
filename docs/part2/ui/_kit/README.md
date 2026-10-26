# UI kit: how a UC package is made

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). Wireframes and mockups are **authored as HTML/CSS (AI-assisted)** and assembled and linked
in Figma by the owner; they are not drawn natively in Figma. The draft screens of the app were built first (I1 to P4); everything here is
**UI design refinement after the draft build**.

## Files

| File | What it is |
|---|---|
| `wireframe.css` | greyscale ramp over the app's grid; `{{p:..}}` placeholders look like grey chips |
| `mockup.css` | imports the app stylesheet (no second palette) |
| `deltas.css` | the refinement rules R1 to R6 shown by wireframes and mockups; the same rules are in `saigonbite/presentation/static/style.css` (see `../refinement_log.md`) |
| `build.py` | `UC-0x/src/<id>.html` → `UC-0x/wireframes/<id>.html` and `UC-0x/mockups/<id>.html` |
| `render.py` | HTML → PNG at the screen's viewport; overflow, contrast, tap-size and label report (`reports/render_<UC>_<kind>.csv`); hotspots (`reports/hotspots.csv`) |
| `capture.py` | clicks through the real app and photographs every screen (`_before/`, `UC-0x/implemented/`), text of each screen in `captured/<mode>/<id>.txt` |
| `make_screens.py`, `make_trace.py`, `must_survive.py`, `check_width.py` | screen list and coverage, trace tables, list of what a refinement must keep, 768/360 px check |

## Screen source format (`UC-0x/src/<screen id>.html`)

```
<!--screen
id: UC-01-S03
title: Choose dishes, address and voucher
role: CUSTOMER
viewport: 390x844
nav: Order food|My orders|Profile
active: Order food
who: Tran Thi Mai
wide: yes            (optional: the 1120 px measure of the staff screens)
-->
<div class="page-head"><h1>…</h1></div>
… page body, the same markup as the Jinja template renders …
```

* `{{p:Hub name||SaigonBite District 1 Hub}}` shows `Hub name` in the wireframe and `SaigonBite District 1 Hub` in the mockup. Put a placeholder on
  every value that comes from data (names, addresses, amounts, times, ids) and write the **real value** after `||`, copied from
  `captured/before/<id>.txt` (the real app, same case). Never invent a number.
* Keep every label, button text, heading and message exactly as the app shows it (that is the "real labels" rule).
* A control that leads to another screen gets `data-goto="UC-0x-Snn"` (and `data-trigger="…"` when the default "click link / press button" is wrong).
  These become the hotspots of `figma_kit/flows.csv`.
* Exactly one `h1`. Phone screens are 390×844, staff screens 1440×900.

## Commands (repository root `D:\RAD\FINAL\SaigonBite`)

```
python docs/part2/ui/_kit/build.py --uc UC-01
Part2/notes/P5/tools/venv/Scripts/python.exe docs/part2/ui/_kit/render.py --uc UC-01      (Playwright + Edge)
python docs/part2/ui/_kit/make_trace.py UC-01
```

A mockup is accepted when the render report says `ok` (no overflow, contrast ≥ 4.5:1 or ≥ 3:1 for large text, tap targets ≥ 44 px, one h1, every
field labelled). In full-page figures the sticky total bar is shown in the flow (`.summary-bar{position:static}`), otherwise it would float over the middle
of the page.

## trace_notes.csv (hand-written columns of `trace.md`)

`occurrence,control,inputs_validation,displayed_result`: one row per SSD occurrence of the UC in the SSD map (the id after `#`, for example `01S-M03`).
Read the view module and the template before writing a row; rule ids are BR-xx from `docs/part2/rules.md`. The route, controller method, guards and
PC/MG anchors are added automatically and each controller call is checked against the view code.
