const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  Footer, PageNumber, PageBreak,
} = require("docx");

const BODY = "Georgia";
const dir = __dirname;
const SKIP_PROV = !!process.env.SKIP_PROVENANCE;
const md = (SKIP_PROV ? "" : fs.readFileSync(path.join(dir, "provenance.md"), "utf8") + "\n\n") +
  fs.readFileSync(path.join(dir, "full.md"), "utf8");

// ---- inline markdown -> TextRuns ----
function runs(text, base = {}) {
  const out = [];
  // tokenize **bold** then *italic*
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*\n]+\*)/g).filter(Boolean);
  for (const p of parts) {
    if (/^\*\*[^*]+\*\*$/.test(p)) out.push(new TextRun({ text: p.slice(2, -2), bold: true, font: BODY, size: 22, ...base }));
    else if (/^\*[^*\n]+\*$/.test(p)) out.push(new TextRun({ text: p.slice(1, -1), italics: true, font: BODY, size: 22, ...base }));
    else out.push(new TextRun({ text: p, font: BODY, size: 22, ...base }));
  }
  return out;
}

const children = [];

// ---- title page ----
children.push(
  new Paragraph({ spacing: { before: 3600 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Answerable Teaching", font: BODY, size: 64, bold: true })] }),
  new Paragraph({ spacing: { before: 300 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Agency, Perception, and the Ethics of Teaching", font: BODY, size: 32, italics: true })] }),
  new Paragraph({ spacing: { before: 900 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Katherine von Duyke, Ph.D.", font: BODY, size: 28 })] }),
  new Paragraph({ spacing: { before: 2400 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Working compilation · Preface and Chapters 1–5 · August 2026", font: BODY, size: 20, color: "666666" })] }),
  new Paragraph({ children: [new PageBreak()] }),
);

// ---- parse blocks ----
const lines = md.split("\n");
let i = 0, firstH1 = true;
while (i < lines.length) {
  const line = lines[i];

  if (/^\s*$/.test(line)) { i++; continue; }
  if (/^---\s*$/.test(line)) { i++; continue; }

  if (line.startsWith("# ")) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_1,
      pageBreakBefore: !firstH1,
      spacing: { before: firstH1 ? 0 : 240, after: 360 },
      children: [new TextRun({ text: line.slice(2), font: BODY, size: 40, bold: true, color: "000000" })],
    }));
    firstH1 = false; i++; continue;
  }
  if (line.startsWith("## ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 360, after: 200 },
      children: [new TextRun({ text: line.slice(3), font: BODY, size: 28, bold: true, color: "000000" })] }));
    i++; continue;
  }
  if (line.startsWith("### ")) {
    children.push(new Paragraph({ spacing: { before: 280, after: 160 },
      children: [new TextRun({ text: line.slice(4), font: BODY, size: 24, bold: true, italics: true })] }));
    i++; continue;
  }
  if (line.startsWith("#### ")) {
    children.push(new Paragraph({ spacing: { before: 240, after: 140 },
      children: [new TextRun({ text: line.slice(5), font: BODY, size: 22, bold: true })] }));
    i++; continue;
  }
  if (line.startsWith("> ")) {
    // callout box: consecutive "> " lines rendered as a shaded, left-ruled block
    const boxLines = [];
    while (i < lines.length && lines[i].startsWith("> ")) { boxLines.push(lines[i].slice(2)); i++; }
    boxLines.forEach((bl, bi) => {
      children.push(new Paragraph({
        indent: { left: 480, right: 480 },
        spacing: { before: bi === 0 ? 200 : 40, after: bi === boxLines.length - 1 ? 240 : 40 },
        shading: { type: ShadingType.CLEAR, fill: "F2F2F2" },
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: "8A8A8A", space: 8 } },
        children: runs(bl),
      }));
    });
    continue;
  }

  // table block
  if (line.trim().startsWith("|")) {
    const tblLines = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) { tblLines.push(lines[i]); i++; }
    const rows = tblLines
      .filter(l => !/^\|[\s\-|]+\|$/.test(l.trim()))
      .map(l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim()));
    const ncols = rows[0].length;
    const total = 9360;
    const widths = ncols === 5 ? [1250, 1800, 2450, 1850, 2010]
      : ncols === 3 ? [2000, 2800, 4560]
      : Array(ncols).fill(Math.floor(total / ncols));
    const tableRows = rows.map((cells, ri) => new TableRow({
      children: cells.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: "EFEFEF" } : undefined,
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: runs(c).map(r => { if (ri === 0) r = new TextRun({ text: c, bold: true, font: BODY, size: 20 }); return r; }) })],
      })),
    }));
    // header row bold handled above crudely; rebuild header cleanly:
    tableRows[0] = new TableRow({
      children: rows[0].map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: "EFEFEF" },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: c, bold: true, font: BODY, size: 20 })] })],
      })),
    });
    // body cells at size 20
    for (let r = 1; r < tableRows.length; r++) {
      tableRows[r] = new TableRow({
        children: rows[r].map((c, ci) => new TableCell({
          width: { size: widths[ci], type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: runs(c).map(x => x).map(x => x) .map(x=>x) })],
        })),
      });
    }
    children.push(new Table({ columnWidths: widths, rows: tableRows, width: { size: total, type: WidthType.DXA } }));
    children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
    continue;
  }

  // regular paragraph (may wrap multiple physical lines until blank)
  const buf = [line];
  i++;
  while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#|\||>|---)/.test(lines[i].trim())) { buf.push(lines[i]); i++; }
  children.push(new Paragraph({
    spacing: { after: 200, line: 300 },
    children: runs(buf.join(" ")),
  }));
}

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: BODY, size: 18, color: "888888" })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = path.join(dir, SKIP_PROV ? "Answerable-Teaching-TEACHER-EDITION.docx" : "Answerable-Teaching-Preface-Ch3.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out, buf.length, "bytes");
});
