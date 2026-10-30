# Ohio: law history in git

The statute law of Ohio as a git repository: one file per section, committed with the official publisher named as author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `legal-system/` | Ohio legal system: open facts (4 entries) | 1 | One version: facts from Wikidata, retrieved 30 October 2026 |

Nothing else of Ohio's law is in it yet.

## Where the text comes from

We did not work round either block. What is here are four open facts from [Wikidata](https://www.wikidata.org/wiki/Q1397) (CC0): the State of Ohio, the Constitution of Ohio, the Ohio Revised Code and the Supreme Court of Ohio, with their descriptions, classes and official websites, and Ohio's date of admission to the Union (1 March 1803, as Wikidata gives it).

## Dates

- The single version is dated **29 October 2026**, the last full day before retrieval, and is credited to Wikidata as "oldest version available". The only historical date in it is the admission date, given in the text.
- The Wikidata inception date for the Supreme Court of Ohio (1841, year precision) is left out as unreliable.

## What it does not show

- Any law text: the Constitution of Ohio, the Revised Code, session laws and regulations.
- Any history of change.
- Nothing here is an official publication. This repository will be replaced by a real build if Ohio's General Assembly or the Legislative Service Commission opens a permitted way to read the Code.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
- Each source file is identified by its sha256, in `data/versions.json`.

## What "author" means

Each commit is authored by the publisher (Wikidata) because this first build holds one version of each act, the oldest version available. The committer is always Lexifina.
