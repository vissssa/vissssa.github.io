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

## 周刊标签

周刊（`src/content/posts/week/`）的 `tags` 固定以 `周报, Weekly` 开头，后面按本周内容补主题标签。新周刊提交前检查一遍，只有 `周报, Weekly` 的要补上。

- 粒度要粗：只打大类，不打具体品牌、公司、产品、人名、地名（不要 `苹果`、`比亚迪`、`马斯克`、`上海`，分别归到 `消费电子`、`新能源`、`ai`/`国际政治`、`旅游`）。
- 优先复用已有标签，不新增近义词。现有词表：`ai` `消费电子` `社会工程` `新能源` `游戏` `互联网` `工作` `程序员` `科学` `国际政治` `经济` `运动` `美食` `旅游` `娱乐` `节日` `工具推荐` `健康` `猫` `历史` `穿搭` `年度总结`。确实没有合适的才新增，新增后同步更新这份词表。
- 只覆盖本周主要话题，一般 2~10 个；不要为单条新闻单独打标签，也不要用 `个人`、`生活碎片`、`奇葩` 这类含义模糊的标签。

## 周刊摘要

`description` 显示在列表页卡片上（为空时主题会截取正文第一段）。提交周刊前检查，为空就按内容补一句：

- 30 字以内，一句话，口吻贴近正文；不重复标题里的日期和周数。
- 优先写生活和片段里的事，字数还有余量再带一两条新闻。
- 用单引号包住，如 `description: '换小佩猫砂盆 MAX2，打卡寿司郎'`。

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

## 同步 Obsidian 面试训练文章

`src/content/posts/agent-interview/<YYYY-MM>/` 是 Obsidian vault 里 `Plan/better/<YYYY-MM>/` 的副本，源头在 vault（那边也是一个 git 仓库，不能移动目录，也不要用软链，线上构建读不到）。定期在仓库根目录执行，只同步日期目录下的 `.md`，README、题库配置、题目索引、prompts、精选都不同步：

```bash
SRC="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Plan/better"
rsync -a --include='20[0-9][0-9]-[0-9][0-9]/' --include='20[0-9][0-9]-[0-9][0-9]/*.md' --exclude='*' "$SRC/" src/content/posts/agent-interview/
```

- 单向 vault → 仓库，不带 `--delete`；vault 里删掉的文章，要手动删仓库里的副本。
- 不要直接改仓库里的副本，改动会在下次同步时被覆盖。
- 文章必须在 vault 里写好 `slug`、`title`、`published`（slug 格式 `ai-agent-interview-YYYY-MM-DD`），缺字段会让构建失败。
- 先加 `-n` 看一遍会同步哪些文件，再正式执行。

## 本地预览

`pnpm dev`，默认 http://127.0.0.1:4321/。
