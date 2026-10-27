# UC-06 Manage brands and menu items: sketch brief (drawn in Figma by Codex (AI-assisted) on 27/10/2026)

Brief authored by 722I0004 with Claude Sonnet 5.5 assistance. Low-fidelity sketches were drawn from this brief in Figma by Codex (AI-assisted) on 27/10/2026; exports and attribution are in `sketch/README.md`.

Device: a desktop browser (1440 × 900 landscape). Catalogue and hub menu screens use the wide table width, the dish forms the narrow one. Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-06-S01 Brands and dishes | title and help line; "Brands" table with a Rename field and button and an Archive link per row; one line "New brand name" + "Add brand"; "Dishes" with "New dish" button and table Dish (with grey description), Brand, Price, Edit and Archive; "Menus per hub" links | OP-25 listCatalogue |
| 2 | UC-06-S02 Brand created and renamed | green box "The brand is renamed." on top of the same page | OP-37 createBrand, OP-38 updateBrand |
| 3 | UC-06-S03 / S04 New dish and Edit a dish | panel with Brand choice (new only), Dish name, Description, Price (VND); "Save dish" and "Back"; edit shows brand and "a new price applies to new orders only" under the title | OP-40 createMenuItem, OP-41 updateMenuItem |
| 4 | UC-06-S05 Dish form refused | red box "The price must be between 1 and 1,000,000 VND." above the panel, typed values kept | OP-40 / OP-41 (refusal) |
| 5 | UC-06-S06 Menu of a hub | title "Menu of <hub>"; table Dish, Brand, Price, Status badge, "Sold out" and "Remove from menu"; below it one line: dish choice, Initial availability, "Add to menu" | OP-25, OP-43 listItemAtHub, OP-44 setListingAvailability, OP-45 unlistItemAtHub |
| 6 | UC-06-S08 Archived brand and dish | green box "The brand is archived..."; muted rows with Archived badge and no buttons | OP-39 archiveBrand, OP-42 archiveMenuItem (BR-19) |

Keep: labels in words (no icons), one main button per screen, the refusal message in a box above the form or table.
