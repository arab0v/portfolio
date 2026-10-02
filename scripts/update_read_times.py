#!/usr/bin/env python3
"""Recompute the `read` (minutes) field for every post in posts-data.js.

Usage:
    python3 update_read_times.py

Counts words in each post's rendered text (strips tags/scripts/styles),
assumes ~200 words/min, and rewrites the "read": N value in place.
Run this after writing or editing a post's content.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "blog"   # blog/
POSTS_DIR = ROOT / "posts"
DATA_FILE = ROOT / "posts-data.js"

TAG_RE = re.compile(r"<[^>]+>")
BLOCK_RE = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
ENTITY_RE = re.compile(r"&[a-zA-Z]+;")


def word_count(html: str) -> int:
    body = BLOCK_RE.sub(" ", html)
    body = TAG_RE.sub(" ", body)
    body = ENTITY_RE.sub(" ", body)
    return len([w for w in body.split() if any(c.isalnum() for c in w)])


def main() -> None:
    data = DATA_FILE.read_text()
    slugs = re.findall(r'"slug":\s*"([^"]+)"', data)

    for slug in slugs:
        path = POSTS_DIR / f"{slug}.html"
        if not path.exists():
            print(f"  ! missing post file: {path.name}")
            continue
        words = word_count(path.read_text())
        minutes = max(1, round(words / 200))
        # replace the "read": N that follows this slug's entry
        pattern = re.compile(
            r'("slug":\s*"' + re.escape(slug) + r'",(?:.|\n)*?"read":\s*)(\d+)'
        )
        data, n = pattern.subn(lambda m: m.group(1) + str(minutes), data, count=1)
        status = f"read={minutes} min ({words} words)" if n else "NO MATCH — left as-is"
        print(f"  {slug}: {status}")

    DATA_FILE.write_text(data)
    print(f"Updated {DATA_FILE}")


if __name__ == "__main__":
    main()
