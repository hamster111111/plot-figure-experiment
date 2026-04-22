from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PRESERVE_DEST_FILES = {"index.html", ".nojekyll"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mirror a local source web directory into work/.")
    parser.add_argument(
        "--source",
        default=str(Path(__file__).resolve().parents[2] / "web"),
        help="Source directory to copy from.",
    )
    parser.add_argument(
        "--dest",
        default=str(Path(__file__).resolve().parents[1] / "work"),
        help="Destination publish directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = Path(args.source).resolve()
    dest = Path(args.dest).resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source}")

    dest.mkdir(parents=True, exist_ok=True)
    source_files = {
        path.relative_to(source)
        for path in source.rglob("*")
        if path.is_file()
    }

    for path in sorted(dest.rglob("*"), reverse=True):
        if not path.is_file():
            continue
        rel = path.relative_to(dest)
        if rel.as_posix() in PRESERVE_DEST_FILES:
            continue
        if rel not in source_files:
            path.unlink()

    for path in sorted(dest.rglob("*"), reverse=True):
        if path.is_dir() and path != dest and not any(path.iterdir()):
            path.rmdir()

    for rel in sorted(source_files):
        src_file = source / rel
        dest_file = dest / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)

    nojekyll = dest / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.write_text("", encoding="utf-8")

    print(f"Synced {len(source_files)} files from {source} to {dest}")


if __name__ == "__main__":
    main()
