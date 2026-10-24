// Phase 2 narrow Artifact Tool authoring; the OOXML guard publishes the result.
import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const req = createRequire('D:/RAD/FINAL/Part2/build/p2_runtime/package.json');
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const base = 'D:/RAD/FINAL/Part2';
const name = 'Team02_RAD_Sem01_2627_Team_Workbook.xlsx';
const verify = process.argv[2] === 'verify';
const source = verify ? `${base}/workbook/${name}` : `${base}/notes/P2-root/workbook_before.xlsx`;
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(source));
await fs.mkdir(`${base}/notes/P2-root/workbook_preview`, { recursive: true });
// Import can omit followers of OOXML shared-formula groups. Restore the exact
// original expanded formula texts from a read-only audit before recalculation.
const originalFormulas = JSON.parse(await fs.readFile(`${base}/notes/P2_workbook_formulas.json`, 'utf8'));
for (const f of originalFormulas) wb.worksheets.getItem(f.sheet).getRange(f.cell).formulas = [[f.formula]];
const originalWrapping = JSON.parse(await fs.readFile(`${base}/notes/P2_workbook_wrap.json`, 'utf8'));
for (const f of originalWrapping) wb.worksheets.getItem(f.sheet).getRange(f.cell).format.wrapText = true;
if (!verify) {
  const updates = JSON.parse(await fs.readFile(`${base}/notes/P2_workbook_updates.json`, 'utf8'));
  for (const u of updates) {
    const cell = wb.worksheets.getItem(u.sheet).getRange(u.cell);
    cell.values = [[u.value]];
    cell.format.wrapText = true; // Restore original template wrapping lost on import.
  }
  const layout = JSON.parse(await fs.readFile(`${base}/notes/P2_workbook_layout.json`, 'utf8'));
  for (const [sheet, rows] of Object.entries(layout)) {
    for (const [row, height] of Object.entries(rows)) wb.worksheets.getItem(sheet).getRange(`A${row}:I${row}`).format.rowHeight = height;
  }
}
if (verify) {
  const updates = JSON.parse(await fs.readFile(`${base}/notes/P2_workbook_updates.json`, 'utf8'));
  for (const u of updates) wb.worksheets.getItem(u.sheet).getRange(u.cell).format.wrapText = true;
}
// Exercise a genuine dependency: a blank operation must produce Gap, then restore.
const crud = wb.worksheets.getItem('CRUD Check');
const previous = crud.getRange('C5').values;
crud.getRange('C5').values = [[null]];
wb.recalculate();
if (crud.getRange('G5').values[0][0] !== 'Gap') throw new Error('Blank C5 did not produce Gap');
crud.getRange('C5').values = previous;
wb.recalculate();
for (let row = 5; row <= 17; row++) if (crud.getRange(`G${row}`).values[0][0] !== 'OK') {
  console.log(JSON.stringify({row,values:crud.getRange(`A${row}:G${row}`).values,formulas:crud.getRange(`A${row}:G${row}`).formulas}));
  throw new Error(`CRUD gap at ${row}`);
}
if (Number(wb.worksheets.getItem('Client Q&A').getRange('C16').values[0][0]) !== 5) throw new Error('Client question count changed');
console.log('CRUD formula probe Gap → OK restored; 13 union rows OK; Q1–Q5 count unchanged.');
console.log((await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 20 }, maxChars: 1500 })).ndjson);
for (const [sheetName, range, file] of [
  ['Events Table','A4:I10','events_1'],['Events Table','A11:I17','events_2'],['Events Table','A18:I24','events_3'],
  ['CRUD Check','A4:H10','crud_1'],['CRUD Check','A11:H17','crud_2'],
  ['Team & Use Cases','A8:H11','team_members'],['Team & Use Cases','A14:H22','team_ucs']
]) {
  const image = await wb.render({ sheetName, range, scale: 1, format: 'png' });
  await fs.writeFile(`${base}/notes/P2-root/workbook_preview/${verify?'final':'candidate'}_${file}.png`, new Uint8Array(await image.arrayBuffer()));
}
if (!verify) {
  const output = await SpreadsheetFile.exportXlsx(wb);
  await output.save(`${base}/notes/P2-root/workbook_artifact_roundtrip.xlsx`);
}
