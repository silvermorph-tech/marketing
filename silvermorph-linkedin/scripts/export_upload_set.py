#!/usr/bin/env python3
"""Make the final upload set for a draft: numbered files in upload order, LinkedIn-safe formats.

  python3 scripts/export_upload_set.py drafts/2026-10-23-ccsv poster.png materials/booth-1.webp materials/booth-2.webp

Writes drafts/<draft>/upload/1-<name>, 2-<name>, ... Files are only format-converted (webp/heic to JPG), never cropped or edited.
Needs Pillow (pip install pillow); PNG and JPG inputs are copied as they are.
"""
import shutil
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    draft = Path(sys.argv[1])
    out = draft / "upload"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir()
    for i, name in enumerate(sys.argv[2:], 1):
        src = draft / name
        if src.suffix.lower() in (".png", ".jpg", ".jpeg"):
            dst = out / f"{i}-{src.stem}{src.suffix.lower()}"
            shutil.copy2(src, dst)
        else:
            from PIL import Image
            dst = out / f"{i}-{src.stem}.jpg"
            Image.open(src).convert("RGB").save(dst, quality=95)
        print(dst.resolve())


if __name__ == "__main__":
    main()
