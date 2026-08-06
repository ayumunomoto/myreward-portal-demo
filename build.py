#!/usr/bin/env python3
"""
Bundles a thin-wrapper page (index.html / lite.html / hub.html) plus its
referenced assets/*.css and assets/*.js into a single self-contained HTML
file, suitable for publishing as a Claude Artifact (which requires exactly
one file) or for any other context that can't load relative assets.

Usage:
  python3 build.py index.html [output_path]
  python3 build.py lite.html
  python3 build.py hub.html
  python3 build.py --all [output_dir]

If output_path is omitted, writes "<name>.standalone.html" next to the
source file.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).parent
LINK_RE = re.compile(r'<link rel="stylesheet" href="(assets/[^"]+)">\n?')
SCRIPT_SRC_RE = re.compile(r'<script src="(assets/[^"]+)"></script>\n?')

PAGES = ["index.html", "lite.html", "hub.html"]


def bundle(page_path: pathlib.Path) -> str:
    html = page_path.read_text(encoding="utf-8")

    def link_sub(m):
        asset = ROOT / m.group(1)
        return "<style>\n" + asset.read_text(encoding="utf-8") + "</style>\n"

    def script_sub(m):
        asset = ROOT / m.group(1)
        return "<script>\n" + asset.read_text(encoding="utf-8") + "</script>\n"

    html = LINK_RE.sub(link_sub, html)
    html = SCRIPT_SRC_RE.sub(script_sub, html)
    return html


def main(argv):
    if not argv:
        print(__doc__)
        return 1

    if argv[0] == "--all":
        out_dir = pathlib.Path(argv[1]) if len(argv) > 1 else ROOT
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in PAGES:
            src = ROOT / name
            out = out_dir / (src.stem + ".standalone.html")
            out.write_text(bundle(src), encoding="utf-8")
            print(f"{name} -> {out}")
        return 0

    src = ROOT / argv[0]
    if not src.exists():
        print(f"Not found: {src}")
        return 1
    out = pathlib.Path(argv[1]) if len(argv) > 1 else src.with_name(src.stem + ".standalone.html")
    out.write_text(bundle(src), encoding="utf-8")
    print(f"{argv[0]} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
