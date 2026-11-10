# United States (Ohio): law history in git

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law of Ohio, United States, which global-law reads at `united-states/ohio/acts/`.

The law of Ohio as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `legal-system/` | Ohio legal system: open facts (4 entries, Wikidata) | 1 | One version, 2026-10-29 (first build) |
| `constitution-article-NN/` | Constitution of the State of Ohio: 19 articles | 1 | 226 sections; each article dated by the day of the capture read (2025-07-15 to 2026-07-16) |
| `orc-chapter-NNNN/` | Ohio Revised Code: 336 of the 968 chapters listed on the title pages | 1 | 11081 sections; each chapter dated by the day of the capture read (2025-06-26 to 2026-10-29) |

Each chapter page prints every section's full text with its "Effective" date and "Latest Legislation"; both are kept as the section's last line. The four Wikidata facts of the first build (`legal-system/`) are kept.

## Dates

The pages carry the current text only. Each chapter and article is therefore one version, "oldest version available", dated by the day of the Internet Archive capture read (the newest capture since 1 January 2025 of each page); codes.ohio.gov prints no edition date. A section's own "Effective" line says since when its words have been in force. Later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@codes-ohio-gov.invalid`). No dated history is available, so every commit is credited to the publisher (codes.ohio.gov, or Wikidata for `legal-system/`) as "oldest version available". The committer is always Lexifina.

## Limits

336 of the 968 Revised Code chapters listed on the title pages are included; complete titles: Title 1, Title 3, Title 5, Title 7, Title 9, Title 11, Title 13, Title 15, Title 17, Title 19; partly covered: Title 21 (14 of 25). A chapter is included only when its capture holds the text of every section it lists. Left out: no capture (632). The Constitution's preamble and schedules, session laws and the Administrative Code are not included. There is no history before the dates above.
