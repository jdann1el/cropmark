#!/usr/bin/env python3
"""Copy user-held study images into an ignored local cache; never downloads anything."""

import argparse
import json
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]
REFS_PATH = SKILL_ROOT / "library" / "refs.json"
CACHE_ROOT = REPO_ROOT / "refs-cache"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
DEFAULT_IMPORT = Path("/workspace/cropmark-refs")


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--import", dest="import_dir", nargs="?", const=str(DEFAULT_IMPORT), metavar="DIR")
    mode.add_argument("--status", action="store_true")
    mode.add_argument("--open", dest="open_id", metavar="ID")
    p.add_argument("--ref", metavar="ID", help="limit --import or --status to one reference")
    return p


def load_refs():
    with REFS_PATH.open(encoding="utf-8") as stream:
        return json.load(stream)["refs"]


def selected_refs(refs, wanted):
    if not wanted:
        return refs
    matches = [r for r in refs if r["id"] == wanted]
    if not matches:
        raise ValueError(f"Unknown reference id: {wanted}")
    return matches


def source_dir(import_root, ref):
    n = int(ref["n"])
    candidates = sorted(path for path in import_root.glob(f"{n:02d}-*") if path.is_dir() and not path.is_symlink())
    return candidates[0] if candidates else None


def local_images(folder):
    if not folder or not folder.is_dir():
        return []
    return sorted(
        item for item in folder.iterdir()
        if item.is_file() and not item.is_symlink() and item.suffix.lower() in IMAGE_SUFFIXES
    )


def write_sources(destination, ref, names):
    lines = [
        f"# Local study cache — {ref['id']}",
        "",
        "Third-party, study only, do not publish.",
        "",
        f"Project page: {ref['url']}",
        f"Study date: {ref.get('studied', 'unknown')}",
        "",
        "## Local files",
        "",
    ]
    if names:
        lines.extend(f"- `{name}` ← {ref['url']} ({ref.get('studied', 'unknown')})" for name in names)
    else:
        lines.append("- No image files copied.")
    lines.append("")
    (destination / "SOURCES.md").write_text("\n".join(lines), encoding="utf-8")


def do_import(import_root, refs):
    if not import_root.is_dir():
        raise ValueError(f"Import directory does not exist: {import_root}")
    copied_refs = copied_files = 0
    for ref in refs:
        source = source_dir(import_root, ref)
        files = local_images(source)
        destination = CACHE_ROOT / ref["id"]
        destination.mkdir(parents=True, exist_ok=True)
        names = []
        for file in files:
            shutil.copy2(file, destination / file.name)
            names.append(file.name)
            copied_files += 1
        write_sources(destination, ref, names)
        if files:
            copied_refs += 1
        print(f"{ref['id']}: copied {len(files)} image file(s)" if files else f"{ref['id']}: no local image files found")
    print(f"Import complete: {copied_files} image file(s) across {copied_refs} reference(s).")


def do_status(refs):
    total = 0
    for ref in refs:
        folder = CACHE_ROOT / ref["id"]
        images = local_images(folder)
        total += len(images)
        print(f"{ref['id']}: {'present' if images else 'absent'} ({len(images)} image file(s))")
    print(f"Status: {sum(bool(local_images(CACHE_ROOT / r['id'])) for r in refs)}/{len(refs)} refs present; {total} image file(s).")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        refs = load_refs()
        if args.open_id:
            ref = selected_refs(refs, args.open_id)[0]
            print(ref["url"])
            return 0
        refs = selected_refs(refs, args.ref)
        if args.import_dir is not None:
            do_import(Path(args.import_dir).expanduser(), refs)
        else:
            do_status(refs)
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
