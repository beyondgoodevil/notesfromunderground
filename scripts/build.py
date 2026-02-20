import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "pandoc"], check=True)
#!/usr/bin/env python3
"""
build.py — Convert all Markdown notebooks to HTML and regenerate index.html
Run: python3 scripts/build.py
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = ROOT / "notebooks"
PUBLIC_DIR = ROOT / "docs"
PUBLIC_NOTEBOOKS_DIR = PUBLIC_DIR / "notebooks"
TEMPLATE = ROOT / "templates" / "notebook.html"
INDEX_TEMPLATE = ROOT / "templates" / "index.html"
INDEX_OUT = PUBLIC_DIR / "index.html"

PUBLIC_DIR.mkdir(exist_ok=True)
PUBLIC_NOTEBOOKS_DIR.mkdir(exist_ok=True)


def check_pandoc():
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("ERROR: pandoc not found. Install it from https://pandoc.org/installing.html")
        sys.exit(1)


def get_title_and_date(md_path):
    """Extract title from first H1 and date from frontmatter or file mtime."""
    content = md_path.read_text(encoding="utf-8")
    title = md_path.stem.replace("-", " ").title()
    date_str = None

    # Check for YAML frontmatter
    if content.startswith("---"):
        fm_end = content.find("---", 3)
        if fm_end != -1:
            fm = content[3:fm_end]
            title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
            date_match = re.search(r'^date:\s*(.+?)\s*$', fm, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            if date_match:
                date_str = date_match.group(1).strip()

    # Fallback: first H1
    if not title or title == md_path.stem.replace("-", " ").title():
        h1 = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if h1:
            title = h1.group(1).strip()

    # Fallback: file mtime
    if not date_str:
        mtime = md_path.stat().st_mtime
        date_str = datetime.fromtimestamp(mtime).strftime("%d %b %Y %H:%M")

    return title, date_str


def build_notebook(md_path):
    """Convert a single .md file to HTML in docs/notebooks/."""
    title, date_str = get_title_and_date(md_path)
    out_name = md_path.stem + ".html"
    out_path = PUBLIC_NOTEBOOKS_DIR / out_name

    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(out_path),
        "--template", str(TEMPLATE),
        "--metadata", f"title={title}",
        "--metadata", f"date={date_str}",
        "--from", "markdown+smart",
        "--to", "html5",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR building {md_path.name}: {result.stderr}")
        return None
    else:
        print(f"  ✓ {md_path.name} → {out_name}")
        return {"title": title, "date": date_str, "file": out_name}


def build_index(entries):
    """Generate the main index.html from all notebook entries."""
    # Sort by date descending
    def parse_date(d):
        for fmt in ("%d %b %Y %H:%M", "%Y-%m-%d", "%d %b %Y"):
            try:
                return datetime.strptime(d, fmt)
            except ValueError:
                pass
        return datetime.min

    entries.sort(key=lambda e: parse_date(e["date"]), reverse=True)

    entries_html = ""
    for e in entries:
        entries_html += f'''    <div class="notebook-entry">
      <a href="notebooks/{e['file']}">{e['title']}</a>
      <span class="date">{e['date']}</span>
    </div>\n'''

    index_template = INDEX_TEMPLATE.read_text(encoding="utf-8")
    output = index_template.replace("{{ENTRIES}}", entries_html)
    INDEX_OUT.write_text(output, encoding="utf-8")
    print(f"\n  ✓ index.html ({len(entries)} notebooks)")


def main():
    print("🔨 Building notebooks site...\n")
    check_pandoc()

    md_files = sorted(NOTEBOOKS_DIR.glob("*.md"))
    if not md_files:
        print("No .md files found in notebooks/. Add some and rebuild!")
        return

    entries = []
    for md in md_files:
        result = build_notebook(md)
        if result:
            entries.append(result)

    build_index(entries)
    print(f"\n✅ Done! {len(entries)} notebooks built → docs/")
    print("   Open docs/index.html in your browser, or deploy the docs/ folder to Netlify.\n")


if __name__ == "__main__":
    main()