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

Requires Python 3 (`scripts/render_poster.py` renders posters; see the script header for dependencies).

## Rules for contributors

- Only skill logic goes in the repo: `SKILL.md`, `scripts/`, `references/`, `assets/`, `starter/`.
- Never commit drafts, customer or partner data, photos, credentials or `.env`.
