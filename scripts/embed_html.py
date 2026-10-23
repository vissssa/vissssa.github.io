#!/usr/bin/env python3
"""Turn a standalone HTML doc into a fuwari post: drop <head>/hero/sidebar(TOC),
keep <main> content, scope the doc's CSS under .mcp-doc so it can't leak onto the
fuwari page chrome. Input path is an argument (untrusted download stays as data).

Usage: python -I embed_html.py <src.html> <dst.md>
"""
import re
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
WRAP = "mcp-doc"

# selectors whose elements we removed (hero/sidebar/wrap/footer) -> drop the rule
DROP = ("html", ".hero", "#sidebar", ".wrap", ".footer", ".toc-note", ".sb-")
# bare selectors that should map to the wrapper itself, not a descendant
SELF = {"body", "main"}

html = SRC.read_text(encoding="utf-8")


def extract(tag_open_re, close):
    m = re.search(tag_open_re, html)
    start = m.start()
    end = html.index(close, start) + len(close)
    return html[start:end]


def inner(block, open_tag_end):
    return block[block.index(">", 0) + 1: block.rindex(open_tag_end)] if False else block


def scope_selector(sel: str) -> str | None:
    sel = sel.strip()
    if not sel:
        return None
    if sel.startswith("@") or sel == ":root":
        return sel
    parts = [p.strip() for p in sel.split(",")]
    out = []
    for p in parts:
        if any(p == d or p.startswith(d) for d in DROP):
            continue
        if p == "*":
            out.append(f".{WRAP} *")
        elif p in SELF:
            out.append(f".{WRAP}")
        elif p.startswith(f".{WRAP}"):
            out.append(p)
        else:
            out.append(f".{WRAP} {p}")
    return ", ".join(out) if out else None


def scope_css(css: str) -> str:
    """Scope a flat/@media CSS blob. Simple brace walker; values have no braces."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # drop comments (break the walker)
    out = []
    i, n = 0, len(css)
    while i < n:
        # find next '{' at this level
        j = css.find("{", i)
        if j == -1:
            break
        sel = css[i:j].strip()
        if sel.startswith("@media") or sel.startswith("@supports"):
            # find matching close brace for the @-block body
            depth, k = 1, j + 1
            while k < n and depth:
                if css[k] == "{":
                    depth += 1
                elif css[k] == "}":
                    depth -= 1
                k += 1
            body = css[j + 1:k - 1]
            out.append(f"{sel}{{{scope_css(body)}}}")
            i = k
            continue
        # plain rule: body is up to next '}'
        k = css.find("}", j)
        body = css[j + 1:k]
        new_sel = scope_selector(sel)
        if new_sel:
            out.append(f"{new_sel}{{{body}}}")
        i = k + 1
    return "".join(out)


style_block = extract(r"<style>", "</style>")
style_css = style_block[len("<style>"):-len("</style>")]
scoped = scope_css(style_css)

main_block = extract(r"<main>", "</main>")
main_inner = main_block[len("<main>"):-len("</main>")].strip()

front = (
    "---\n"
    "title: MCP 完全指南\n"
    "published: 2026-10-22\n"
    "description: 面向中高级 AI Agent 开发工程师的 MCP 深度教程。\n"
    "tags: [MCP, AI Agent, 协议]\n"
    "category: 教程\n"
    "draft: false\n"
    "---\n\n"
)

body = f"<style>\n{scoped}\n</style>\n\n<div class=\"{WRAP}\">\n{main_inner}\n</div>\n"
DST.write_text(front + body, encoding="utf-8")
print(f"wrote {DST}  (css {len(scoped)} chars, body {len(main_inner)} chars)")
