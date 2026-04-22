from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import shutil
from pathlib import Path


PRESERVE_DEST_FILES = {"index.html", ".nojekyll"}
EXTERNAL_REF_PATTERN = re.compile(
    r'(?P<attr>src|href)=(?P<quote>["\'])(?P<url>\.\./[^"\']+)(?P=quote)'
)


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


def build_missing_asset_svg(label: str) -> str:
    safe_label = html.escape(label)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540" role="img" aria-label="Missing asset">
<rect width="960" height="540" fill="#0d1117"/>
<rect x="36" y="36" width="888" height="468" rx="18" fill="#161b22" stroke="#30363d"/>
<text x="480" y="240" fill="#e6edf3" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" text-anchor="middle">Asset not available in published site</text>
<text x="480" y="286" fill="#a7b0ba" font-family="Consolas, monospace" font-size="18" text-anchor="middle">{safe_label}</text>
</svg>
"""


def missing_asset_rel(url: str) -> Path:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return Path("assets") / "external" / "_missing" / f"{digest}.svg"


def collect_external_assets(
    source: Path,
    dest: Path,
    source_files: set[Path],
) -> tuple[dict[Path, str], dict[Path, Path], dict[Path, str]]:
    workspace_root = source.parent.resolve()
    rewritten_html: dict[Path, str] = {}
    mirrored_assets: dict[Path, Path] = {}
    placeholder_assets: dict[Path, str] = {}
    warned_refs: set[str] = set()

    for rel in sorted(source_files):
        if rel.suffix.lower() != ".html":
            continue

        src_file = source / rel
        dest_file = dest / rel
        content = src_file.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            url = match.group("url")
            resolved = (src_file.parent / Path(url)).resolve()
            fallback_label = "/".join(Path(url).parts[-2:])

            def placeholder_reference(message: str) -> str:
                if url not in warned_refs:
                    print(message)
                    warned_refs.add(url)
                dest_asset_rel = missing_asset_rel(url)
                placeholder_assets.setdefault(dest_asset_rel, build_missing_asset_svg(fallback_label))
                rewritten_url = Path(os.path.relpath(dest / dest_asset_rel, dest_file.parent)).as_posix()
                return f'{match.group("attr")}={match.group("quote")}{rewritten_url}{match.group("quote")}'

            try:
                external_rel = resolved.relative_to(workspace_root)
            except ValueError:
                return placeholder_reference(f"Skipping external reference outside workspace: {url}")

            if not resolved.exists() or not resolved.is_file():
                return placeholder_reference(f"Missing external asset: {resolved}")

            dest_asset_rel = Path("assets") / "external" / external_rel
            mirrored_assets[dest_asset_rel] = resolved
            rewritten_url = Path(os.path.relpath(dest / dest_asset_rel, dest_file.parent)).as_posix()
            return f'{match.group("attr")}={match.group("quote")}{rewritten_url}{match.group("quote")}'

        rewritten_html[rel] = EXTERNAL_REF_PATTERN.sub(replace, content)

    return rewritten_html, mirrored_assets, placeholder_assets


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
    rewritten_html, mirrored_assets, placeholder_assets = collect_external_assets(source, dest, source_files)
    expected_dest_files = source_files | set(mirrored_assets) | set(placeholder_assets)

    for path in sorted(dest.rglob("*"), reverse=True):
        if not path.is_file():
            continue
        rel = path.relative_to(dest)
        if rel.as_posix() in PRESERVE_DEST_FILES:
            continue
        if rel not in expected_dest_files:
            path.unlink()

    for path in sorted(dest.rglob("*"), reverse=True):
        if path.is_dir() and path != dest and not any(path.iterdir()):
            path.rmdir()

    for rel in sorted(source_files):
        src_file = source / rel
        dest_file = dest / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        if rel.suffix.lower() == ".html":
            dest_file.write_text(rewritten_html[rel], encoding="utf-8")
            continue
        shutil.copy2(src_file, dest_file)

    for rel, src_file in sorted(mirrored_assets.items()):
        dest_file = dest / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)

    for rel, content in sorted(placeholder_assets.items()):
        dest_file = dest / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(content, encoding="utf-8")

    nojekyll = dest / ".nojekyll"
    if not nojekyll.exists():
        nojekyll.write_text("", encoding="utf-8")

    print(
        f"Synced {len(source_files)} source files, mirrored {len(mirrored_assets)} external assets, "
        f"and generated {len(placeholder_assets)} placeholders "
        f"from {source} to {dest}"
    )


if __name__ == "__main__":
    main()
