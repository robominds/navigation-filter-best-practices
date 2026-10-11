#!/usr/bin/env python3
"""Generate per-chapter Markdown files from the single-file edition.

Usage:
    python3 tools/split.py

The single file "Navigation Filter Best Practices 2025.md" is the canonical
edition. It is too large for GitHub to render (the limit is 512 KiB), so this
script writes chapters/NN-*.md for browsing on GitHub, with these changes:
  * internal links that point into another chapter file are rewritten as
    <file>.md#<anchor>
  * image paths are adjusted for the subdirectory
  * each file gets previous / contents / next navigation
  * math is rewritten into GitHub's verbatim syntax (```math fences and $`…`$),
    because GitHub otherwise applies Markdown escaping inside $…$ / $$…$$
Edit the single file, then re-run this script; never edit chapters/ by hand.
"""
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Navigation Filter Best Practices 2025.md")
OUT = os.path.join(ROOT, "chapters")


def slug(title):
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"^(Chapter|Appendix)\s+([0-9A-C]+)\.\s*", "", title)
    s = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower()
    return s[:60].rstrip("-")


GREEK = {
    "alpha": "ALPHA", "beta": "BETA", "gamma": "GAMMA", "delta": "DELTA", "epsilon": "EPSILON SYMBOL",
    "varepsilon": "EPSILON", "zeta": "ZETA", "eta": "ETA", "theta": "THETA", "vartheta": "THETA SYMBOL",
    "iota": "IOTA", "kappa": "KAPPA", "lambda": "LAMDA", "mu": "MU", "nu": "NU", "xi": "XI", "pi": "PI",
    "varpi": "PI SYMBOL", "rho": "RHO", "sigma": "SIGMA", "tau": "TAU", "upsilon": "UPSILON",
    "phi": "PHI SYMBOL", "varphi": "PHI", "chi": "CHI", "psi": "PSI", "omega": "OMEGA",
}
# TeX font command -> (Unicode style for Latin/digits, style for lowercase Greek, style for uppercase Greek)
STYLES = {
    "mathbf": ("BOLD", "BOLD", "BOLD"),
    "boldsymbol": ("BOLD ITALIC", "BOLD ITALIC", "BOLD"),
    "mathsf": ("SANS-SERIF", None, None),
    "boldsf": ("SANS-SERIF BOLD", "SANS-SERIF BOLD", "SANS-SERIF BOLD"),
    "mathcal": ("SCRIPT", None, None),
    "mathbb": ("DOUBLE-STRUCK", None, None),
    "mathit": ("ITALIC", "ITALIC", "ITALIC"),
}
LETTERLIKE = {  # code points the Mathematical Alphanumeric block leaves to Letterlike Symbols
    ("SCRIPT", "B"): "ℬ", ("SCRIPT", "E"): "ℰ", ("SCRIPT", "F"): "ℱ", ("SCRIPT", "H"): "ℋ",
    ("SCRIPT", "I"): "ℐ", ("SCRIPT", "L"): "ℒ", ("SCRIPT", "M"): "ℳ", ("SCRIPT", "R"): "ℛ",
    ("SCRIPT", "e"): "ℯ", ("SCRIPT", "g"): "ℊ", ("SCRIPT", "o"): "ℴ", ("ITALIC", "h"): "ℎ",
    ("DOUBLE-STRUCK", "C"): "ℂ", ("DOUBLE-STRUCK", "H"): "ℍ", ("DOUBLE-STRUCK", "N"): "ℕ",
    ("DOUBLE-STRUCK", "P"): "ℙ", ("DOUBLE-STRUCK", "Q"): "ℚ", ("DOUBLE-STRUCK", "R"): "ℝ",
    ("DOUBLE-STRUCK", "Z"): "ℤ",
}
DIGITS = "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE".split()


def styled(cmd, token):
    """Unicode mathematical alphanumeric for one token (letter, digit or Greek macro), or None."""
    latin, small_greek, cap_greek = STYLES[cmd]
    try:
        if len(token) == 1 and token.isalpha():
            if (latin, token) in LETTERLIKE:
                return LETTERLIKE[(latin, token)]
            case = "CAPITAL" if token.isupper() else "SMALL"
            return unicodedata.lookup(f"MATHEMATICAL {latin} {case} {token.upper()}")
        if len(token) == 1 and token.isdigit():
            style = "SANS-SERIF BOLD" if latin.startswith("SANS-SERIF BOLD") else ("BOLD" if "BOLD" in latin else latin)
            return unicodedata.lookup(f"MATHEMATICAL {style} DIGIT {DIGITS[int(token)]}")
        name = token.lstrip("\\")
        if name.lower() in GREEK:
            upper = name[0].isupper()
            style = cap_greek if upper else small_greek
            if style is None:
                return None
            if upper:
                return unicodedata.lookup(f"MATHEMATICAL {style} CAPITAL {GREEK[name.lower()].replace(' SYMBOL', '')}")
            if GREEK[name].endswith("SYMBOL"):  # e.g. MATHEMATICAL BOLD ITALIC PHI SYMBOL (no SMALL)
                return unicodedata.lookup(f"MATHEMATICAL {style} {GREEK[name]}")
            return unicodedata.lookup(f"MATHEMATICAL {style} SMALL {GREEK[name]}")
    except KeyError:
        return None
    return None


def unicode_fonts(tex):
    """Replace \\mathbf{…}, \\boldsymbol{…}, \\mathsf{…}, \\mathcal{…}, \\mathbb{…}, \\mathit{…} with
    Unicode mathematical letters. GitHub renders math as native MathML, and Chrome ignores
    MathML's mathvariant attribute, so these fonts would otherwise all show as plain italic."""
    def convert(cmd, arg):
        out = []
        for tok in re.findall(r"\\[A-Za-z]+|\\_|.", arg):
            if tok.isspace():
                continue
            u = styled(cmd, tok)
            out.append(u if u else tok)
        return "".join(out)
    tex = re.sub(r"\\boldsymbol\{\\mathsf\{([^{}]*)\}\}", lambda m: "{" + convert("boldsf", m.group(1)) + "}", tex)
    return re.sub(r"\\(mathbf|boldsymbol|mathsf|mathcal|mathbb|mathit)\{([^{}]*)\}",
                  lambda m: "{" + convert(m.group(1), m.group(2)) + "}", tex)


def fixed_delimiters(tex):
    """Chrome mis-positions a sub+superscripted term inside stretchy \\left…\\right fences. For
    such pairs use fixed-size delimiters (\\biggl/\\biggr around fractions, integrals and sums,
    \\Bigl/\\Bigr otherwise)."""
    tokens = list(re.finditer(r"\\(left|right)\s*(\\[A-Za-z]+|\\[{}|]|[.()\[\]|])", tex))
    stack, pairs = [], []
    for t in tokens:
        if t.group(1) == "left":
            stack.append(t)
        elif stack:
            pairs.append((stack.pop(), t))
    edits = []
    for left, right in pairs:
        inner = tex[left.end():right.start()]
        if not ("_" in inner and "^" in inner):
            continue
        size = "bigg" if re.search(r"\\(d?frac|int|sum|genfrac|begin)", inner) else "Big"
        for t, side in ((left, "l"), (right, "r")):
            delim = t.group(2)
            edits.append((t.start(), t.end(), "" if delim == "." else f"\\{size}{side}{delim}"))
    for a, b, rep in sorted(edits, reverse=True):
        tex = tex[:a] + rep + tex[b:]
    return tex


def github_math(text):
    """Rewrite math into GitHub's verbatim math syntax.

    Works around these GitHub rendering quirks:
      * GitHub applies Markdown backslash-escaping inside $…$ and $$…$$ (so `\\,`
        becomes `,` and `\\\\` becomes `\\`). Fenced ```math blocks and $`…`$
        spans are passed to MathJax untouched.
      * `<`, `>` and (in inline spans) `&` are double-escaped, so `<`/`>` are written
        \\lt/\\gt and inline matrices are rebuilt without `&`.
      * A "\\\\" at the end of a line gets an extra backslash, so each display
        block is written on one line.
      * Safari clips \\widetilde with a scrollbar, so single-symbol wide tildes use \\tilde.
      * GitHub hands MathJax's output to the browser as native MathML. Chrome cannot lay out
        <mlabeledtr> (from \\tag), so numbers are written after the equation, and it ignores
        mathvariant, so font commands become Unicode mathematical letters (see unicode_fonts).
      * Chrome also mis-positions sub+superscripted terms inside stretchy \\left…\\right fences,
        so those pairs get fixed-size delimiters (fixed_delimiters).
      * In a list that contains inline math, display blocks inside the list are
        not rendered, so display blocks are moved out of lists (blockquotes are fine).
    """
    def no_amp(tex):
        # Inline $`…`$ spans double-escape "&", which breaks matrices; rebuild 1- and
        # 2-row bmatrix without it (row vector -> bracketed list, 2 rows -> stacked columns).
        def repl(m):
            rows = [r.strip() for r in m.group(1).split("\\\\")]
            cells = [[c.strip() for c in r.split("&")] for r in rows]
            if len(cells) == 1:
                return "\\left[\\, " + " \\;\\; ".join(cells[0]) + " \\,\\right]"
            if len(cells) == 2 and len(cells[0]) == len(cells[1]):
                cols = ["\\genfrac{}{}{0pt}{}{" + a + "}{" + b + "}" for a, b in zip(*cells)]
                return "\\left[\\, " + " \\;\\; ".join(cols) + " \\,\\right]"
            raise ValueError("cannot rewrite inline matrix without &: " + m.group(0))
        return re.sub(r"\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}", repl, tex) if "&" in tex else tex

    def narrow_tilde(tex):
        # Safari clips \widetilde with a scrollbar; on a single symbol \tilde looks the same.
        return re.sub(r"\\widetilde\{((?:\\(?:mathbf|boldsymbol|mathrm|mathsf)\{\\?[A-Za-z]+\})|\\?[A-Za-z]+)\}",
                      r"\\tilde{\1}", tex)

    def ltgt(tex):
        return re.sub(r"\s*([<>])\s*", lambda m: " \\lt " if m.group(1) == "<" else " \\gt ", tex)

    out = []
    pos = 0
    for m in re.finditer(r"\$\$(.*?)\$\$", text, flags=re.S):
        line_start = text.rfind("\n", 0, m.start()) + 1
        prefix = text[line_start:m.start()]
        if not re.fullmatch(r"[ >]*", prefix):
            raise ValueError(f"display math does not start a line: {text[line_start:m.end()][:80]!r}")
        body = [re.sub("^" + re.escape(prefix), "", l) if l.startswith(prefix) else l.lstrip(" >")
                for l in m.group(1).strip("\n").split("\n")]
        body = [unicode_fonts(narrow_tilde(ltgt(b.strip()))) for b in body if b.strip()]
        body = [fixed_delimiters(" ".join(body))]
        # Chrome cannot lay out MathJax's <mlabeledtr> (from \\tag), so show the number after the equation.
        body = [re.sub(r"\\tag\{([^}]*)\}", r"\\qquad\\qquad(\1)", b) for b in body]
        fence_prefix = "> " if ">" in prefix else ""
        out.append(text[pos:line_start])
        # One line per block: GitHub appends a backslash to a line-ending "\\".
        out.append("\n".join([fence_prefix + "```math", fence_prefix + " ".join(body), fence_prefix + "```"]))
        pos = m.end()
        if pos < len(text) and text[pos] != "\n":
            out.append("\n")
    out.append(text[pos:])
    text = "".join(out)

    # Inline math, skipping fenced blocks.
    parts = re.split(r"(```math.*?```)", text, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<![\\$`])\$([^$\n`]+?)\$(?![$`])",
                          lambda m: "$`" + fixed_delimiters(unicode_fonts(narrow_tilde(no_amp(ltgt(m.group(1)))))).strip() + "`$", parts[i])
    return "".join(parts)


# GitHub stops rendering math part-way down a page once a page's math gets too heavy
# (observed from about 18,000 characters of TeX, depending on complexity). Chapters
# above this budget are split at section boundaries.
MATH_BUDGET = 12000


def math_chars(lines):
    text = "\n".join(lines)
    display = re.findall(r"\$\$(.*?)\$\$", text, flags=re.S)
    rest = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
    return sum(map(len, display)) + sum(map(len, re.findall(r"(?<![\\$])\$([^$\n]+?)\$", rest)))


def split_by_budget(lines, level=2):
    """Split lines into groups at headings of `level` (then deeper) so each group fits MATH_BUDGET."""
    if math_chars(lines) <= MATH_BUDGET or level > 4:
        return [lines]
    marker = "#" * level + " "
    cuts = [i for i, l in enumerate(lines) if l.startswith(marker) and i > 0]
    if not cuts:
        return split_by_budget(lines, level + 1)
    sections = [lines[a:b] for a, b in zip([0] + cuts, cuts + [len(lines)])]
    groups, current = [], []
    for sec in sections:
        if current and math_chars(current + sec) > MATH_BUDGET:
            groups.append(current)
            current = []
        current = current + sec
    groups.append(current)
    out = []
    for g in groups:
        out.extend(split_by_budget(g, level + 1) if math_chars(g) > MATH_BUDGET else [g])
    # Merge neighbouring pieces that fit together.
    merged = [out[0]]
    for g in out[1:]:
        if math_chars(merged[-1] + g) <= MATH_BUDGET:
            merged[-1] = merged[-1] + g
        else:
            merged.append(g)
    return merged


def first_heading(lines):
    for l in lines:
        if l.startswith("#"):
            return re.sub(r"<[^>]+>", "", l.lstrip("#")).strip()
    return ""


def main():
    lines = open(SRC, encoding="utf-8").read().split("\n")

    # Split at top-level headings from Chapter 1 onwards; everything before is front matter.
    starts = [i for i, l in enumerate(lines)
              if re.match(r"# (<span[^>]*></span>)*(Chapter \d+\.|Appendix [A-C]\.|Bibliography|Index of Best Practices)", l)]
    bounds = [0] + starts + [len(lines)]
    parts = []
    for n, (a, b) in enumerate(zip(bounds, bounds[1:])):
        body = lines[a:b]
        if n == 0:
            title, name = "Front Matter", "00-front-matter.md"
        else:
            heading = re.sub(r"<[^>]+>", "", body[0][2:]).strip()
            m = re.match(r"(Chapter (\d+)|Appendix ([A-C]))\.", heading)
            if m and m.group(2):
                prefix = f"{int(m.group(2)):02d}"
            elif m:
                prefix = f"{12 + 'ABC'.index(m.group(3)) + 1:02d}-appendix-{m.group(3).lower()}"
            else:
                prefix = f"{n:02d}"
            title, name = heading, f"{prefix}-{slug(heading)}.md"
        groups = split_by_budget(body)
        if len(groups) == 1:
            parts.append({"title": title, "name": name, "lines": body})
            continue
        for g, glines in enumerate(groups, 1):
            parts.append({"title": f"{title} (part {g} of {len(groups)})",
                          "index_title": None if g == 1 else first_heading(glines),
                          "name": name.replace(".md", f"-part{g}.md"),
                          "lines": glines if g == 1 else
                          [f"*{title}, continued*", ""] + glines})

    # Map each anchor to the file that contains it, for rewriting cross-file links.
    owner = {}
    for p in parts:
        for l in p["lines"]:
            for anchor in re.findall(r'id="([^"]+)"', l):
                owner[anchor] = p["name"]

    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".md"):
            os.remove(os.path.join(OUT, f))

    index = ["# Navigation Filter Best Practices: Chapters", "",
             "Generated from the single-file edition by `tools/split.py`; edit the single file, not these.", ""]
    for k, p in enumerate(parts):
        text = "\n".join(p["lines"]).strip("\n")

        def relink(m):
            anchor = m.group(1)
            target = owner.get(anchor)
            if target is None or target == p["name"]:
                return m.group(0)
            return f"]({target}#{anchor})"

        text = re.sub(r"\]\(#([^)]+)\)", relink, text)
        text = re.sub(r"(!\[[^\]]*\]\()(_page_[^)]+\))", r"\1../\2", text)
        text = github_math(text)

        nav = []
        if k > 0:
            nav.append(f"[← {parts[k - 1]['title']}]({parts[k - 1]['name']})")
        nav.append("[Contents](README.md)")
        if k + 1 < len(parts):
            nav.append(f"[{parts[k + 1]['title']} →]({parts[k + 1]['name']})")
        nav_line = " · ".join(nav)

        with open(os.path.join(OUT, p["name"]), "w", encoding="utf-8") as fh:
            fh.write(f"{nav_line}\n\n{text}\n\n---\n\n{nav_line}\n")
        if p.get("index_title"):
            index.append(f"  - [{p['index_title']}]({p['name']})")
        else:
            index.append(f"- [{p['title'].split(' (part')[0]}]({p['name']})")

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(index) + "\n")

    for p in parts:
        size = os.path.getsize(os.path.join(OUT, p["name"]))
        print(f"{size:>8}  {p['name']}")


if __name__ == "__main__":
    main()
