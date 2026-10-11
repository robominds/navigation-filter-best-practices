# Navigation Filter Best Practices: Markdown Edition

This repository holds a verified Markdown transcription of **NASA/TP–2018–219822/Revision, *Navigation Filter Best Practices*, Second Edition** (J. Russell Carpenter and Christopher N. D'Souza, eds., NASA Engineering and Safety Center, January 29, 2025).

The document is now plain text you can search and diff, and it renders on GitHub. All 760 numbered equations are LaTeX, and every cross-reference, citation and index link works. The original PDF is included for reference.

| File | What it is |
|---|---|
| [`Navigation Filter Best Practices 2025.md`](Navigation%20Filter%20Best%20Practices%202025.md) | The Markdown edition |
| [`Navigation Filter Best Practices 2025.pdf`](Navigation%20Filter%20Best%20Practices%202025.pdf) | The source PDF (176 pages) |
| `_page_*.jpeg` | Figures and logos used by the Markdown |
| [`CONVERSION.md`](CONVERSION.md) | How the edition was made and verified, and every deliberate deviation from the PDF |
| [`conversion/`](conversion/) | The raw, uncorrected output from `marker-pdf`, kept for provenance |
| [`tools/`](tools/) | Validation scripts and the instructions given to the AI agents |

## Status of the text

The report states: *"This material is declared a work of the US Government and is not subject to copyright protection in the United States, but may be subject to US Government copyright in other countries."* This repository is an independent transcription. It is not affiliated with or endorsed by NASA. For anything safety- or mission-critical, cite and check the official NASA publication.

## How it was made (summary)

1. The PDF was converted with [`marker-pdf`](https://github.com/datalab-to/marker). The prose came through well, but an audit found that about 38% of the display equations had errors that changed their meaning. Typical errors were a priori/a posteriori superscripts turned into inverses or transposes, swapped accents, lost derivative dots and garbled matrices. Several tables had also been flattened.
2. Every page was re-transcribed against images of the PDF pages by AI agents (Claude, Anthropic), working on chapter-sized chunks in parallel. They fixed the equations, inline math, tables, algorithm boxes, footnotes and headings, and kept the prose verbatim.
3. The result passed automated checks:
   - every PDF equation number appears exactly once;
   - KaTeX renders all 2,538 math expressions without error;
   - all 578 internal links resolve;
   - no prose from the original conversion was lost.
4. As a clean recheck, ten fresh agents audited all 176 pages against high-resolution renders. They did not see the earlier findings. They found **no errors that change meaning** in about 800 display equations and about 1,750 inline expressions. They found a few cosmetic issues, which were fixed.

Details, including the list of deliberate corrections, are in [CONVERSION.md](CONVERSION.md).

## Corrections relative to the PDF

Typos that are in the PDF itself are reproduced as printed, with these exceptions:

- **Eq. (C.56):** the second component of $\mathbf{u}_\delta$ is corrected from $-\cos\alpha\cos\delta$ to $-\sin\alpha\sin\delta$, with an erratum note in the text. This value is the derivative of the line-of-sight vector (C.46), it is a unit vector, and it matches the identical eq. (C.74).
- **Spelling:** "eignevectors", "peripasis", "liklihood" and "partitoned" are corrected.

## Rendering notes

- Equations use `$…$` and `$$…\tag{n.m}$$`. They render on GitHub, in VS Code, in Obsidian, and through Pandoc with MathJax or KaTeX.
- Random variables are written in bold sans-serif (`\boldsymbol{\mathsf{x}}`), as in the PDF. KaTeX-based viewers show them as sans-serif but not bold; MathJax shows them bold.
- The file is about 0.5 MB. If GitHub's web view won't render it, open the raw file or view it locally.

## Re-running the checks

```sh
python3 tools/verify.py --original "conversion/Navigation Filter Best Practices 2025.marker-original.md"
(cd tools && npm install) && node tools/katex-check.js "Navigation Filter Best Practices 2025.md"
```

`verify.py` needs `pdftotext` (poppler), and `katex-check.js` needs Node.js.

## Credits

- **Original report:** J. Russell Carpenter and Christopher N. D'Souza, editors, with contributions from Shyam Bhaskaran, Cheryl J. Gramling, F. Landis Markley, James McCabe, Timothy McElrath, Lincoln Wood and Renato Zanetti. NASA Engineering and Safety Center.
- **Markdown edition:** prepared by Mark Castelluccio.
- **AI assistance:** the initial conversion used `marker-pdf`. The equation re-transcription, structural repair and verification were done with Claude (Anthropic), working as AI agents under the editor's direction.
