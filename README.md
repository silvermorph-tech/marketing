# Silvermorph Skills

Shared Claude skills for the Silvermorph team.

| Skill | What it does |
|---|---|
| `silvermorph-linkedin` | Company-page LinkedIn posting coach: topic, on-brand copy, poster, fills the composer; you click Post |

## Install (Claude Code)

```bash
git clone https://github.com/silvermorph-tech/marketing.git
mkdir -p ~/.claude/skills
cp -R marketing/silvermorph-linkedin ~/.claude/skills/
```

Update: `git pull`, then copy again (your local `drafts/`, `inputs/`, `calendar/` are not in the repo; copy with `rsync -a --exclude drafts --exclude inputs --exclude calendar --exclude published --exclude inbox` to keep them).

## First use

Open Claude Code and say "I want to post on LinkedIn". The skill creates its working folders from `starter/`. Fill `inputs/00-facts/facts-bank.md` with verified facts first; unverified facts are never used.

Requirements: Python 3, Google Chrome or Chromium (posters are HTML screenshotted by headless Chrome; set `CHROME_PATH` if it is not found), and `pip install pillow` for `export_upload_set.py`.

Every post image is HTML. `silvermorph-linkedin/references/design-reference.html` shows all layouts live; after changing a layout run `python3 scripts/build_reference.py` to refresh it.

## Daily workflow (what your teammates do)

1. Open Claude Code, say "I want to post on LinkedIn" (or drop copy and photos into the chat).
2. The coach confirms the post, writes or checks the copy, picks the layout from `references/design-reference.html`, and renders the poster (`scripts/render_poster.py`, HTML screenshotted by Chrome).
3. You approve the card. The coach hands you every file to upload, numbered in order, and fills the LinkedIn composer in the browser.
4. You click Post, then tell the coach "published". It logs and archives the draft.

Every poster is HTML: all layouts are in `references/design-reference.html`. To add or change a layout, edit `scripts/render_poster.py` and `assets/posters.css`, then run `python3 scripts/build_reference.py`.

## Rules for contributors

- Only skill logic goes in the repo: `SKILL.md`, `scripts/`, `references/`, `assets/`, `starter/`.
- Never commit drafts, customer or partner data, photos, credentials or `.env`.
