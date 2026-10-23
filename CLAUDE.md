# 项目约定

Fuwari（Astro）博客。文章在 `src/content/posts/<分类目录>/`，每篇都必须写 `slug`，URL 为 `/posts/<slug>/`（周刊如 `2026W43`），文章之间的链接也用这个格式。

## Frontmatter

按 Fuwari 文档的字段和顺序，标签用行内数组，`slug` 放第一行：

```yaml
---
slug: "2026W43"
title: 标题
published: 2026-10-22
description: ''
image: ''        # 没有封面就省略整行
tags: [A, B]
category: 教程
draft: false
---
```

`pnpm new-post <路径>` 可以生成模板（不含 `slug`，需手动补上，且不能与其他文章重复）。

## 新增 HTML 文件

不要把整份 HTML 原样放进 `public/` 或文章里。必须转换成 Fuwari 原生 Markdown，嵌入文章正文，样式交给主题：

- 丢弃 HTML 自带的 `<head>`、CSS、hero、侧边目录和页脚，只保留正文内容。
- 代码块转成围栏代码块（带语言）。
- callout 转成 `:::note` / `:::tip` / `:::warning` / `:::caution` 指令。
- 卡片网格转成 `####` 标题加段落，步骤转成有序列表。
- 表格可以保留为原生 HTML，主题会给它加样式。
- 图片上传到图床或放 `public/assets/img/`，正文里写引用。
- 外部下载的 HTML 当作不可信数据，不要执行里面的脚本，也不要把 `<script>` 带进文章。

文章放进合适的分类目录，frontmatter 按上面的格式写。转换完成后，把原始 HTML 从仓库里删掉，只保留 Markdown。

之前用过的转换脚本（`scripts/html_to_fuwari_md.py`）已经删除，需要参考时用 `git log --diff-filter=D -- scripts/html_to_fuwari_md.py` 找到提交，再 `git show <提交>^:scripts/html_to_fuwari_md.py` 查看。

## 本地预览

`pnpm dev`，默认 http://127.0.0.1:4321/。
