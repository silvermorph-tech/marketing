# Quality rubric (self-check before every approval card)

Run it on the finished draft and poster. Fix and re-check, up to 2 rounds. A hard-gate failure blocks the post, no matter how good the rest is.

## Hard gates (all must pass)
1. **Facts:** every number, name, date, quote is in `inputs/00-facts/facts-bank.md` with status SITE or OK, or was given in chat. No UNVERIFIED fact.
2. **Consent:** every named person, customer, partner and logo has consent on file.
3. **Lint:** `python3 scripts/lint_copy.py draft.txt` returns 0 hits.
4. **No stamp:** the poster has no DRAFT, DEMO or PREVIEW chip.
5. **Category:** structure beats in order, length in range, hashtags from the category list, category gates in `categories.md` satisfied.
6. **English only** on poster and copy.
7. **No claims** about medical outcomes or compliance beyond the owner-approved wording.

## Content tests (score each 0 or 1, need 5 of 6)
1. After 20 seconds the reader knows something new: write that sentence. If you cannot, fail.
2. A competitor could not post this unchanged.
3. The root cause is named before the product is.
4. It sounds like a friend who knows the field, not an announcement.
5. The hook is inside the first 210 characters and is a statement.
6. The closing question is specific enough that one reader could answer it in a comment.

## Design tests (need 4 of 5)
1. Headline readable on a 360 px wide render.
2. One idea only; nothing decorative that carries no meaning.
3. Brand tokens only; frame invariants intact.
4. Layout differs from the previous post in this category (`published/publish-log.csv`).
5. Every photo is a supplied real file (no AI-generated images); product UI is English and legible.

## Output of the check
One line per failed test and what was changed. If everything passed, say so in one line. Never explain away a failure.
