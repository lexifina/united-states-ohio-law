# How this repository was made (Ohio)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Wikidata | <https://www.wikidata.org/wiki/Q1397> | 2026-10-30 | CC0 1.0 (structured data in the main, Property and Lexeme namespaces). |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `legal-system` | Ohio legal system: open facts (metadata only, no law text) | 1 | 2026-10-29 to 2026-10-29 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No law text is held; the single version is dated by the day before retrieval https://www.wikidata.org/wiki/Q1397

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `591fb7ef6530d2f754eeb4a1c5da274f8dd2a9a2f8e94d759d8f857231561226` (3415 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Metadata only: neither block was worked around, so no law text is held.
- The version is dated 2026-10-29, the last full day before retrieval, so that no commit is dated ahead of the build.
- The Supreme Court of Ohio's inception date in Wikidata (1841, year precision) is left out as unreliable.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
