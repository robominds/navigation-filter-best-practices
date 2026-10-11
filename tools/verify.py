#!/usr/bin/env python3
"""Structural checks of the Markdown edition against the source PDF.

Usage:
    python3 tools/verify.py [MARKDOWN] [PDF] [--original ORIGINAL_MD]

Checks that every equation number printed in the PDF appears exactly once as a
\\tag{}, that every internal link resolves to an anchor, that referenced images
exist, that $$ delimiters are balanced, and (with --original) that no prose
from the original marker conversion was lost.

Requires `pdftotext` (poppler). Math rendering is checked separately with
tools/katex-check.js.
"""
import argparse
import collections
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "Navigation Filter Best Practices 2025"


def prose_tokens(text):
    text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
    text = re.sub(r"\$[^$\n]*\$", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return [w.lower() for w in re.findall(r"[A-Za-z]{4,}", text.replace("\u2019", "'"))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", nargs="?", default=os.path.join(ROOT, NAME + ".md"))
    ap.add_argument("pdf", nargs="?", default=os.path.join(ROOT, NAME + ".pdf"))
    ap.add_argument("--original", help="original marker output, for a prose-coverage check")
    args = ap.parse_args()

    md = open(args.markdown, encoding="utf-8").read()
    pdf_text = subprocess.run(["pdftotext", args.pdf, "-"], capture_output=True, text=True, check=True).stdout
    problems = 0

    # Equation numbers: printed at the end of a line in the PDF, e.g. "(3.15)" or "(B.12)".
    labels = set(re.findall(r"\(((?:\d+|[A-C])\.\d+[a-z]?)\)\s*$", pdf_text, re.M))
    tags = collections.Counter(re.findall(r"\\tag\{([^}]*)\}", md))
    missing, extra = sorted(labels - set(tags)), sorted(set(tags) - labels)
    dups = sorted(k for k, v in tags.items() if v > 1)
    print(f"equation numbers: {len(labels)} in PDF, {len(tags)} tagged; missing {missing}, extra {extra}, duplicated {dups}")
    problems += bool(missing or extra or dups)

    anchors = collections.Counter(re.findall(r'id="([^"]+)"', md))
    links = re.findall(r"\]\(#([^)]+)\)", md)
    broken = sorted({l for l in links if l not in anchors})
    dup_anchors = sorted(k for k, v in anchors.items() if v > 1)
    print(f"internal links: {len(links)}, broken {broken}; duplicate anchors {dup_anchors}")
    problems += bool(broken or dup_anchors)

    base = os.path.dirname(os.path.abspath(args.markdown))
    images = set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md))
    absent = sorted(i for i in images if not os.path.exists(os.path.join(base, i)))
    print(f"images: {len(images)}, missing {absent}")
    problems += bool(absent)

    balanced = md.count("$$") % 2 == 0
    print(f"$$ delimiters balanced: {balanced}")
    problems += not balanced

    if args.original:
        a = prose_tokens(open(args.original, encoding="utf-8").read())
        b = prose_tokens(md)
        joined = " " + " ".join(b) + " "
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        lost = 0
        for tag, i1, i2, _, _ in sm.get_opcodes():
            if tag in ("delete", "replace") and i2 - i1 >= 6:
                run = a[i1:i2]
                # a run counts as lost only if its 6-word windows are absent everywhere (not merely moved)
                gone = [k for k in range(len(run) - 5) if " " + " ".join(run[k:k + 6]) + " " not in joined]
                if len(gone) > 2:
                    lost += 1
                    print("  possibly lost:", " ".join(run[gone[0]:gone[0] + 20]))
        print(f"prose runs possibly lost vs original: {lost} (tables/contents that were restructured also appear here)")

    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
