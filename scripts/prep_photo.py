#!/usr/bin/env python3
"""Prepare a portrait for ASCII conversion:

Pipeline:
1. Remove background using rembg
2. Composite subject onto white
3. Improve local contrast using OpenCV CLAHE
4. Convert to grayscale and save as source-prepped.png

Usage:
    python scripts/prep_photo.py source-photo.jpg
"""
import argparse
import io
import os
os.environ["U2NET_HOME"] = os.path.join(os.getcwd(), ".u2net")
from pathlib import Path

try:
    from rembg import remove
except Exception as e:
    raise RuntimeError("rembg is required. Install with: pip install rembg") from e

from PIL import Image
import numpy as np
import cv2


def prep_photo(input_path: str, output_path: str, clip_limit: float = 3.0, tile_grid: int = 8):
    inp = Path(input_path)
    if not inp.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Load source image and ensure RGBA
    with Image.open(inp) as im:
        im = im.convert("RGBA")

        # Remove background (rembg works on bytes)
        bio = io.BytesIO()
        im.save(bio, format="PNG")
        bio.seek(0)
        out_bytes = remove(bio.read())

        # Open rembg output and ensure RGBA
        out_img = Image.open(io.BytesIO(out_bytes)).convert("RGBA")

        # Composite onto white background to avoid transparent areas turning black
        bg = Image.new("RGBA", out_img.size, (255, 255, 255, 255))
        bg.paste(out_img, (0, 0), out_img)

        # Convert to RGB then to grayscale via OpenCV for CLAHE
        rgb = bg.convert("RGB")
        arr = np.array(rgb)
        # Convert RGB -> BGR for OpenCV
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE (local contrast enhancement)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid, tile_grid))
        cl = clahe.apply(gray)

        # Optional slight Gaussian blur could be applied here, but keep crisp for ASCII

        # Convert back to PIL and save as PNG (grayscale)
        out_pil = Image.fromarray(cl)
        out_pil = out_pil.convert("L")
        out_pil.save(output_path)


def main():
    parser = argparse.ArgumentParser(description="Prepare a portrait for ASCII conversion")
    parser.add_argument("input", help="Path to source photo (JPEG/PNG)")
    parser.add_argument("--output", default=os.path.join(os.getcwd(), "source-prepped.png"), help="Output PNG path")
    parser.add_argument("--clip", type=float, default=3.0, help="CLAHE clipLimit (default: 3.0)")
    parser.add_argument("--tile", type=int, default=8, help="CLAHE tileGridSize (default: 8)")
    args = parser.parse_args()

    print(f"Preparing photo: {args.input} -> {args.output}")
    prep_photo(args.input, args.output, clip_limit=args.clip, tile_grid=args.tile)
    print(f"Saved prepped image: {args.output}")


if __name__ == "__main__":
    main()
