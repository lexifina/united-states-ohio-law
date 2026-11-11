# United States (Ohio): law history in git

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law of Ohio, United States, which global-law reads at `united-states/ohio/acts/`.

The law of Ohio as a git history: one file per provision, with `git blame` and `git log` working line by line. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `legal-system/` | Ohio legal system: open facts (4 entries, Wikidata) | 1 | One version, 2026-10-29 (first build) |
| `constitution-article-NN/` | Constitution of the State of Ohio: 19 articles | 1 | 226 sections; each article dated by the day of the capture read (2025-07-15 to 2026-07-16) |
| `orc-chapter-NNNN/` | Ohio Revised Code: 973 of the 973 chapters listed on the title pages | 1 | 33184 sections; 968 chapters from archive captures and five newly listed chapters from live official pages |

**Source.** The Ohio Revised Code and the Ohio Constitution are published by the Legislative Service Commission on [codes.ohio.gov](https://codes.ohio.gov/). The original 968 chapter texts and 19 Constitution articles were read from Internet Archive copies of official pages. Chapters 1314, 1316, 1357, 3957 and 4151 were added from current official pages on 11 November 2026. Each chapter page prints every section's full text with its "Effective" date and "Latest Legislation"; both are kept as the section's last line. The four Wikidata facts of the first build (`legal-system/`) are kept.

## Dates

The pages carry the current text only. The original chapters and articles are one version each, "oldest version available", dated by the day of their Internet Archive captures (the newest capture since 1 January 2025 of each page). The five chapters added from current official pages each have one version dated by the common "Effective" day printed for all of their sections. Later builds will add later versions on top.

## How it is checked

Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`) and must match `corpus.json`; the results are in `REPRODUCE.md`.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist (`<law key>@codes-ohio-gov.invalid`). No dated history is available, so every commit is credited to the publisher (codes.ohio.gov, or Wikidata for `legal-system/`) as "oldest version available". The committer is always Lexifina.

## Limits

973 of the 973 Revised Code chapters listed on the title pages are included; complete titles: Title 1, Title 3, Title 5, Title 7, Title 9, Title 11, Title 13, Title 15, Title 17, Title 19, Title 21, Title 23, Title 25, Title 27, Title 29, Title 31, Title 33, Title 35, Title 37, Title 39, Title 41, Title 43, Title 45, Title 47, Title 49, Title 51, Title 53, Title 55, Title 57, Title 58, Title 59, Title 61, Title 63. A chapter is included only when its source page holds the text of every section it lists. The Constitution's preamble and schedules, session laws and the Administrative Code are not included. There is no history before the dates above.
