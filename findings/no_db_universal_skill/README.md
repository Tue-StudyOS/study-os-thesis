# No-DB Universal Skill — Findings

This subfolder records the reasoning, decisions, and open risks for the
**database-less, university-wide thesis-discovery skill** direction.

## The Direction in One Sentence

Instead of maintaining a scraped database of chairs/professors, the skill
*encodes how Claude interviews the student and how it searches the live web*,
so it works for **all faculties of the University of Tübingen** (and later
companies) with **zero ongoing maintenance**.

## Why This Direction Exists

The team will not be around to maintain a database in a few months, and no one
is expected to take over scraping/CI upkeep. A maintenance-free system that
stays correct because it reads the live web is the only thing that survives.

## Documents

- [2026-06-26-concept-and-risks.md](2026-06-26-concept-and-risks.md) — the
  concept, the grilling, decisions, and open risks.

## Related

- Vision doc at repo root: [VISION_NO_DB.md](../../VISION_NO_DB.md)
- Branch: `feat/no-db-universal-skill` (off `codex/chair-discovery-eval-from-valentin`)
