# Writes Part2/deliverables/Readme.txt from Part2/content/links.json (the single source of links).
from pathlib import Path
import json
B = Path(r'D:\RAD\FINAL'); L = json.loads((B / 'Part2/content/links.json').read_text(encoding='utf-8'))
tag = L['github_release_tag']
release = f"{L['github_repo']}/releases/tag/{tag}"
video = L['demo_video'] if not L['demo_video'].startswith('PENDING') else 'No separate video for Part 2; the demonstration steps are in report section 5.3 (the Part 3 video follows with Part 3).'
members = '\n'.join(f"  {m['id']}  {m['name']}" for m in L['members'])
text = f"""SaigonBite - Online Food Delivery Hub Platform
RAD Sem01_2627 - Team {L['team_no']} - Part 2 (BRS and SRS)

Members
{members}

Links
  GitHub repository : {L['github_repo']}
  Tagged release    : {release}   (tag {tag}; GitHub release of the same name)
  Figma prototype   : {L['figma_prototype']}
  Figma design file : {L['figma_file']}
  Deployed system   : {L['deployed_url']}   (fallback {L['deployed_url_fallback']})
  Drive folder      : {L['drive_folder']}
  Demonstration     : {video}

Demo accounts (demo data only; password for all: 123456)
  customer, kitchen (District 1 hub), kitchen_bt (Binh Thanh hub), shipper, admin, manager

Run locally (Docker Desktop)
  git clone {L['github_repo']}.git
  cd SaigonBite
  git checkout {tag}
  docker compose up --build -d
  then open http://127.0.0.1:5000

Run the tests (Python 3.13, full Git checkout)
  pip install -r requirements.txt
  python -m pytest -q          (928 tests)

Files submitted
  Team{L['team_no']}_BRS_SRS_for_SaigonBite.pdf   report (sections I-V, appendices incl. Contribution Statement and AI Usage Log)
  Team{L['team_no']}_Self_Assessment_SaigonBite.xlsx   self-assessment (course marking sheet: Part 1 and Part 2 self-marks, checklist)
  Team{L['team_no']}_RAD_Sem01_2627_Team_Workbook.xlsx   team workbook (Q&A, assumptions, backlog, requirements, events, CRUD, test cases, feedback)
  Readme.txt                                   this file
  Model sources (draw.io, Graphviz .dot, PNG, SVG) are in the repository folder models/ and in the Drive folder.
"""
out = B / 'Part2/deliverables/Readme.txt'
out.write_text(text, encoding='utf-8'); print(text)
