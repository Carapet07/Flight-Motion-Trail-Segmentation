#!/usr/bin/env python3
"""Group original and preprocessed GoPro videos by video type."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


VIDEO_GROUPS = {
    "TMPv.mp4": "TMPv",
    "TMPt.mp4": "TMPt",
    "TMPt_Multiplied.mp4": "Mult",
}


def sort_videos(dataset_dir: Path, dry_run: bool = False) -> tuple[int, int]:
    source_dir = dataset_dir / "GoPro"
    if not source_dir.is_dir():
        raise FileNotFoundError(f"GoPro directory not found: {source_dir}")

    recording_dirs = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_dir() and not path.name.startswith("._")
    )
    if not recording_dirs:
        raise RuntimeError(f"No recording folders found in {source_dir}")

    copied = 0
    skipped = 0

    for recording_dir in recording_dirs:
        videos = {
            **VIDEO_GROUPS,
            f"{recording_dir.name}.MP4": "Original",
        }

        for source_name, group_name in videos.items():
            source = recording_dir / source_name
            if not source.is_file():
                print(f"WARNING: missing {source}", flush=True)
                continue

            destination_dir = dataset_dir / group_name
            destination_name = (
                source_name
                if group_name == "Original"
                else f"{recording_dir.name}_{source_name}"
            )
            destination = destination_dir / destination_name

            if destination.exists():
                if destination.stat().st_size == source.stat().st_size:
                    print(f"SKIP  {destination}", flush=True)
                    skipped += 1
                    continue
                raise FileExistsError(
                    f"Refusing to overwrite a different file: {destination}"
                )

            print(f"COPY  {source} -> {destination}", flush=True)
            if not dry_run:
                destination_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            copied += 1

    return copied, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "dataset_dir",
        nargs="?",
        type=Path,
        default=Path("/Volumes/1TB/Dataset"),
        help="Dataset root containing GoPro (default: /Volumes/1TB/Dataset)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display planned copies without writing files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataset_dir = args.dataset_dir.expanduser().resolve()
    print(f"Dataset: {dataset_dir}", flush=True)
    copied, skipped = sort_videos(dataset_dir, dry_run=args.dry_run)
    action = "Would copy" if args.dry_run else "Copied"
    print(f"\n{action} {copied} video(s); skipped {skipped} existing video(s).")


if __name__ == "__main__":
    main()
