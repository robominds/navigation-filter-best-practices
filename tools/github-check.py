#!/usr/bin/env python3
"""Check that GitHub passes every math expression in chapters/ to MathJax unchanged.

Usage:
    python3 tools/github-check.py [owner/repo]

Renders each chapter through the GitHub Markdown API (`gh api markdown`,
needs the GitHub CLI and network access) and compares the TeX inside every
<math-renderer> element with the source. Note that MathJax itself runs in the
browser, so this catches Markdown mangling and missed math, not MathJax errors.
GitHub also rejects some macros (e.g. \\operatorname) at render time; those are
checked by DISALLOWED below.
"""
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, "chapters")
DISALLOWED = ["\\operatorname"]


def source_math(text):
    display = [re.sub(r"(?m)^[ >]*", "", m).strip()
               for m in re.findall(r"```math\n(.*?)\n[ >]*```", text, flags=re.S)]
    rest = re.sub(r"```math.*?```", "", text, flags=re.S)
    inline = re.findall(r"\$`(.+?)`\$", rest)
    return display, inline


def rendered_math(page):
    display = [html.unescape(m).strip()[2:-2].strip()
               for m in re.findall(r'js-display-math[^>]*>(.*?)</math-renderer>', page, flags=re.S)]
    inline = [html.unescape(m).strip()[1:-1].strip()
              for m in re.findall(r'js-inline-math[^>]*>(.*?)</math-renderer>', page, flags=re.S)]
    return display, inline


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "robominds/navigation-filter-best-practices"
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    failures = 0
    for name in sorted(os.listdir(CHAPTERS)):
        if not name[:2].isdigit():
            continue
        text = open(os.path.join(CHAPTERS, name), encoding="utf-8").read()
        payload = json.dumps({"text": text, "mode": "gfm", "context": repo})
        page = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=payload,
                              capture_output=True, text=True, check=True).stdout
        sd, si = source_math(text)
        rd, ri = rendered_math(page)
        bad_d = [s for s, r in zip(sd, rd) if norm(s) != norm(r)]
        bad_i = [s for s, r in zip(si, ri) if norm(s) != norm(r)]
        banned = [m for m in DISALLOWED if m in text]
        ok = len(sd) == len(rd) and len(si) == len(ri) and not bad_d and not bad_i and not banned
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: display {len(rd)}/{len(sd)}, inline {len(ri)}/{len(si)}"
              + (f", altered {len(bad_d) + len(bad_i)}" if bad_d or bad_i else "")
              + (f", disallowed {banned}" if banned else ""))
        for s in (bad_d + bad_i)[:3]:
            print("     ", s[:120])
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
