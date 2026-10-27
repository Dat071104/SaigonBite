# Figma prototype and source kit

## Built on 27/10/2026

The [Edu file](https://www.figma.com/design/R8sYygIpfqzI6Nm2Gx2hDh) has four pages: Sketch, Wireframe, Mockup and Prototype. Codex (AI-assisted) drew 35 low-fidelity sketches from the briefs in Figma, and assembled and linked the file in Dat’s account using the Desktop plugin. Wireframes and mockups were authored as HTML/CSS (AI-assisted) and exported to PNG; they were not drawn natively in Figma. The Prototype page contains 47 mockup image frames, 148 hotspots, 129 navigation reactions and six flow starts. The 19 same-frame hotspots have no reaction; the corresponding app controls reload the same screen. Dat set Anyone with the link to can view. The [prototype](https://www.figma.com/proto/R8sYygIpfqzI6Nm2Gx2hDh/SaigonBite-Part-2-UI?node-id=4-3&starting-point-node-id=4%3A3&page-id=4%3A2&scaling=min-zoom&content-scaling=fixed) passed six logged-out flow checks (one transition each). See `Part2/evidence/figma/check.md`.

## Original manual recipe (historical; superseded by the build above)

# Build the Figma prototype (owner step, about 45 minutes)

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). The frames in this folder are **HTML/CSS wireframes and mockups authored with AI assistance and exported to PNG**.
In Figma you only import, assemble and link them; do not describe them as drawn natively in Figma. Dates of each artifact: `UC-0x/trace.md`.

1. In Figma create a file `SaigonBite Part 2 UI`, with four pages: **Sketch**, **Wireframe**, **Mockup**, **Prototype**.
2. Sketch: draw (paper or freehand) the screens listed in each `UC-0x/sketch_brief.md` and put the photos on this page. Nothing is generated for you.
3. Wireframe and Mockup: drag the PNG files of `2_Wireframe` and `3_Mockup` onto the page (File > Place image). Keep the file names: they are the frame names. Phone frames are 390 wide, staff frames 1440 wide; keep 1x.
4. Prototype: drag the files of `4_Prototype` (the mockup frames) onto the page, one row per use case.
5. For every row of `flows.csv` (UC, from frame, x, y, w, h in frame pixels, to frame, trigger): in the Prototype page add a rectangle at (x, y) with size (w, h) inside the *from frame*, no fill, then in Prototype mode drag its handle to the *to frame* (On click, Navigate to, instant). There are 148 hotspots.
6. Start frame of each use case (Prototype settings > Flow starting point):
   - UC-01: `UC01-S01 Choose a kitchen hub`
   - UC-05: `UC05-S01 Kitchen board`
   - UC-02: `UC02-S01 Deliveries - ready for pickup`
   - UC-03: `UC03-S01 Hubs and kitchen capacity`
   - UC-06: `UC06-S01 Brands and dishes`
   - UC-04: `UC04-S01 Sales report`
7. Share: Share > General access **Anyone with the link** > **Can view**; copy the link of the Prototype (Share prototype).
8. Paste the link into `Part2/content/links.json` under `figma_prototype` (replace `PENDING`), then tell Claude to run the logged-out check: it opens the link in a fresh private context, confirms each start frame, and saves dated screenshots to `Part2/evidence/figma/`.

Until step 8 is done, the report says `PENDING (owner)` for the prototype link.
