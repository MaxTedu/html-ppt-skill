# html-ppt — HTML PPT Studio

> An AI-powered workbench for generating professional HTML presentations.
>
> Forked and enhanced from [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill).
>
> **36 themes** · **15 full-deck templates** · **31 page layouts** · **47 animations**
> (27 CSS + 20 Canvas FX) · **Presenter mode** (pixel-perfect previews + speaker script + timer)
> · **AI image generation** (Doubao Seedream API)
>
> Pure static HTML/CSS/JS, zero build step.

**中文文档:** [README.zh-CN.md](README.zh-CN.md)

---

## 🎯 What is this

This is an **AI workbench project** — open it in Trae IDE (or any AI tool that supports AGENTS.md), and the AI will generate professional slide decks through natural language conversation.

**Core Pipeline**: `Understand Requirements → Pick Theme & Layouts → ⚠️ Confirm Plan → [🎨 Generate Images] → Scaffold Deck → Author Slides → Add Animations → Quality Review → Export PNG`

> Fork enhancements: added [AGENTS.md](AGENTS.md) as the AI entry point, AI image generation via Doubao API, and a `projects/` directory for organizing all generated content.

---

## ✨ What's New in This Fork

### 🤖 AGENTS.md — AI Project Entry

[AGENTS.md](AGENTS.md) is the entry point that tells AI agents how to work with this project:

- **Mandatory confirmation gate** — the AI must present a plan and get your approval before writing any files
- **Image generation gate** — submit an image plan for confirmation before any API calls
- **Complete workflow guidance**

### 🎨 AI Image Generation

Generate high-quality images via the Doubao Seedream API (OpenAI-compatible). Images are automatically downloaded to `projects/<deck>/images/` and ready to embed in slides.

```bash
python scripts/image_gen.py "prompt" -o projects/<deck>/images/ --size 2K --aspect-ratio 16:9
```

See [`references/image-gen.md`](references/image-gen.md) for the full resolution table and usage guide.

### 📁 projects/ Workspace

All generated decks now live in [`projects/`](projects/) instead of `examples/`. Each project has its own folder with cleanly organized image assets.

---

## 🎤 Presenter Mode

Press `S` on any deck to pop open a dedicated presenter window with four draggable, resizable **magnetic cards**: current slide preview, next slide preview, speaker script (逐字稿), and timer. Two windows stay in sync via `BroadcastChannel`.

![Presenter mode with 4 magnetic cards](docs/readme/presenter-mode.png)

**Why previews are pixel-perfect:** each card is an `<iframe>` that loads the same deck HTML with a `?preview=N` query param. The runtime detects this and renders only slide N with no chrome — so the preview uses the **same CSS, theme, fonts and viewport** as the audience view. Colors and layout are guaranteed identical.

**Smooth (no-reload) navigation:** on slide change, the presenter window sends `postMessage` to each iframe, which just toggles `.is-active` — **no reload, no flicker**.

**Speaker script rules:**
1. Prompt signals, not lines to read — bold keywords, separate transitions
2. 150–300 words per slide (~2–3 min/page pace)
3. Write conversationally, not like written prose

See [`references/presenter-mode.md`](references/presenter-mode.md), or use the ready-made `templates/full-decks/presenter-mode-reveal/` template.

---

## 📦 What's in the Box

| | Count | Where |
|---|---|---|
| 🎤 **Presenter mode** | Built-in | `S` key / `?preview=N` |
| 🎨 **Themes** | **36** | `assets/themes/*.css` |
| 📑 **Full-deck templates** | **15** | `templates/full-decks/<name>/` |
| 🧩 **Single-page layouts** | **31** | `templates/single-page/*.html` |
| ✨ **CSS animations** | **27** | `assets/animations/animations.css` |
| 💥 **Canvas FX animations** | **20** | `assets/animations/fx/*.js` |
| 🖼️ **Showcase decks** | 4 | `templates/*-showcase.html` |
| 🤖 **AI image generation** | New | `scripts/image_gen.py` |
| 📸 **Verification screenshots** | 56 | `scripts/verify-output/` |

### 36 Themes

`minimal-white` · `editorial-serif` · `soft-pastel` · `sharp-mono` · `arctic-cool` ·
`sunset-warm` · `catppuccin-latte` · `catppuccin-mocha` · `dracula` · `tokyo-night` ·
`nord` · `solarized-light` · `gruvbox-dark` · `rose-pine` · `neo-brutalism` ·
`glassmorphism` · `bauhaus` · `swiss-grid` · `terminal-green` · `xiaohongshu-white` ·
`rainbow-gradient` · `aurora` · `blueprint` · `memphis-pop` · `cyberpunk-neon` ·
`y2k-chrome` · `retro-tv` · `japanese-minimal` · `vaporwave` · `midcentury` ·
`corporate-clean` · `academic-paper` · `news-broadcast` · `pitch-deck-vc` ·
`magazine-bold` · `engineering-whiteprint`

![36 themes · 8 of them](docs/readme/themes.png)

Each theme is a pure CSS tokens file — swap one `<link>` to reskin the entire deck.

![15 full-deck templates](docs/readme/templates.png)

### 15 Full-deck templates

**8 extracted looks:** `xhs-white-editorial` · `graphify-dark-graph` · `knowledge-arch-blueprint` · `hermes-cyber-terminal` · `obsidian-claude-gradient` · `testing-safety-alert` · `xhs-pastel-card` · `dir-key-nav-minimal`

**7 scenario scaffolds:** `pitch-deck` · `product-launch` · `tech-sharing` · `weekly-report` · `xhs-post` (9-slide 3:4) · `course-module` · **`presenter-mode-reveal`** 🎤 (complete talk template with speaker scripts)

![31 single-page layouts](docs/readme/layouts.png)

### 31 Single-page layouts

cover · toc · section-divider · bullets · two-column · three-column ·
big-quote · stat-highlight · kpi-grid · table · code · diff · terminal ·
flow-diagram · timeline · roadmap · mindmap · comparison · pros-cons ·
todo-checklist · gantt · image-hero · image-grid · chart-bar · chart-line ·
chart-pie · chart-radar · arch-diagram · process-steps · cta · thanks

![47 animations — 27 CSS + 20 canvas FX](docs/readme/animations.png)

### 27 CSS animations + 20 Canvas FX

**CSS (lightweight)** — directional fades · `rise-in` · `zoom-pop` · `blur-in` · `glitch-in` · `typewriter` · `neon-glow` · `shimmer-sweep` · `gradient-flow` · `stagger-list` · `counter-up` · `path-draw` · `morph-shape` · `parallax-tilt` · `card-flip-3d` · `cube-rotate-3d` · `page-turn-3d` · `perspective-zoom` · `marquee-scroll` · `kenburns` · `ripple-reveal` · `spotlight` · …

**Canvas FX (cinematic)** — `particle-burst` · `confetti-cannon` · `firework` · `starfield` · `matrix-rain` · `knowledge-graph` · `neural-net` · `constellation` · `orbit-ring` · `galaxy-swirl` · `word-cascade` · `letter-explode` · `chain-react` · `magnetic-field` · `data-stream` · `gradient-blob` · `sparkle-trail` · `shockwave` · `typewriter-multi` · `counter-explosion`

---

## 🚀 Quick Start

### Method 1: AI-powered (recommended)

Open this project in Trae IDE. The AI will read [AGENTS.md](AGENTS.md) and [SKILL.md](SKILL.md), then you just tell it what you need:

> "Make me an 8-slide tech sharing deck with the tokyo-night theme"
> "Turn this outline into a pitch deck for investors"
> "Create a 小红书 social media post, 9 slides, soft pastel style"
> "Build a product launch deck with presenter mode and speaker notes"
> "Generate a cover image: futuristic smart city concept art"

The AI will confirm the plan with you before generating anything.

### Method 2: Manual

```bash
# Install Python deps (for AI image gen)
pip install openai python-dotenv requests

# Configure API key
# Edit .env and set your ARK_API_KEY

# Scaffold a new deck
./scripts/new-deck.sh my-talk

# Browse everything
open templates/theme-showcase.html         # all 36 themes
open templates/layout-showcase.html        # all 31 layouts
open templates/animation-showcase.html     # all 47 animations
open templates/full-decks-index.html       # all 15 full decks

# Generate images (optional)
python scripts/image_gen.py "futuristic city, cinematic" -o projects/my-talk/images/ --size 2K

# Render to PNG via headless Chrome
./scripts/render.sh projects/my-talk/index.html all
```

---

## ⌨️ Keyboard Cheat Sheet

```
← → Space PgUp PgDn Home End    navigate
F                                fullscreen
S                                presenter window (magnetic cards)
N                                notes drawer
R                                reset timer (in presenter window)
O                                slide overview grid
T                                cycle themes
A                                demo animation on current slide
#/N (URL)                        deep-link to slide N
?preview=N (URL)                 preview-only mode (single slide, no chrome)
```

---

## 📁 Project Structure

```
html-ppt-skill/
├── AGENTS.md                     AI entry point (new)
├── SKILL.md                      AgentSkill workflow definition
├── README.md                     this file
├── README.zh-CN.md               Chinese docs
├── .env                          API key config (new, gitignored)
├── .gitignore                    ignore rules (new)
│
├── references/                   detailed docs
│   ├── themes.md                 36 themes with when-to-use
│   ├── layouts.md                31 layout types
│   ├── animations.md             27 CSS + 20 FX catalog
│   ├── full-decks.md             15 full-deck templates
│   ├── presenter-mode.md         🎤 presenter mode guide
│   ├── image-gen.md              🤖 AI image gen guide (new)
│   └── authoring-guide.md        full workflow
│
├── assets/                       shared resources
│   ├── base.css                  tokens + primitives
│   ├── fonts.css                 webfont imports
│   ├── runtime.js                keyboard + presenter + overview
│   ├── themes/*.css              36 theme token files
│   └── animations/
│       ├── animations.css        27 named CSS animations
│       ├── fx-runtime.js         auto-init FX on slide enter
│       └── fx/*.js               20 canvas FX modules
│
├── templates/                    template files
│   ├── deck.html                 minimal starter
│   ├── theme-showcase.html       iframe-isolated theme tour
│   ├── layout-showcase.html      all 31 layouts
│   ├── animation-showcase.html   47 animation slides
│   ├── full-decks-index.html     15-deck gallery
│   ├── full-decks/<name>/        15 scoped multi-slide decks
│   └── single-page/*.html        31 layout files with demo data
│
├── scripts/                      tooling
│   ├── new-deck.sh               scaffold
│   ├── image_gen.py              🤖 AI image generation (new)
│   ├── render.sh                 headless Chrome → PNG
│   └── verify-output/            56 self-test screenshots
│
├── projects/                     user project workspace (new, replaces examples/)
│   └── demo-deck/                demo deck
│
└── docs/readme/                  README assets
```

---

## 🧠 Philosophy

- **Token-driven design system.** All colors, radii, shadows, fonts live in `assets/base.css` + the current theme. Change one variable, the whole deck reflows tastefully.
- **Iframe isolation for previews.** Theme/layout/deck showcases use `<iframe>` so every preview is a real, independent render.
- **Zero build.** Pure static HTML/CSS/JS. CDN only for webfonts, highlight.js and chart.js (optional).
- **AI safety gates.** Every write operation (file creation, API calls) goes through user confirmation.
- **Chinese + English first-class.** Noto Sans SC / Noto Serif SC pre-imported.

---

## 📜 License

MIT © 2026 lewis — original author [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)
