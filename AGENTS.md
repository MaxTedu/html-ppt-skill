# AGENTS.md

This file is the project entry point for AI agents. Before any PPT generation task, **you MUST first read [`SKILL.md`](SKILL.md)** — the authoritative workflow for content discovery, theme/layout selection, slide authoring, quality review, and export.

## Project Overview

HTML PPT Studio is an AI-driven static HTML presentation generation system. It converts user ideas/outlines/content into natively runnable HTML decks (zero build, pure HTML/CSS/JS) with real keyboard navigation, presenter mode, and theme switching.

**Core Pipeline**: `Understand Requirements → Pick Theme & Layouts → ⚠️ Confirm Slide Plan → [🎨 Confirm Image Plan if needed → Generate Images] → Scaffold Deck → Author Slides → Add Animations → Quality Review → Export PNG (optional)`

> **⚠️ BOTH CONFIRMATION GATES ARE MANDATORY.** Do NOT scaffold a deck file or write any slide HTML until the user has explicitly confirmed the slide plan. If the deck needs AI-generated images, create an image generation plan and get it confirmed separately before any API calls. See [Confirmation Gate](#confirmation-gate-mandatory) and [Image Generation](#image-generation-optional) below.

> Decks requiring speaker scripts (逐字稿): use the `presenter-mode-reveal` full-deck template and write 150-300 words per slide in `<aside class="notes">`.
>
> 小红书图文 (3:4 aspect ratio): use the `xhs-post` or `xhs-white-editorial` template. Render at 1242×1660 via `scripts/render.sh`.
>
> Post-creation iteration: whenever the user asks to tweak a slide ("改一下", "换个主题", "这个布局不好看"), read the current deck file, make targeted edits, and tell the user to refresh their browser. Use `T` to cycle themes and `S` to check speaker notes.

## Confirmation Gate (MANDATORY)

**Before writing a single line of slide HTML, you MUST present a plan to the user and get their explicit confirmation.** This gate covers three items — adapted from [`SKILL.md`](SKILL.md) "Before you author anything":

### Three items to confirm

1. **Content & audience.** Summarize what the deck is about, your proposed slide count, target audience (engineers / execs / 小红书 readers / students / VC), and language (Chinese / English / bilingual).

2. **Theme selection.** Recommend 2–3 themes from [`references/themes.md`](references/themes.md) based on audience + tone, and explain why each fits. If the user didn't specify, propose a default with a brief rationale.

   Quick mapping (see [`references/themes.md`](references/themes.md) for full catalog):
   - Business / investor pitch → `pitch-deck-vc`, `corporate-clean`, `swiss-grid`
   - Tech sharing / engineering → `tokyo-night`, `dracula`, `catppuccin-mocha`, `terminal-green`, `blueprint`
   - 小红书图文 → `xiaohongshu-white`, `soft-pastel`, `rainbow-gradient`, `magazine-bold`
   - Academic / report → `academic-paper`, `editorial-serif`, `minimal-white`
   - Edgy / launch → `cyberpunk-neon`, `vaporwave`, `y2k-chrome`, `neo-brutalism`

3. **Slide outline.** List every slide with its page number, proposed layout (from [`references/layouts.md`](references/layouts.md)), and a one-line summary of what content it will carry. Use this format:

   ```
   # 封面 — layout: cover — 标题 + 副标题 + 演讲者信息
   # 目录 — layout: toc — 三个章节导航
   # 章节过渡 — layout: section-divider — "第一章：背景"
   # 正文 — layout: two-column — 问题陈述 + 痛点数据
   # 数据页 — layout: kpi-grid — 四个核心指标
   # 正文 — layout: bullets — 解决方案三大要点
   # CTA — layout: cta — 行动号召
   # 感谢 — layout: thanks — 联系方式 + Q&A
   ```

   **Start from a full-deck template when possible.** If one of the 15 templates in [`templates/full-decks/`](templates/full-decks/) matches the user's scenario, propose using it as the scaffold and adapting from there.

### Confirmation protocol

Present the plan clearly, then **stop and wait for the user's response.** A good confirmation message looks like:

> 我准备这样来做这份 PPT：
>
> **内容/受众**：关于 XXX 的技术分享，预计 15 页，面向工程师，中文为主。
>
> **推荐主题**：
> - `tokyo-night`（推荐）— 深色蓝调，代码密集场景默认好看
> - `catppuccin-mocha` — 深色柔和，长时间观看不刺眼
> - `dracula` — 经典紫红，程序员熟悉
>
> **页面大纲**：
> 1. 封面 (cover) — XXX 技术分享
> 2. 目录 (toc) — 三个章节
> 3. 章节过渡 (section-divider) — 背景与动机
> 4. 正文 (bullets) — 当前痛点
> 5. 正文 (two-column) — 方案对比
> 6. 数据 (kpi-grid) — 关键指标
> 7. ...
>
> **模板**：建议用 `tech-sharing` 全 deck 模板打底。
>
> 可以的话我就开始了？

- **Do NOT proceed to scaffolding** until the user says "可以", "开始", "go ahead", or similar affirmative response.
- If the user proposes changes, revise only the affected parts of the plan and re-confirm. Do not restart from scratch.
- If the user provides very specific and detailed content upfront (e.g. a full outline with exact slide content), you may condense the confirmation to the three items above — but still present them and wait.

## Image Generation (Optional)

When slides need real images — cover hero images, product shots, concept illustrations, mood imagery — use the Doubao Seedream API via `scripts/image_gen.py`. Full guide in [`references/image-gen.md`](references/image-gen.md).

### Image Generation Gate

**Before calling the API, you MUST present an image generation plan and get user confirmation.** Format:

```
## 图片生成计划

| # | 文件名 | Prompt | 尺寸 | 比例 | 用途 |
|---|--------|--------|------|------|------|
| 1 | image_001.png | 未来智慧城市，飞行汽车... | 2K | 16:9 | 封面主视觉 |
| 2 | image_002.png | 微服务架构，信息图风格... | 2K | 16:9 | 第5页架构图 |
| 3 | image_003.png | 人物剪影，数据流动... | 1K | 3:4 | 小红书用户画像 |
```

Wait for the user's OK before running the script.

### Quick usage

```bash
python scripts/image_gen.py "未来城市，电影大片风格..." -o projects/<deck>/images/ --size 2K --aspect-ratio 16:9
```

Images are auto-named sequentially (`image_001.png`, `image_002.png`, ...) and saved to `projects/<deck>/images/`. Reference them in HTML with relative paths:

```html
<img src="images/image_001.png" alt="未来城市" style="...object-fit:cover...">
```

Resolution reference: `16:9` (widescreen slide), `4:3` (classic), `3:4` (小红书 portrait). See [`references/image-gen.md`](references/image-gen.md) for the full resolution table.

## Execution Requirements

- **ALWAYS** read [`SKILL.md`](SKILL.md) before starting a PPT task.
- Read [`references/themes.md`](references/themes.md) to select an appropriate theme based on audience and tone.
- Read [`references/layouts.md`](references/layouts.md) to map each outline item to a layout.
- Read [`references/animations.md`](references/animations.md) sparingly — only when adding entry effects or canvas FX.
- If the user mentions **演讲 / 分享 / 逐字稿 / speaker notes**, read [`references/presenter-mode.md`](references/presenter-mode.md) and use the `presenter-mode-reveal` full-deck template.
- If the deck needs **AI-generated images** (cover hero, product shots, illustrations), read [`references/image-gen.md`](references/image-gen.md) and create an image generation plan for user confirmation before calling the API.
- For a full step-by-step walkthrough, read [`references/authoring-guide.md`](references/authoring-guide.md).
- Technical constraints and naming conventions live in [`SKILL.md`](SKILL.md) under "Authoring rules".
- Theme/icon/template details live in their respective `references/` files and `templates/` directories.

## Compatibility Boundary

- This project is a **static HTML deck generation workspace**, not an app or service scaffold. All output is self-contained HTML files.
- Do NOT assume build tools (webpack, vite, npm), frameworks (React, Vue), or backend services. The only external dependencies are CDN webfonts (Google Fonts) and optional chart.js / highlight.js.
- Do NOT invent new color values — always use CSS variables (tokens) defined in `assets/base.css` and overridden by themes.
- Do NOT modify `assets/base.css`, `assets/runtime.js`, or existing theme/layout/template files unless explicitly asked.
- On conflict with a generic coding skill, prioritize [`SKILL.md`](SKILL.md) and this file inside this project.

## Command Quick Reference

Convenience summary only — full workflow in [`SKILL.md`](SKILL.md).

```bash
# Scaffold a new deck from the starter template
./scripts/new-deck.sh <deck-name> projects

# AI image generation via Doubao Seedream (requires ARK_API_KEY in .env)
python scripts/image_gen.py "prompt" -o projects/<deck>/images/ --size 2K --aspect-ratio 16:9

# Render slides to PNG (requires Chrome/Chromium)
./scripts/render.sh <path/to/index.html>                    # single slide
./scripts/render.sh <path/to/index.html> <N>                # N slides
./scripts/render.sh <path/to/index.html> all                 # auto-detect slide count
./scripts/render.sh <path/to/index.html> <N> <output-dir>   # custom output dir
```

## Core Directories

- [`SKILL.md`](SKILL.md) — main workflow authority and authoring rules.
- [`assets/base.css`](assets/base.css) — design system tokens and primitive components. Never edit per-deck.
- [`assets/runtime.js`](assets/runtime.js) — keyboard navigation, presenter mode (`S`), theme cycling (`T`), overview grid (`O`), notes drawer (`N`).
- [`assets/themes/`](assets/themes/) — 36 theme CSS files (each ~100-200 lines overriding tokens).
- [`assets/animations/`](assets/animations/) — 27 CSS entry animations + 20 canvas FX modules + fx runtime.
- [`assets/fonts.css`](assets/fonts.css) — Google Fonts CDN imports (Inter, Noto Sans SC, Noto Serif SC, etc.).
- [`templates/deck.html`](templates/deck.html) — minimal 6-slide starter template for scaffolding.
- [`templates/single-page/`](templates/single-page/) — 31 individual layout HTML files with demo data.
- [`templates/full-decks/`](templates/full-decks/) — 15 complete multi-slide deck templates.
- [`references/`](references/) — detailed catalogs for themes, layouts, animations, full-decks, presenter mode, image generation, and authoring guide.
- [`projects/`](projects/) — user project workspace (all generated decks go here).
- [`scripts/`](scripts/) — scaffolding (`new-deck.sh`), image generation (`image_gen.py`), and PNG export (`render.sh`).
- [`.env`](.env) — API key configuration for image generation (never commit to git, listed in `.gitignore`).
