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
Edit the single file, then re-run this script; never edit chapters/ by hand.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Navigation Filter Best Practices 2025.md")
OUT = os.path.join(ROOT, "chapters")


def slug(title):
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"^(Chapter|Appendix)\s+([0-9A-C]+)\.\s*", "", title)
    s = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-").lower()
    return s[:60].rstrip("-")


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
        parts.append({"title": title, "name": name, "lines": body})

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

        nav = []
        if k > 0:
            nav.append(f"[← {parts[k - 1]['title']}]({parts[k - 1]['name']})")
        nav.append("[Contents](README.md)")
        if k + 1 < len(parts):
            nav.append(f"[{parts[k + 1]['title']} →]({parts[k + 1]['name']})")
        nav_line = " · ".join(nav)

        with open(os.path.join(OUT, p["name"]), "w", encoding="utf-8") as fh:
            fh.write(f"{nav_line}\n\n{text}\n\n---\n\n{nav_line}\n")
        index.append(f"- [{p['title']}]({p['name']})")

    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(index) + "\n")

    for p in parts:
        size = os.path.getsize(os.path.join(OUT, p["name"]))
        print(f"{size:>8}  {p['name']}")


if __name__ == "__main__":
    main()
