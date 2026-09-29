#!/usr/bin/env python3
"""Scaffold a new blog post.

Usage:
  python3 new_post.py "My Post Title" "Short description" tag1 tag2 tag3

Creates blog/posts/<slug>.html and registers it in blog/posts-data.js.
Edit the generated HTML file's <div class="post-body"> to add real content.
"""
import sys, re, datetime, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent  # blog/
POSTS_DIR = ROOT / "posts"
DATA_FILE = ROOT / "posts-data.js"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} — Yousef Aldabbas</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<nav>
  <div class="logo">yousef@backend:~$</div>
  <div class="navlinks">
    <a href="../../index.html">Home</a>
    <a href="../index.html" class="active">Blog</a>
  </div>
</nav>
<div class="wrap">
  <a class="back" href="../index.html">&larr; back to posts</a>
  <div class="post-body">
    <h1>{title}</h1>
    <div class="meta">{date} · {tags_str}</div>
    <p>Write your post here.</p>
  </div>
</div>
</body>
</html>
"""

def slugify(title):
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def main():
    if len(sys.argv) < 3:
        print("Usage: new_post.py \"Title\" \"Description\" [tag1 tag2 ...]")
        sys.exit(1)
    title = sys.argv[1]
    desc = sys.argv[2]
    tags = sys.argv[3:] or ["backend"]
    slug = slugify(title)
    date = datetime.date.today().isoformat()

    post_path = POSTS_DIR / f"{slug}.html"
    if post_path.exists():
        print(f"Post already exists: {post_path}")
        sys.exit(1)

    post_path.write_text(TEMPLATE.format(
        title=title, date=date, tags_str=", ".join(tags)
    ))

    # Update posts-data.js by inserting into the POSTS array
    data_text = DATA_FILE.read_text()
    new_entry = (
        "  {\n"
        f'    "slug": "{slug}",\n'
        f'    "title": {json.dumps(title)},\n'
        f'    "date": "{date}",\n'
        f'    "desc": {json.dumps(desc)},\n'
        f'    "tags": {json.dumps(tags)}\n'
        "  },\n"
    )
    data_text = data_text.replace("const POSTS = [\n", "const POSTS = [\n" + new_entry, 1)
    DATA_FILE.write_text(data_text)

    print(f"Created {post_path}")
    print(f"Registered in {DATA_FILE}")
    print("Edit the .post-body content in the HTML file to write your post.")

if __name__ == "__main__":
    main()
