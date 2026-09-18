#!/usr/bin/env python3
"""Composite a transparent cover overlay over an untouched portrait."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--overlay", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.original.is_file():
        parser.error(f"original not found: {args.original}")
    if not args.overlay.is_file():
        parser.error(f"overlay not found: {args.overlay}")

    original_hash = sha256(args.original)
    with Image.open(args.original) as source, Image.open(args.overlay) as overlay:
        source_rgba = source.convert("RGBA")
        if overlay.mode not in ("RGBA", "LA") and "transparency" not in overlay.info:
            raise SystemExit("overlay must contain an alpha channel (RGBA/LA or transparency metadata)")
        overlay_rgba = overlay.convert("RGBA")
        if overlay_rgba.size != source_rgba.size:
            # The overlay must cover the complete base canvas. Resize it exactly;
            # centering a smaller overlay would leave the generated design trapped
            # in the middle of the portrait.
            overlay_rgba = overlay_rgba.resize(source_rgba.size, Image.Resampling.LANCZOS)
        result = Image.alpha_composite(source_rgba, overlay_rgba)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Keep the overlay as PNG, but make the flattened deliverable a normal JPG
    # when the requested output path ends in .jpg/.jpeg.
    if args.output.suffix.lower() in {".jpg", ".jpeg"}:
        flattened = result.convert("RGB")
        flattened.save(args.output, format="JPEG", quality=95, subsampling=0, optimize=False)
        output_mode = flattened.mode
        output_format = "JPEG"
    else:
        result.save(args.output, format="PNG", optimize=False)
        output_mode = result.mode
        output_format = "PNG"
    print(f"original: {args.original} {source_rgba.size} sha256={original_hash}")
    print(f"overlay:  {args.overlay} {overlay_rgba.size} mode={overlay.mode}")
    print(f"output:   {args.output} {result.size} mode={output_mode} format={output_format}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
