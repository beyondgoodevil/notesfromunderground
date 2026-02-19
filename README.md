# My Notebooks Site

My personal knowledge base — notes on books, ideas, and research — published to the web.

## How It Works

- You write notes in plain **Markdown** files inside `notebooks/`
- Running `python3 scripts/build.py` converts them all to HTML in `public/`
- Push to GitHub → **Netlify auto-deploys** your site

---

## Quick Start

### 1. Prerequisites

Install [Pandoc](https://pandoc.org/installing.html):

```bash
# macOS
brew install pandoc

# Ubuntu/Debian
sudo apt install pandoc

# Windows: download installer from https://pandoc.org/installing.html
```

### 2. Add or edit a notebook

Notebooks live in the `notebooks/` folder as `.md` files. Each file should start with YAML frontmatter:

```markdown
---
title: Your Notebook Title
date: 18 Feb 2026 12:00
---

# Your Notebook Title

Your notes go here. Write in plain Markdown.

## A Section

- Bullet points work
- **Bold**, *italic*, `code`

> Blockquotes for quotations

## References

- Author, *Book Title* (Year)
- [Link text](https://example.com)

## See Also

- [Other Notebook](other-notebook.html)
```

**The filename becomes the URL.** `notebooks/statistics.md` → `yoursite.com/notebooks/statistics.html`

### 3. Create a new notebook quickly

```bash
python3 scripts/new-notebook.py "My New Topic"
# Creates notebooks/my-new-topic.md with frontmatter pre-filled
```

### 4. Build the site

```bash
python3 scripts/build.py
```

This regenerates `public/` — the index page and all notebook HTML files.

### 5. Preview locally

Open `public/index.html` in your browser. That's it — no server needed, it's all static HTML.

---

## Publishing to Netlify

### First-time setup

1. Push this folder to a GitHub repository
2. Go to [app.netlify.com](https://app.netlify.com) → **Add new site** → **Import from Git**
3. Connect your GitHub account and select your repo
4. Set these build settings:
   - **Build command**: `python3 scripts/build.py`
   - **Publish directory**: `public`
5. Click **Deploy site**

Netlify gives you a free URL like `https://your-site-name.netlify.app`.

### Every time you update

```bash
# Edit or add a notebook in notebooks/
# Then:
git add .
git commit -m "Add notes on X"
git push
```

Netlify detects the push and automatically rebuilds and redeploys. Your site updates in about 30 seconds.

### Custom domain (optional)

In Netlify: **Site settings → Domain management → Add custom domain**.

---

## Folder Structure

```
notebooks-site/
├── notebooks/          ← YOUR MARKDOWN FILES GO HERE
│   ├── statistics.md
│   ├── probability.md
│   └── ...
├── templates/
│   ├── index.html      ← Template for the index page
│   └── notebook.html   ← Template for individual notebook pages
├── scripts/
│   ├── build.py        ← Main build script
│   └── new-notebook.py ← Helper to create new notebooks
├── public/             ← GENERATED OUTPUT (don't edit by hand)
│   ├── index.html
│   └── notebooks/
│       ├── statistics.html
│       └── ...
├── netlify.toml        ← Netlify configuration
└── README.md           ← This file
```

---

## Tips

- **Date format**: Use `DD Mon YYYY HH:MM` (e.g. `18 Feb 2026 14:30`) for consistency with the original site style
- **Linking between notebooks**: Use relative links: `[Statistics](statistics.html)` (note: `.html` not `.md`)
- **The index is sorted by date** (most recently modified first) — update the `date:` in frontmatter when you edit a notebook
- **Keep notes rough**: these are notebooks, not essays. Bullet points, half-formed thoughts, and "things to look into" are all fine.
