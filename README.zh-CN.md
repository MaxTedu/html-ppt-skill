# html-ppt · HTML PPT 工作室

> 一款让 AI 直接生成专业级 HTML 演示文稿的工作台。
>
> 基于 [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) 扩展增强。
>
> **36 套主题** · **15 套完整 deck 模板** · **31 种页面布局** · **47 个动效**
> (27 CSS + 20 Canvas FX) · **演讲者模式**（像素级完美预览 + 逐字稿提词器 + 计时器）
> · **AI 图片生成**（豆包 Seedream API 驱动）
>
> 纯静态 HTML/CSS/JS，无需构建。

**English docs:** [README.md](README.md)

---

## 🎯 这是什么

这是一个 **AI 工作台项目** —— 你可以在 Trae IDE（或其他支持 AGENTS.md 的 AI 工具）中直接打开这个项目，通过与 AI 对话来生成专业幻灯片。

**核心流程**：`理解需求 → 选主题/布局 → 确认方案 → [生成图片] → 搭架子 → 写页面 → 加动效 → 审核 → 导出 PNG`

> 与原始项目的区别：本 fork 新增了 [AGENTS.md](AGENTS.md) 作为 AI 入口文件，加入了 AI 图片生成能力（豆包 API），并将所有生成内容统一存放在 `projects/` 目录下。

---

## ✨ 新增特性

### 🤖 AGENTS.md — AI 项目入口

[AGENTS.md](AGENTS.md) 是本项目的 AI Agent 入口文件。当 AI 打开这个项目时，会先读取它来理解工作流程，包括：

- **强制确认闸门** — 写任何文件前都必须先提交方案给用户确认
- **图片生成计划** — 调用 API 前先提交图片清单等待确认
- **完整的工作流水线**指引

### 🎨 AI 图片生成

通过豆包 Seedream API（兼容 OpenAI 协议）生成高质量配图，自动下载到 `projects/<deck>/images/` 并嵌入幻灯片。

```bash
python scripts/image_gen.py "prompt" -o projects/<deck>/images/ --size 2K --aspect-ratio 16:9
```

详见 [`references/image-gen.md`](references/image-gen.md)（含完整分辨率对照表）。

### 📁 projects/ 项目工作区

所有生成的幻灯片统一存放在 [`projects/`](projects/) 目录下，替代原来的 `examples/`。每个项目独立文件夹，图片资源组织清晰。

---

## 🎤 演讲者模式

在任何 deck 里按 `S` 键，弹出一个独立的演讲者窗口，包含 4 个**可拖拽、可调整大小的磁吸卡片**：当前页预览、下一页预览、逐字稿、计时器。两个窗口通过 `BroadcastChannel` 双向同步翻页。

![演讲者模式 · 4 个磁吸卡片](docs/readme/presenter-mode.png)

**为什么预览是像素级完美的：** 每个卡片是一个 `<iframe>`，加载的是**同一份 deck HTML 文件**，只是 URL 多了 `?preview=N` 参数。runtime 检测到这个参数后，只渲染第 N 页并隐藏所有 chrome —— 所以预览使用**和观众视图完全相同的 CSS、主题、字体、viewport**，颜色和排版保证 100% 一致。

**丝滑翻页（零闪烁）：** 翻页时演讲者窗口通过 `postMessage` 通知 iframe，iframe 只是切换 `.is-active` class —— **不重新加载、不白屏、不闪烁**。

**逐字稿 3 条铁律：**
1. **提示信号，不是讲稿** — 关键词加粗，过渡句独立成段
2. **每页 150–300 字** — 约 2–3 分钟/页的节奏
3. **用口语，不用书面语** — "所以" 不是 "因此"，"这个" 不是 "该"

详见 [`references/presenter-mode.md`](references/presenter-mode.md)，或直接复制 `templates/full-decks/presenter-mode-reveal/` 这个现成模板。

---

## 📦 资源一览

| | 数量 | 位置 |
|---|---|---|
| 🎤 **演讲者模式** | 内置 | `S` 键 / `?preview=N` |
| 🎨 **主题** | **36** | `assets/themes/*.css` |
| 📑 **完整 deck 模板** | **15** | `templates/full-decks/<name>/` |
| 🧩 **单页布局** | **31** | `templates/single-page/*.html` |
| ✨ **CSS 动画** | **27** | `assets/animations/animations.css` |
| 💥 **Canvas FX 动画** | **20** | `assets/animations/fx/*.js` |
| 🖼️ **Showcase deck** | 4 | `templates/*-showcase.html` |
| 🤖 **AI 图片生成** | 新增 | `scripts/image_gen.py` |
| 📸 **验证截图** | 56 | `scripts/verify-output/` |

### 36 套主题

`minimal-white` · `editorial-serif` · `soft-pastel` · `sharp-mono` · `arctic-cool` ·
`sunset-warm` · `catppuccin-latte` · `catppuccin-mocha` · `dracula` · `tokyo-night` ·
`nord` · `solarized-light` · `gruvbox-dark` · `rose-pine` · `neo-brutalism` ·
`glassmorphism` · `bauhaus` · `swiss-grid` · `terminal-green` · `xiaohongshu-white` ·
`rainbow-gradient` · `aurora` · `blueprint` · `memphis-pop` · `cyberpunk-neon` ·
`y2k-chrome` · `retro-tv` · `japanese-minimal` · `vaporwave` · `midcentury` ·
`corporate-clean` · `academic-paper` · `news-broadcast` · `pitch-deck-vc` ·
`magazine-bold` · `engineering-whiteprint`

![36 主题 · 其中 8 个](docs/readme/themes.png)

每个主题都是一份纯 CSS token 文件 —— 只需要换一行 `<link>` 就能给整份 deck 换皮。

![15 套完整 deck 模板](docs/readme/templates.png)

### 15 套完整 deck 模板

**8 个提炼款：** `xhs-white-editorial` · `graphify-dark-graph` · `knowledge-arch-blueprint` · `hermes-cyber-terminal` · `obsidian-claude-gradient` · `testing-safety-alert` · `xhs-pastel-card` · `dir-key-nav-minimal`

**7 个场景款：** `pitch-deck`（投资人 pitch）· `product-launch`（产品发布会）· `tech-sharing`（技术分享）· `weekly-report`（周报）· `xhs-post`（小红书图文）· `course-module`（教学模块）· **`presenter-mode-reveal`** 🎤（带逐字稿的完整分享模板）

![31 种单页布局](docs/readme/layouts.png)

### 31 种单页布局

cover · toc · section-divider · bullets · two-column · three-column ·
big-quote · stat-highlight · kpi-grid · table · code · diff · terminal ·
flow-diagram · timeline · roadmap · mindmap · comparison · pros-cons ·
todo-checklist · gantt · image-hero · image-grid · chart-bar · chart-line ·
chart-pie · chart-radar · arch-diagram · process-steps · cta · thanks

![47 个动效 · 27 CSS + 20 Canvas FX](docs/readme/animations.png)

### 27 个 CSS 动画 + 20 个 Canvas FX

**CSS 动画（轻量）** — 方向性淡入 · `rise-in` · `zoom-pop` · `blur-in` · `glitch-in` · `typewriter` · `neon-glow` · `shimmer-sweep` · `gradient-flow` · `stagger-list` · `counter-up` · `path-draw` · `morph-shape` · `parallax-tilt` · `card-flip-3d` · `cube-rotate-3d` · `page-turn-3d` · `perspective-zoom` · `marquee-scroll` · `kenburns` · `ripple-reveal` · `spotlight` · …

**Canvas FX（电影级）** — `particle-burst`（粒子爆发）· `confetti-cannon`（彩带）· `firework`（烟花）· `starfield`（星空）· `matrix-rain`（代码雨）· `knowledge-graph`（力导向知识图谱）· `neural-net`（神经网络脉冲）· `constellation`（星座连线）· `orbit-ring`（轨道环）· `galaxy-swirl`（星系漩涡）· `word-cascade` · `letter-explode` · `chain-react` · `magnetic-field` · `data-stream` · `gradient-blob` · `sparkle-trail` · `shockwave` · `typewriter-multi` · `counter-explosion`

---

## 🚀 快速开始

### 方式一：AI 对话生成（推荐）

在 Trae IDE 中打开本项目，AI 会自动读取 [AGENTS.md](AGENTS.md) 和 [SKILL.md](SKILL.md)，然后你只需告诉它需求：

> "做一份 8 页的技术分享 slides，用 tokyo-night 主题"
> "把这段 outline 变成投资人 pitch deck"
> "做一个小红书图文，9 张，白底柔和风"
> "做一份带演讲者模式的产品分享，要有逐字稿"
> "帮我生成一张封面的配图：未来城市概念图"

AI 会先和你确认方案，再生成代码。

### 方式二：手动操作

```bash
# 安装 Python 依赖（AI 图片生成用）
pip install openai python-dotenv requests

# 配置 API 密钥
# 编辑 .env 文件，填入你的 ARK_API_KEY

# 从 base 模板新建一个 deck
./scripts/new-deck.sh my-talk

# 浏览所有内容
open templates/theme-showcase.html         # 全部 36 主题
open templates/layout-showcase.html        # 全部 31 布局
open templates/animation-showcase.html     # 全部 47 动效
open templates/full-decks-index.html       # 全部 15 个完整 deck

# 生成配图（可选）
python scripts/image_gen.py "未来城市，电影大片风格" -o projects/my-talk/images/ --size 2K

# 用 headless Chrome 导出 PNG
./scripts/render.sh projects/my-talk/index.html all
```

---

## ⌨️ 键盘快捷键

```
← → Space PgUp PgDn Home End    翻页
F                                全屏
S                                演讲者窗口（磁吸卡片模式）
N                                notes 抽屉
R                                重置计时器（演讲者窗口内）
O                                slide 总览网格
T                                切换主题
A                                在当前 slide 循环演示动画
#/N (URL)                        深链到第 N 页
?preview=N (URL)                 预览模式（单页，无 chrome）
```

---

## 📁 项目结构

```
html-ppt-skill/
├── AGENTS.md                     AI 入口文件（新增）
├── SKILL.md                      AgentSkill 工作流定义
├── README.md                     英文 README
├── README.zh-CN.md               本文件
├── .env                          API 密钥配置（新增，不提交 git）
├── .gitignore                    忽略规则（新增）
│
├── references/                   详细文档
│   ├── themes.md                 36 主题 + 使用场景
│   ├── layouts.md                31 布局
│   ├── animations.md             27 CSS + 20 FX 目录
│   ├── full-decks.md             15 完整 deck 模板
│   ├── presenter-mode.md         🎤 演讲者模式 + 逐字稿指南
│   ├── image-gen.md              🤖 AI 图片生成指南（新增）
│   └── authoring-guide.md        完整工作流
│
├── assets/
│   ├── base.css                  共享 tokens + 基础组件
│   ├── fonts.css                 web 字体引入
│   ├── runtime.js                键盘导航 + 演讲者模式 + 总览
│   ├── themes/*.css              36 主题 token 文件
│   └── animations/
│       ├── animations.css        27 个命名 CSS 动画
│       ├── fx-runtime.js         进入 slide 自动初始化 FX
│       └── fx/*.js               20 个 Canvas FX 模块
│
├── templates/
│   ├── deck.html                 最小起步模板
│   ├── theme-showcase.html       iframe 隔离的主题 tour
│   ├── layout-showcase.html      全部 31 布局
│   ├── animation-showcase.html   47 动画 slide
│   ├── full-decks-index.html     15 deck gallery
│   ├── full-decks/<name>/        15 个 scoped 多页 deck 模板
│   └── single-page/*.html        31 个布局文件（带示例数据）
│
├── scripts/
│   ├── new-deck.sh               脚手架
│   ├── image_gen.py              🤖 AI 图片生成（新增）
│   ├── render.sh                 headless Chrome → PNG
│   └── verify-output/            56 张自测截图
│
├── projects/                     项目工作区（新增，替代 examples/）
│   └── demo-deck/                示例 deck
│
└── docs/readme/                  README 配图资源
```

---

## 🧠 设计理念

- **Token 驱动的设计系统。** 所有颜色、圆角、阴影、字体都在 `assets/base.css` + 当前主题里。改一个变量，整份 deck 优雅地重排。
- **Iframe 隔离预览。** 主题/布局/deck showcase 都用 `<iframe>`，确保每个预览都是真实、独立的渲染结果。
- **零构建。** 纯静态 HTML/CSS/JS。只有 webfont / highlight.js / chart.js (可选) 走 CDN。
- **AI 安全闸门。** 所有生成操作（写文件、调 API）前都经过用户确认，确保方向正确。
- **中英双语一等公民。** 预导入了 Noto Sans SC / Noto Serif SC。

---

## 📜 协议

MIT © 2026 lewis — 原始作者 [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)
