# Clean recheck: PDF vs Markdown (READ-ONLY)

You are independently auditing a Markdown edition of the NASA report "Navigation Filter Best Practices" (2nd ed.) against its PDF. Do NOT modify any file except inside your own output folder.

- PDF: `<repo>/Navigation Filter Best Practices 2025.pdf`
- Markdown: `<repo>/Navigation Filter Best Practices 2025.md`
- SCRATCH = `<scratch directory>`
- Page images at 110 dpi: `SCRATCH/render/p-NNN.png` (1-based PDF page, 3 digits). For accents, fonts or small sub/superscripts, render a sharper copy into your own folder `SCRATCH/recheck/<id>/` with `pdftoppm -r 250 -png -f N -l N "<pdf>" <out>`.
- PDF text: `pdftotext -layout -f N -l N "<pdf>" -`
- Finding the Markdown for a page: equation tags `\tag{n.m}` or anchors `<span id="page-K-…">`, where K = PDF page − 1.

## Check EVERY page in your range, completely
1. **Every display equation**, symbol by symbol. Check:
   - ± superscripts (a priori/a posteriori)
   - transpose vs inverse
   - accents: tilde, breve, check, hat, bar, dot, double dot
   - subscripts and superscripts
   - signs
   - matrix shape and the position of each entry
   - extent of roots and fractions
   - brackets
   - font: bold, sans-serif random variables, calligraphic, blackboard
   - the equation number
2. **Inline math** in the prose: the same checks.
3. **Prose**: compare it with the PDF and look for missing, extra, reordered or altered sentences and words. A quick way is to diff the normalized words of `pdftotext` against the Markdown for the page. Footnotes are deliberately placed after their paragraph.
4. **Structure**: headings, and their numbering and levels; algorithm boxes, with every line present; tables, with every cell; figures, with image and caption; footnotes; list items; and bibliography or index entries, if they fall in your range.

## Known, intentional deviations: do NOT report these
- Markdown conventions:
  - equations are `$$…\tag{}$$` blocks;
  - run-in subsection titles are made into `###` headings;
  - algorithm and summary boxes are blockquotes;
  - footnotes come after the paragraph they belong to;
  - the Contents is a table;
  - the duplicate title page is merged;
  - blank pages and running headers or footers are omitted;
  - there is an authorship note at the end.
- Typos that are in the PDF itself are reproduced as printed. The exceptions are the deliberate corrections "eigenvectors", "periapsis", "likelihood" and "partitioned", and C.56 (corrected, with an erratum note).
- Style equivalents: `\widetilde`/`\tilde`; `^{\mathsf{T}}`/`^T`/`^\top`; `{}^{c}\!\sqrt{}` for the Cholesky root; `\hline` for dashed partition lines.
- `\boldsymbol{\mathsf{x}}` is the intended notation for sans-serif random variables. KaTeX may not show it bold; that is expected.

## Report (under 450 words)
- Pages checked, and the counts of display equations, inline-math spans and prose paragraphs checked.
- **Each discrepancy**: Markdown line number, PDF page, what the PDF shows, what the Markdown has, and its class: MEANING (changes the math or the text), FONT, STRUCTURE, or COSMETIC. Give exact replacement text where you can.
- If you find nothing, say so explicitly.
