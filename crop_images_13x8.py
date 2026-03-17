from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def center_crop_to_ratio(image: Image.Image, ratio_w: float = 25.6, ratio_h: float = 16.0) -> Image.Image:
    """Center-crop an image to the target aspect ratio without resizing."""
    target_ratio = ratio_w / ratio_h
    width, height = image.size
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Image is too wide: crop left and right edges.
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        return image.crop((left, 0, left + new_width, height))

    if current_ratio < target_ratio:
        # Image is too tall: crop top and bottom edges.
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        return image.crop((0, top, width, top + new_height))

    return image


def resolve_source_dir(source_arg: Path) -> Path:
    """Resolve source folder robustly from common project locations."""
    script_dir = Path(__file__).resolve().parent
    candidates = [
        source_arg,
        Path.cwd() / source_arg,
        script_dir / source_arg,
        script_dir / "assets" / "images",
        Path.cwd() / "assets" / "images",
        script_dir / "images",
        Path.cwd() / "images",
    ]

    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists() and resolved.is_dir():
            return resolved

    searched = "\n".join(f" - {c.resolve()}" for c in candidates)
    raise FileNotFoundError(f"Source folder not found. Searched:\n{searched}")


def process_folder(source_dir: Path, output_dir: Path, ratio_w: float = 25.6, ratio_h: float = 16.0) -> tuple[int, int]:
    """Copy and crop all supported images from source_dir to output_dir."""
    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Source folder not found: {source_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for src_path in source_dir.rglob("*"):
        if not src_path.is_file() or src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        rel_path = src_path.relative_to(source_dir)
        dst_path = output_dir / rel_path
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with Image.open(src_path) as img:
                # Respect EXIF orientation before cropping.
                corrected = ImageOps.exif_transpose(img)
                cropped = center_crop_to_ratio(corrected, ratio_w, ratio_h)
                save_format = img.format if img.format else None
                cropped.save(dst_path, format=save_format)
                converted += 1
        except Exception as exc:
            skipped += 1
            print(f"Skipped {src_path}: {exc}")

    return converted, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy images to another folder and center-crop to 25.6:16 ratio."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("assets/images"),
        help="Source images folder (default: assets/images)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("images_25_6x16"),
        help="Output folder for cropped images (default: images_25_6x16)",
    )
    parser.add_argument("--ratio-w", type=float, default=25.6, help="Aspect ratio width (default: 25.6)")
    parser.add_argument("--ratio-h", type=float, default=16.0, help="Aspect ratio height (default: 16.0)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_dir = resolve_source_dir(args.source)
    output_dir = args.output.resolve()
    print(f"Using source: {source_dir}")
    print(f"Writing output: {output_dir}")

    converted, skipped = process_folder(source_dir, output_dir, args.ratio_w, args.ratio_h)
    print(f"Done. Converted: {converted}, Skipped: {skipped}")


if __name__ == "__main__":
    main()
