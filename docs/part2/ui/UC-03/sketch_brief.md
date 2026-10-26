# UC-03 Manage hubs and capacity: sketch brief (for Dat to draw)

Author: 722I0004 · AI-assisted (Claude Sonnet 5.5). This is the brief only. The sketch itself is the owner's own paper or Figma-freehand drawing;
no image imitating a hand-drawn sketch is generated. Put the photos in `sketch/` and write the real date you drew them in the file name
or in `sketch/README.md`. Until then `trace.md` says `OWNER-PENDING`.

Device: a desktop browser (1440 × 900 landscape). Admin screens use the 720 px form width or the wide 1120 px table width, centred. Draw one rectangle per screen, about 10 minutes for all of them.

| Sketch | Screen it becomes | Draw these controls | SSD operation it serves |
|---|---|---|---|
| 1 | UC-03-S01 Hubs and kitchen capacity | wordmark, role name and Log out on top; 5 admin links (Hubs underlined); title and one grey help line; green "New hub" button; table Code, Hub, Load / capacity, Now (Quiet badge), Base fee, Open orders, then "Edit" and "Menu" links | OP-23 listHubs |
| 2 | UC-03-S02 Edit a hub | hub name as title and "Load now 1 of 12 · 2 open order(s)"; panel with Hub code, Name, Address, Latitude and Longitude side by side, Kitchen capacity (hint "1 to 500") and Base delivery fee side by side; "Save hub" and "Back"; the line "can be archived once its open orders are finished" under the panel | OP-24 getHub, OP-35 updateHub |
| 3 | UC-03-S04 New hub | the same panel, all fields empty, title "New hub" | OP-34 createHub |
| 4 | UC-03-S05 Hub form refused | red box "The kitchen capacity must be between 1 and 500." above the panel; fields keep what was typed | OP-34 / OP-35 (refusal, BR-18) |
| 5 | UC-03-S03 Hub saved | green box "The hub is saved." above the hub table | OP-35 |
| 6 | UC-03-S06 Hub archived | green box "The hub is archived..."; a muted row with Archived badge and "archived <time>" instead of links | OP-36 archiveHub (BR-18) |

Keep: labels in words (no icons), one main button per screen, the refusal message in a box above the form or table.
