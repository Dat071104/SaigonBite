// Artifact Tool authoring; run with the bundled Node runtime.
import fs from 'node:fs/promises';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const req = createRequire('D:/RAD/FINAL/Part2/build/p1_runtime/package.json');
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const base = 'D:/RAD/FINAL/Part2';
const source = process.argv[2] === 'verify'
  ? `${base}/workbook/Team02_RAD_Sem01_2627_Team_Workbook.xlsx`
  : 'D:/RAD/FINAL/Part1_v2/drive_upload/Team02_RAD_Sem01_2627_Team_Workbook.xlsx';
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(source));
await fs.mkdir(`${base}/notes/P1_workbook_preview`, { recursive: true });
function verifyQuestionLimit() {
  const qa = wb.worksheets.getItem('Client Q&A');
  const probe = qa.getRange('H10');
  const previous = probe.values;
  try {
    probe.values = [['Submitted']];
    wb.recalculate();
    if (Number(qa.getRange('C16').values[0][0]) !== 6 ||
        !String(qa.getRange('C18').values[0][0]).startsWith('Over the limit')) {
      throw new Error('The preserved Q&A formulas did not reject a sixth question');
    }
  } finally {
    probe.values = previous;
    wb.recalculate();
  }
  if (Number(qa.getRange('C16').values[0][0]) !== 5 || qa.getRange('C18').values[0][0] !== 'OK') {
    throw new Error('The original five-question state was not restored');
  }
  console.log('Q&A recalculation: 6 -> over limit; restored 5 -> OK. Probe was not exported.');
}
if (process.argv[2] === 'before') {
  console.log((await wb.inspect({ kind: 'region', sheetId: 'Client Q&A', range: 'B16:C18', maxChars: 1600 })).ndjson);
  const image = await wb.render({ sheetName: 'Assumption Log', range: 'A4:I8', scale: 1, format: 'png' });
  await fs.writeFile(`${base}/notes/P1_workbook_preview/before_assumptions.png`, new Uint8Array(await image.arrayBuffer()));
  for (const [sheetName, range, name] of [
    ['Client Q&A', 'A4:L9', 'qa'],
    ['Backlog & Risks', 'A4:H8', 'backlog'],
    ['Backlog & Risks', 'A27:H32', 'risks'],
    ['Requirements List', 'A4:H8', 'requirements'],
    ['Iteration Plan', 'A4:H10', 'iterations'],
    ['AI Usage Log', 'A4:H8', 'ai'],
  ]) {
    const preview = await wb.render({ sheetName, range, scale: 1, format: 'png' });
    await fs.writeFile(`${base}/notes/P1_workbook_preview/before_${name}.png`, new Uint8Array(await preview.arrayBuffer()));
  }
} else if (process.argv[2] === 'edit') {
  const updates = JSON.parse(await fs.readFile(`${base}/notes/P1_workbook_updates.json`, 'utf8'));
  for (const update of updates) {
    const cell = wb.worksheets.getItem(update.sheet).getRange(update.cell);
    if (update.formula) cell.formulas = [[update.formula]];
    else cell.values = [[update.value]];
    if (update.format_from) cell.setNumberFormat('dd/mm/yyyy');
  }
  const layout = JSON.parse(await fs.readFile(`${base}/notes/P1_workbook_layout.json`, 'utf8'));
  for (const [name, spec] of Object.entries(layout)) {
    const sheet = wb.worksheets.getItem(name);
    for (const [row, height] of Object.entries(spec.heights ?? {})) {
      sheet.getRange(`A${row}:L${row}`).format.rowHeight = height;
    }
    for (const [column, width] of Object.entries(spec.new_columns ?? {})) {
      const letter = String.fromCharCode(64 + Number(column));
      sheet.getRange(`${letter}4:${letter}100`).format.columnWidth = width;
    }
  }
  verifyQuestionLimit();
  wb.recalculate();
  console.log((await wb.inspect({ kind: 'region', sheetId: 'Client Q&A', range: 'B16:C18', maxChars: 1800 })).ndjson);
  const out = await SpreadsheetFile.exportXlsx(wb);
  await out.save(`${base}/notes/P1_workbook_artifact_roundtrip.xlsx`);
} else {
  wb.recalculate();
  console.log((await wb.inspect({ kind: 'region', sheetId: 'Client Q&A', range: 'B16:C18', maxChars: 1800 })).ndjson);
  console.log((await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!', options: { useRegex: true, maxResults: 12 }, maxChars: 1800 })).ndjson);
  const views = JSON.parse(await fs.readFile(`${base}/notes/P1_workbook_views.json`, 'utf8'));
  for (const view of views) {
    const image = await wb.render({ sheetName: view.sheet, range: view.range, scale: 1, format: 'png' });
    await fs.writeFile(`${base}/notes/P1_workbook_preview/${view.name}.png`, new Uint8Array(await image.arrayBuffer()));
  }
}
