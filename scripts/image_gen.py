#!/usr/bin/env python3
"""
html-ppt :: image_gen.py — generate images via Doubao Seedream API

Usage:
  python scripts/image_gen.py "prompt text" -o projects/my-deck/images/
  python scripts/image_gen.py "prompt text" -o projects/my-deck/images/ --size 1K --aspect-ratio 16:9

Environment:
  ARK_API_KEY — set in .env file at project root (loaded via python-dotenv)

Dependencies:
  pip install openai python-dotenv requests
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

RESOLUTION_TABLE = {
    "1K": {
        "1:1":  "2048x2048",
        "4:3":  "2304x1728",
        "3:4":  "1728x2304",
        "16:9": "2848x1600",
        "9:16": "1600x2848",
        "3:2":  "2496x1664",
        "2:3":  "1664x2496",
        "21:9": "3136x1344",
    },
    "2K": {
        "1:1":  "2048x2048",
        "4:3":  "2304x1728",
        "3:4":  "1728x2304",
        "16:9": "2848x1600",
        "9:16": "1600x2848",
        "3:2":  "2496x1664",
        "2:3":  "1664x2496",
        "21:9": "3136x1344",
    },
    "3K": {
        "1:1":  "3072x3072",
        "4:3":  "3456x2592",
        "3:4":  "2592x3456",
        "16:9": "4096x2304",
        "9:16": "2304x4096",
        "2:3":  "2496x3744",
        "3:2":  "3744x2496",
        "21:9": "4704x2016",
    },
    "4K": {
        "1:1":  "4096x4096",
        "3:4":  "3520x4704",
        "4:3":  "4704x3520",
        "16:9": "5504x3040",
        "9:16": "3040x5504",
        "2:3":  "3328x4992",
        "3:2":  "4992x3328",
        "21:9": "6240x2656",
    },
}

VALID_SIZES = ["1K", "2K", "3K", "4K"]
VALID_RATIOS = ["1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"]
DEFAULT_MODEL = "doubao-seedream-4-5-251128"


def get_resolution(size: str, aspect_ratio: str) -> str:
    if size not in RESOLUTION_TABLE:
        raise ValueError(f"Unknown size '{size}'. Valid: {VALID_SIZES}")
    if aspect_ratio not in RESOLUTION_TABLE[size]:
        raise ValueError(f"Unknown aspect ratio '{aspect_ratio}' for size {size}. Valid: {list(RESOLUTION_TABLE[size].keys())}")
    return RESOLUTION_TABLE[size][aspect_ratio]


def next_image_path(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = list(output_dir.glob("image_*.png")) + list(output_dir.glob("image_*.jpg")) + list(output_dir.glob("image_*.webp"))
    if not existing:
        return output_dir / "image_001.png"
    nums = []
    for p in existing:
        try:
            nums.append(int(p.stem.split("_")[1]))
        except (IndexError, ValueError):
            pass
    next_num = max(nums) + 1 if nums else 1
    return output_dir / f"image_{next_num:03d}.png"


def generate_image(
    prompt: str,
    output_dir: str,
    size: str = "2K",
    aspect_ratio: str = "16:9",
    model: str = DEFAULT_MODEL,
) -> str:
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("error: ARK_API_KEY not set. Please set it in .env file.", file=sys.stderr)
        sys.exit(1)

    resolution = get_resolution(size, aspect_ratio)
    out_path = next_image_path(Path(output_dir))

    print(f"model:      {model}")
    print(f"size/ratio: {size} / {aspect_ratio} → {resolution}")
    print(f"output:     {out_path}")
    print(f"prompt:     {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print("generating...", flush=True)

    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )

    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=resolution,
        response_format="url",
        extra_body={"watermark": True, "sequential_image_generation": "disabled"},
    )

    image_url = response.data[0].url
    print(f"url: {image_url}")

    r = requests.get(image_url, timeout=60)
    r.raise_for_status()

    out_path.write_bytes(r.content)
    file_size_kb = len(r.content) / 1024
    print(f"saved: {out_path} ({file_size_kb:.0f} KB)")

    rel = out_path.relative_to(PROJECT_ROOT).as_posix()
    print(f"relative: {rel}")

    return rel


def main():
    parser = argparse.ArgumentParser(
        description="Generate images via Doubao Seedream API for html-ppt decks"
    )
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument(
        "-o", "--output", default=".",
        help="Output directory (default: current dir; suggested: projects/<deck>/images/)"
    )
    parser.add_argument(
        "--size", default="2K", choices=VALID_SIZES,
        help="Resolution tier: 1K / 2K / 3K / 4K (default: 2K)"
    )
    parser.add_argument(
        "--aspect-ratio", default="16:9", choices=VALID_RATIOS,
        help="Aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"Model name (default: {DEFAULT_MODEL})"
    )

    args = parser.parse_args()
    generate_image(
        prompt=args.prompt,
        output_dir=args.output,
        size=args.size,
        aspect_ratio=args.aspect_ratio,
        model=args.model,
    )


if __name__ == "__main__":
    main()
