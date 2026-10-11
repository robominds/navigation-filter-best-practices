# Conversion and Verification Record

This file records how the Markdown edition of *Navigation Filter Best Practices* (NASA/TP–2018–219822/Revision, 2nd ed., 2025) was produced from the PDF, how it was checked, and every place it deliberately differs from the PDF.

## 1. Source

- `Navigation Filter Best Practices 2025.pdf`: 176 pages, US Letter, typeset with LaTeX. It is math-heavy, with 760 numbered equations.

## 2. Initial conversion (marker-pdf)

The PDF was converted with `marker-pdf` 2.0.0, without its AI-assisted mode. The metadata records 0 AI requests. The raw output is kept unchanged in [`conversion/`](conversion/):

- `…marker-original.md`: the converted Markdown
- `…_meta.json`: marker's page metadata

### Audit of the raw conversion

Four agents compared about 50 equation-dense pages against rendered page images, covering Chapter 1 through Appendix C.

**What came through well:**
- The prose: word counts matched the PDF to within 0.3%.
- The 8 figures, the 5 algorithm boxes, and the internal links.

**What was wrong in the display equations:**

| Range | Display equations with an error that changes meaning |
|---|---|
| Ch. 1–3 | ~36%. 15 of the 21 lines in Algorithms 1.1–1.3 were wrong |
| Ch. 4–7 | ~38% |
| Ch. 8–9 | ~48%. ~68% in the Ch. 8 UDU derivations |
| Ch. 10–App. C | ~36% |

The errors fell into a few systematic patterns:
- a priori/a posteriori superscripts ($\mathbf{P}^-$, $\mathbf{P}^+$) rendered as $^{-1}$, $^{\mathsf T}$, $^\dagger$ or $^*$;
- transposes turned into inverses;
- tilde and breve accents swapped;
- hats turned into dots, and time-derivative dots lost;
- wrong subscripts;
- matrices of the wrong size;
- roots and fractions with the wrong extent;
- equations duplicated in two different versions;
- truncated equation labels, such as `(B.6)` for B.68.

**Structural problems:**
- The Notational Conventions table and Lear's table were flattened.
- The bibliography was run together into one paragraph.
- Heading levels were inconsistent.
- Footnotes split sentences.
- About 144 equations were laid out as Markdown tables.
- 14 image links pointed to images that did not exist (blank pages).
- Inline math was mostly unicode with `<sup>` tags.

## 3. Correction

The Markdown was split into 13 chunks at chapter boundaries. Each chunk went to an AI agent (Claude, Anthropic) together with renders of the PDF pages at 110–400 dpi. The full instructions are in [`tools/prompts/fix-chunk-instructions.md`](tools/prompts/fix-chunk-instructions.md). In summary, each agent was told to:

- re-transcribe every display equation from the page image into LaTeX that KaTeX and MathJax can render, with one `$$ … \tag{n.m} $$` block per equation number and duplicates removed;
- convert all inline math to `$…$` LaTeX;
- keep the prose verbatim, fixing only conversion damage;
- keep every `<span id="page-…">` anchor, because the internal links point to them;
- apply a consistent heading scheme, and format algorithm boxes and summary frames as blockquotes;
- rebuild the tables, the bibliography (one entry per line) and the index;
- delete the dead image links.

Two consistency decisions were confirmed on 400-dpi crops and applied throughout:

- The second accent in the UDU derivations is a **breve** (`\breve`), not a check.
- Transposes are written with a sans-serif T (`^{\mathsf{T}}`), as in the PDF.

The chunks were then stitched back together. A final pass normalized the random-variable notation to `\boldsymbol{\mathsf{·}}`.

## 4. Verification

### Automated checks ([`tools/`](tools/))

- `verify.py`:
  - all 760 equation numbers printed in the PDF appear exactly once as `\tag{}`;
  - all 578 internal links resolve, with no duplicate anchors;
  - all referenced images exist;
  - `$$` delimiters are balanced;
  - compared with the original conversion, no prose was lost. The only flagged runs come from restructured tables and the Contents.
- `katex-check.js`: all 2,538 math expressions parse in KaTeX 0.16.11.
- A word-level comparison with `pdftotext` output for every page found no missing text. Apparent gaps are explained by math, hyphenation at line breaks, or restructured tables.

### First independent re-audit

Two new agents re-checked 26 of the worst pages from the original audit (255 equations). They found **0 errors that change meaning**. They found 5 font-only slips (serif vs sans-serif bold), which were fixed.

### Clean full recheck

Ten new agents, with no knowledge of earlier findings, audited all 176 pages against renders at 200–500 dpi. The instructions are in [`tools/prompts/recheck-instructions.md`](tools/prompts/recheck-instructions.md).

| Item | Checked | Errors that change meaning |
|---|---|---|
| Display equations | ~800 (all 760 numbered plus unnumbered) | 0 |
| Inline math | ~1,750 spans | 0 |
| Prose | every page, by word diff and by eye | 0 |
| Structure (headings, algorithm boxes, tables, figures, footnotes, 92 references, index) | all | 0 |

The cosmetic findings were fixed:
- bibliography titles were missing their italics;
- three headings had no blank line before them;
- "crosscovariance" became "cross-covariance", and "statespace" became "state-space";
- one heading level was adjusted;
- a stray space in eq. 10.12 was removed;
- a misplaced apostrophe in a link was moved.

## 5. Deliberate deviations from the PDF

### Content corrections

- **Eq. (C.56):** the second component of $\mathbf{u}_\delta$ is printed in the PDF as $-\cos\alpha\cos\delta$. Here it is $-\sin\alpha\sin\delta$, and an *Erratum* note follows the equation. The reasons:
  - It equals $\partial/\partial\delta$ of the line-of-sight vector $[\cos\alpha\cos\delta,\ \sin\alpha\cos\delta,\ \sin\delta]^{\mathsf T}$ in (C.46).
  - It is a unit vector, whereas the printed version is not.
  - It is identical to (C.74), which the PDF prints correctly.
- **Spelling:**
  - eignevectors → eigenvectors (Ch. 8)
  - peripasis → periapsis (Ch. 3)
  - liklihood → likelihood (Ch. 1)
  - partitoned → partitioned (App. B)

### PDF typos kept as printed

Other errors in the source are reproduced exactly. They include:
- doubled words, such as "as as", "is is" and "using using";
- the stray `]` in (1.15);
- the missing superscript on the first $\mathbf{P}_i$ in (5.10);
- $w_d^2$ for $\omega_d^2$ in (6.40)–(6.41);
- the repeated $\mathbf{P}^-_{B_i}$ in (11.5);
- the empty equation number (12.13);
- "**a**r" (a broken `\bar` macro) in (B.65)–(B.66);
- the mismatched bracket in (B.29);
- $x_{t_{nom}}$ in (C.4).

### Formatting choices

- Equations are `$$` blocks with `\tag{}`. Groups that the PDF typesets as one aligned block with several numbers are split into separately tagged blocks.
- Run-in subsection titles in the PDF (bold text that starts a paragraph) are Markdown headings.
- Algorithm boxes and boxed summaries are blockquotes.
- Footnotes are placed immediately after the paragraph they belong to.
- The Contents and Notational Conventions are pipe tables.
- The duplicate title page is merged into one. Blank pages and running headers and footers are omitted.
- The Cholesky root, ᶜ√, is written `{}^{c}\!\sqrt{\cdot}`, and dashed partition lines are written `\hline` or `\hdashline`.
- Straight quotes are used where the PDF uses curly quotes in a few places, and the index has no gaps between letter groups.

## 6. Tools and people

- `marker-pdf` 2.0.0, poppler (`pdftoppm`, `pdftotext`), pdfplumber, KaTeX 0.16.11.
- Claude (Anthropic), working as coordinated AI agents for the audit, the correction and the verification.
- Mark Castelluccio directed the work, decided on the corrections, and prepared the edition.
