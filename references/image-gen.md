# Image Generation Guide

How to generate AI images via Doubao Seedream API and embed them into html-ppt slides.

## Overview

When a slide deck needs real images — cover hero images, product shots, concept illustrations, mood imagery — use `scripts/image_gen.py` to generate them via Doubao Seedream API, then reference the downloaded local files in your HTML.

**Important**: Do NOT generate images automatically during slide authoring. First create an **Image Generation Plan** (see below), present it to the user for confirmation, then run the script one image at a time.

## Prerequisites

```bash
pip install openai python-dotenv requests
```

Set your API key in the `.env` file at the project root:

```
ARK_API_KEY=fxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Get your key at: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

## Resolution & Aspect Ratio Reference

| Size | Aspect Ratio | Pixel Dimensions | Slide Use Case |
|------|-------------|------------------|----------------|
| **1K** | 1:1 | 2048×2048 | Square avatars, profile images |
| | 4:3 | 2304×1728 | Classic slide ratio |
| | 3:4 | 1728×2304 | 小红书 portrait images |
| | 16:9 | 2848×1600 | **Standard widescreen slide** ← default |
| | 9:16 | 1600×2848 | Phone wallpaper / vertical slides |
| | 3:2 | 2496×1664 | Photo-friendly ratio |
| | 2:3 | 1664×2496 | Portrait photos |
| | 21:9 | 3136×1344 | Ultrawide banner |
| **2K** | 1:1 | 2048×2048 | High-res square |
| | 4:3 | 2304×1728 | High-res classic |
| | 3:4 | 1728×2304 | High-res portrait |
| | 16:9 | 2848×1600 | **High-res widescreen** ← recommended |
| | 9:16 | 1600×2848 | High-res vertical |
| | 3:2 | 2496×1664 | High-res photo |
| | 2:3 | 1664×2496 | High-res portrait photo |
| | 21:9 | 3136×1344 | High-res ultrawide |
| **3K** | 1:1 | 3072×3072 | Premium square |
| | 4:3 | 3456×2592 | Premium classic |
| | 3:4 | 2592×3456 | Premium portrait |
| | 16:9 | 4096×2304 | **Premium widescreen** |
| | 9:16 | 2304×4096 | Premium vertical |
| | 2:3 | 2496×3744 | Premium portrait photo |
| | 3:2 | 3744×2496 | Premium photo |
| | 21:9 | 4704×2016 | Premium ultrawide |
| **4K** | 1:1 | 4096×4096 | Ultra-high-res square |
| | 3:4 | 3520×4704 | Ultra-high-res portrait |
| | 4:3 | 4704×3520 | Ultra-high-res classic |
| | 16:9 | 5504×3040 | **Ultra-high-res widescreen** |
| | 9:16 | 3040×5504 | Ultra-high-res vertical |
| | 2:3 | 3328×4992 | Ultra-high-res portrait photo |
| | 3:2 | 4992×3328 | Ultra-high-res photo |
| | 21:9 | 6240×2656 | Ultra-high-res ultrawide |

**Recommendation for slides**: Use `--size 2K --aspect-ratio 16:9` (2848×1600) for most decks. Bump to `4K` only for print-quality exports.

## Image Generation Plan (MANDATORY before generation)

Before running `image_gen.py`, create an **Image Generation Plan** and present it to the user for confirmation. Format:

```
## 图片生成计划

| # | 文件名 | API Prompt | 尺寸 | 比例 | 用途 (幻灯片页面) |
|---|---|--------|------|------|------|
| 1 | image_001.png | ... | 2K | 16:9 | 封面 — 未来城市概念图 |
| 2 | image_002.png | ... | 2K | 16:9 | 第5页 — 产品架构示意图 |
| 3 | image_003.png | ... | 1K | 3:4 | 第8页 — 用户画像插图 (小红书) |
```

### Prompt writing tips

- Write in **Chinese** for best results with Seedream
- Include style keywords: "电影大片", "oc渲染", "光线追踪", "超现实主义", "极简", "扁平化", "3D渲染"
- Include composition keywords: "广角透视", "景深", "动态模糊"
- Include color direction: "深蓝", "暖色调", "对比色", "莫兰迪色系"
- For charts/diagrams: "信息图", "数据可视化", "简洁商务"
- Negative prompt (avoid): "不要文字", "不要水印"

Example prompt:
```
未来智慧城市，空中穿梭的飞行汽车，玻璃幕墙摩天大楼，全息投影广告牌，
黄昏暖光，电影大片，oc渲染，光线追踪，景深，广角透视，超现实主义，
强视觉冲击力，蓝色与金色对比
```

## Script Usage

```bash
# Single image generation
python scripts/image_gen.py "未来城市概念图，电影大片，oc渲染..." \
  -o projects/my-deck/images/ \
  --size 2K \
  --aspect-ratio 16:9

# The script outputs the relative path:
# projects/my-deck/images/image_001.png
```

### Parameters

| Arg | Default | Description |
|-----|---------|-------------|
| `prompt` | required | Image generation prompt (Chinese recommended) |
| `-o` / `--output` | `.` | Output directory (use `projects/<deck>/images/`) |
| `--size` | `2K` | Resolution tier: `1K` / `2K` / `3K` / `4K` |
| `--aspect-ratio` | `16:9` | Aspect ratio (see table above) |
| `--model` | `doubao-seedream-4-5-251128` | Model name |

### File naming

Images are auto-named sequentially: `image_001.png`, `image_002.png`, etc. The script scans existing files in the output directory to avoid overwrites.

## Embedding Images in HTML

After generating images, reference them with relative paths in your slide HTML:

### Image Hero (full-bleed background)

```html
<section class="slide" data-title="Cover">
  <div class="hero">
    <img src="images/image_001.png" alt="未来城市" class="hero-bg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:var(--radius-lg)">
    <div class="overlay" style="position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(10,12,20,.7))"></div>
    <div class="caption" style="position:absolute;bottom:48px;left:56px;right:56px;color:#fff;z-index:2">
      <h1 class="h1">未来城市构想</h1>
      <p class="lede">智慧城市 2.0 技术白皮书</p>
    </div>
  </div>
</section>
```

### Image Grid (bento gallery)

```html
<section class="slide" data-title="Gallery">
  <p class="kicker">Gallery</p>
  <h2 class="h2">项目展示</h2>
  <div class="grid g3">
    <div class="card"><img src="images/image_001.png" alt="项目A" style="width:100%;height:100%;object-fit:cover;border-radius:var(--radius)"></div>
    <div class="card"><img src="images/image_002.png" alt="项目B" style="width:100%;height:100%;object-fit:cover;border-radius:var(--radius)"></div>
    <div class="card"><img src="images/image_003.png" alt="项目C" style="width:100%;height:100%;object-fit:cover;border-radius:var(--radius)"></div>
  </div>
</section>
```

### Card with image

```html
<div class="card card-soft">
  <img src="images/image_001.png" alt="示意图" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:var(--radius) var(--radius) 0 0">
  <div style="padding:var(--space-m)">
    <h4 class="h4">Feature Title</h4>
    <p>Description here.</p>
  </div>
</div>
```

## Workflow Integration

The image generation step fits into the core pipeline as an optional phase:

```
Understand Requirements → Pick Theme & Layouts
  → ⚠️ Confirm Slide Plan with User
    → ⚠️ Confirm Image Generation Plan with User (if images needed)
      → Generate Images → Scaffold Deck → Author Slides → ...
```

### When to propose image generation

Propose generating images when slides contain:

1. **Cover/hero** — a strong visual first impression
2. **Product showcase** — showing a product, device, or physical object
3. **Concept illustration** — abstract ideas that benefit from visual metaphor
4. **Mood/atmosphere** — setting emotional tone (section dividers, CTA)
5. **小红书图文** — portrait images for social media style decks

### When NOT to generate images

Skip image generation when:

- The deck is data-heavy (charts, tables, code)
- The existing CSS gradients in `image-hero` / `image-grid` layouts suffice
- The user explicitly prefers a text-only or minimal style
- The content is purely technical/architectural (use `blueprint` / `terminal-green` themes instead)

## Troubleshooting

- **ARK_API_KEY not set**: ensure `.env` file exists at project root with `ARK_API_KEY=...`
- **Resolution not supported for size**: check the table above for valid size × ratio combinations
- **Image download fails**: the URL from Seedream expires after some time; re-run immediately after generation
- **Image too large/small on slide**: use `object-fit: cover` for hero images, set explicit `aspect-ratio` for grid items
