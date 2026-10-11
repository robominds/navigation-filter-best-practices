# Fixing one chunk of a PDF→Markdown conversion

The NASA report "Navigation Filter Best Practices" (2nd ed., 176-page LaTeX PDF) was converted to Markdown with `marker`. The prose came through well. About 40% of the display equations, most of the inline math and several structures are wrong. Your job is to produce a corrected version of ONE chunk of the Markdown, using the PDF page images as ground truth.

## Inputs
- SCRATCH = <scratch directory>
- Your chunk: `SCRATCH/chunks/<id>.md`
- Page images: `SCRATCH/render/p-NNN.png` (1-based PDF page, zero-padded to 3 digits, 110 dpi). Look at them with the Read tool. If something is too small to read, re-render that page at higher resolution with `pdftoppm -r 200 -png -f N -l N "<pdf>" SCRATCH/render/hi-<id>-N`.
- Plain text of the PDF (useful for prose): `pdftotext -f N -l N "<repo>/Navigation Filter Best Practices 2025.pdf" -`
- Anchors like `<span id="page-48-1">` use the 0-indexed page number (page-48 = PDF page 49).

## Output
Write the complete corrected chunk to `SCRATCH/fixed/<id>.md`. Do NOT modify anything in the project directory or in `SCRATCH/chunks/`. Your chunk is concatenated with the other chunks in order, so begin and end at the same content boundaries as the input.

## What to do
Go through every page in your range, comparing the image with the Markdown. Do all of the following:

1. **Display equations.** Re-transcribe every display equation from the image into correct LaTeX that KaTeX and MathJax can render. Check it symbol by symbol, paying particular attention to:
   - the ± superscripts on P, x̂, U, D (a priori `^-` and a posteriori `^+`). These were frequently corrupted into `^{-1}`, `^T`, `^\dagger` or `^*`.
   - transposes vs inverses.
   - accents: tilde `\tilde`/`\widetilde`, check `\check`, hat `\hat`, bar `\bar`, dot `\dot`/`\ddot`. A dot means a time derivative and must be correct.
   - subscripts and indices (i vs j vs 1, nn vs mn).
   - matrix dimensions and entry positions.
   - extent of square roots and fractions.
   - signs.
   - the font of each symbol: bold `\mathbf{}` (or `\boldsymbol{}` for Greek), sans-serif `\mathsf{}` (random variables), blackboard `\mathbb{}`, calligraphic `\mathcal{}`, and Fraktur where used. Match the PDF.
   - Cholesky-type roots written like ᶜ√: use `{}^{c}\!\sqrt{\cdot}` or a similar notation, not `\sqrt[n]`.
2. **Equation format.** Use one `$$ … $$` block per equation number, on its own lines, separated by blank lines, with the number given as `\tag{3.15}`. Delete any `(3.15)` or `(\text{3.15})` left in the body. For multi-line equations, use `\begin{aligned} … \end{aligned}` inside the block. Where several numbered lines are typeset as one aligned group (e.g. B.1/B.2), split them into separate tagged blocks, starting a continuation with `= …` where needed. Unnumbered display equations get no tag. Convert the marker tables of the form `| equation | (n.m) |` into `$$` blocks. **Remove duplicated equations**: marker often emitted the same equation twice, in two different versions. Keep one correct copy. Every equation number on your pages must appear exactly once as a `\tag{}`.
3. **Inline math.** Replace broken unicode/HTML math such as `σ<sup>x</sup>`, `<sup>U</sup>e`, `P − <sup>i</sup>`, `xˆ`, `R n` or `p 1 − ζ 2` with proper `$…$` LaTeX. Inline math already in `$…$` should be verified and fixed where needed. Do not leave `<sup>`/`<sub>` tags used for math, but footnote markers like `<sup>1</sup>` are fine.
4. **Prose.** Keep it verbatim. Fix only conversion damage: dropped or merged words, a sentence cut in two by a footnote, missing sentences. Do NOT correct typos that are genuinely in the PDF (e.g. "eignevectors", "partitoned"). Drop running page headers, footers and page numbers if any slipped in.
5. **Footnotes.** When a footnote interrupts a sentence, rejoin the sentence and put the footnote paragraph immediately after the paragraph it belongs to, formatted as `<sup>1</sup> footnote text`. Keep its anchor span.
6. **Anchors and links.** Keep EVERY `<span id="page-…"></span>` anchor, because 574 internal links point to them. Place an anchor at the start of the paragraph it belongs to, or on its own line directly above a `$$` block. Never put one inside math. Keep cross-reference links such as `[\(3.15\)](#page-40-2)` unchanged.
7. **Headings.** Use one consistent scheme:
   - Front-matter sections, chapters and appendices: `# Title`. Chapters are `# Chapter 3. The Covariance Matrix` and appendices `# Appendix B. The Mathematics Behind the UDU Factorization`. Leave any `<span id>` anchor in the heading where it already is.
   - Numbered sections: `## 3.1. Metrics for Orbit State Covariances`.
   - Run-in numbered subsections in the PDF (bold "3.1.1. Variance of … " followed by text on the same line): `### 3.1.1. Variance of an Arbitrary Function of Two Random Variables`, with the following text as its own paragraph.
   - Deeper levels: `####`.
   - Unnumbered section titles in the PDF (e.g. "The Sigma-Point Estimator" in Ch. 12): `##`.
   - "Contributed by …" is a plain italic line, `*Contributed by J. Russell Carpenter*`, never a heading.
   - Remove stray "CHAPTER N" lines, since the number goes into the chapter heading.
   - Math in headings is written as `$…$`.
8. **Algorithm boxes.** Format them as a blockquote:
   ```
   > **Algorithm 1.1** The Linear Kalman Filter
   >
   > Initialize: …
   >
   > $$ … \tag{1.17} $$
   ```
   Reproduce every line of the box, including text lines such as "for i = 1, 2, … do". Boxed best-practice or summary frames, if present, also become blockquotes.
9. **Tables.** Real tables (e.g. the Notational Conventions table, Lear's table in Ch. 3, the Contents) become GFM pipe tables. Inside table cells, write `|` in math as `\vert`, `\lvert`/`\rvert` or `\|`, so it doesn't split cells. Contents becomes a nested list or a two-column table without dotted leaders.
10. **Images.** Keep the image links whose files exist (`_page_39_Figure_6.jpeg` etc.) together with their captions as `*Figure 3.1. …*`. **Delete** image links to `_page_N_Picture_1.jpeg` for N in {11,17,21,23,31,57,63,71,123,135,139,145,159,169}. Those files don't exist; they are blank pages.

## Before finishing
- Re-read your output against the page images once more, focusing on equations.
- Run a self-check: list all `\tag{…}` values in your output and compare them with the equation numbers visible on your pages (`pdftotext -layout` helps). Report any you couldn't place.
- Check that every `id="page-…"` from the input chunk is still present in your output. For example: `grep -o 'id="page-[^"]*"' in | sort > a; grep -o … out | sort > b; comm -23 a b` must print nothing.
- Check that `$$` delimiters are balanced.

## Report back (under 200 words)
Include: pages covered, number of display equations in your output, how many you corrected, any equation numbers that are missing or uncertain, any passages you couldn't resolve, and the results of the anchor and `$$` checks.
