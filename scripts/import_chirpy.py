#!/usr/bin/env python3
"""Convert Chirpy (Jekyll) posts to fuwari frontmatter and copy into src/content/posts/.

Chirpy -> fuwari field mapping:
  date (datetime, maybe '+0800')  -> published (date only)
  categories: [a, b]              -> category: a   (fuwari takes a single string)
  tags: [...]                     -> tags (unchanged)
  image: <url|empty>              -> image if non-empty, else dropped ("" default in schema)
Subdirectory layout under _posts is mirrored under src/content/posts/.
"""
import sys
from pathlib import Path
from datetime import date, datetime
import yaml

SRC = Path(sys.argv[1])          # .../2han99Siegward.github.io/_posts
DST = Path(sys.argv[2])          # .../podcast/src/content/posts


def split_front_matter(text: str):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    return parts[1], parts[2]


def to_published(val) -> date:
    # val may be a datetime.date/datetime, or str like '2020-08-01 00:01:00 +0800'.
    # Return a date object so pyyaml emits it unquoted (Astro parses it as a date).
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    s = str(val).split(" ")[0].split("T")[0]
    y, m, d = (int(x) for x in s.split("-")[:3])
    return date(y, m, d)


def convert(fm: dict) -> dict:
    out = {"title": str(fm.get("title", "Untitled"))}
    if fm.get("date"):
        out["published"] = to_published(fm["date"])
    cats = fm.get("categories")
    if isinstance(cats, list) and cats:
        out["category"] = str(cats[0])
    elif isinstance(cats, str) and cats:
        out["category"] = cats
    tags = fm.get("tags")
    if tags:
        out["tags"] = tags if isinstance(tags, list) else [tags]
    img = fm.get("image")
    if img:
        out["image"] = img
    return out


def main():
    count = 0
    for md in SRC.rglob("*.md"):
        raw = md.read_text(encoding="utf-8")
        fm_text, body = split_front_matter(raw)
        if fm_text is None:
            continue
        fm = yaml.safe_load(fm_text) or {}
        new_fm = convert(fm)
        rel = md.relative_to(SRC)
        target = DST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        dumped = yaml.safe_dump(new_fm, allow_unicode=True, sort_keys=False).strip()
        target.write_text(f"---\n{dumped}\n---\n{body.lstrip(chr(10))}", encoding="utf-8")
        count += 1
    print(f"converted {count} posts -> {DST}")


if __name__ == "__main__":
    main()
