#!/usr/bin/env python3
"""Prepare white-on-black ASCII avatar for the portrait SVG generator.
Run: python scripts/prep_ascii_avatar.py source-photo.png
"""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
import sys

base = Path(__file__).resolve().parent.parent
source = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "source-photo.png"
dest = Path(sys.argv[2]) if len(sys.argv) > 2 else base / "source-prepped.png"
with Image.open(source) as image:
    original = image.convert("L")
    # Detect the bright ASCII silhouette and crop with a generous margin.
    bbox = original.point(lambda v: 255 if v > 40 else 0).getbbox()
    if bbox:
        x0,y0,x1,y1 = bbox
        side = max(x1-x0, y1-y0) + 64
        cx,cy = (x0+x1)/2, (y0+y1)/2
        original = original.crop((round(cx-side/2), round(cy-side/2),round(cx+side/2),round(cy+side/2)))
    gray = ImageOps.invert(original)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    ImageEnhance.Contrast(gray).enhance(1.32).save(dest)
print(f"wrote {dest}")
