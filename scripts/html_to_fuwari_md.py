#!/usr/bin/env python3
"""Convert the MCP tutorial HTML into fuwari-native Markdown (theme styles it).

Drops the doc's own CSS/hero/sidebar; maps components to fuwari equivalents:
  .codeblock          -> fenced code block (expressive-code)
  .callout c-*        -> :::note/:::tip/:::warning/:::caution directive
  .grid2 > .card      -> #### heading + paragraph
  .step-h             -> ordered list
  table               -> kept as raw HTML (prose styles it)
Input path is an argument (untrusted download stays data). Run with -I.
"""
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])

CALLOUT = {"c-note": "note", "c-tip": "tip", "c-warn": "warning", "c-danger": "caution"}


def lang_of(text: str) -> str:
    w = text.strip().split("·")[0].strip().split()[0].lower() if text.strip() else ""
    return {"typescript": "typescript", "ts": "typescript", "js": "javascript",
            "json": "json", "python": "python", "bash": "bash", "http": "http",
            "nginx": "nginx"}.get(w, w or "text")


def inline(node) -> str:
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    name = node.name
    if name in ("strong", "b"):
        return f"**{inline_children(node).strip()}**"
    if name in ("em", "i"):
        return f"*{inline_children(node).strip()}*"
    if name == "code":
        return f"`{node.get_text()}`"
    if name == "a":
        return f"[{inline_children(node).strip()}]({node.get('href', '')})"
    if name == "br":
        return "\n"
    return inline_children(node)


def inline_children(node) -> str:
    return "".join(inline(c) for c in node.children)


def codeblock(div) -> str:
    lang_span = div.find("span", class_="lang")
    lang = lang_of(lang_span.get_text() if lang_span else "")
    code = div.find("code")
    body = code.get_text() if code else ""
    return f"```{lang}\n{body.rstrip()}\n```"


def callout(div) -> str:
    kind = next((CALLOUT[c] for c in div.get("class", []) if c in CALLOUT), "note")
    ct = div.find("span", class_="ct")
    title = ct.get_text(strip=True) if ct else ""
    if ct:
        ct.extract()
    paras = [inline_children(p).strip() for p in div.find_all("p", recursive=False)]
    inner = "\n\n".join(p for p in paras if p)
    head = f":::{kind}[{title}]" if title else f":::{kind}"
    return f"{head}\n{inner}\n:::"


def card(div) -> str:
    parts = []
    for ch in div.find_all(recursive=False):
        if ch.name == "h4":
            parts.append(f"#### {inline_children(ch).strip()}")
        elif ch.name == "p":
            parts.append(inline_children(ch).strip())
    return "\n\n".join(parts)


def listify(ul, indent=0) -> str:
    lines = []
    pad = "  " * indent
    for li in ul.find_all("li", recursive=False):
        sub = li.find(["ul", "ol"], recursive=False)
        if sub:
            sub.extract()
        lines.append(f"{pad}- {inline_children(li).strip()}")
        if sub:
            lines.append(listify(sub, indent + 1))
    return "\n".join(lines)


def heading(tag, level) -> str:
    num = tag.find("span", class_="num")
    prefix = ""
    if num:
        prefix = num.get_text(strip=True) + " "
        num.extract()
    return f"{'#' * level} {prefix}{inline_children(tag).strip()}"


def convert_block(tag) -> str | None:
    cls = tag.get("class", [])
    name = tag.name
    if name == "h2":
        return heading(tag, 2)
    if name == "h3":
        return heading(tag, 3)
    if name == "h4":
        return heading(tag, 4)
    if name == "p":
        return inline_children(tag).strip()
    if name == "hr":
        return "---"
    if name in ("ul", "ol"):
        return listify(tag)
    if name == "table":
        return str(tag)  # prose styles raw HTML tables
    if name == "div" and "codeblock" in cls:
        return codeblock(tag)
    if name == "div" and "callout" in cls:
        return callout(tag)
    if name == "div" and "grid2" in cls:
        return "\n\n".join(card(c) for c in tag.find_all("div", class_="card", recursive=False))
    if name == "div" and "footer" in cls:
        return None
    return inline_children(tag).strip() or None


def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "lxml")
    root = soup.find("main")
    children = [c for c in root.find_all(recursive=False)]
    blocks, i = [], 0
    while i < len(children):
        ch = children[i]
        if ch.name == "div" and "step-h" in ch.get("class", []):
            steps = []
            while i < len(children) and children[i].name == "div" and "step-h" in children[i].get("class", []):
                p = children[i].find("p")
                steps.append(f"{len(steps) + 1}. {inline_children(p).strip() if p else ''}")
                i += 1
            blocks.append("\n".join(steps))
            continue
        b = convert_block(ch)
        if b:
            blocks.append(b)
        i += 1

    front = (
        "---\n"
        "title: MCP 完全指南\n"
        "published: 2026-10-22\n"
        "category: 教程\n"
        "tags:\n- MCP\n- AI Agent\n- 协议\n"
        "description: 面向中高级 AI Agent 开发工程师的 MCP 深度教程。\n"
        "---\n\n"
    )
    DST.write_text(front + "\n\n".join(blocks) + "\n", encoding="utf-8")
    print(f"wrote {DST}  ({len(blocks)} blocks)")


if __name__ == "__main__":
    main()
