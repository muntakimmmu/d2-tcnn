# PRISMA 2020 systematic review: forecasting and sustainability in Middle Eastern (Saudi) tourism

**Status: draft requiring human verification. Not submission-ready.** See `paper/main.tex` Section 5 (Limitations).

## What was done
- Search: Crossref REST API only (70 queries, top-100 each, journal articles 2015-2026), run 2026-10-05.
- Screening: automated keyword stages (`search/screen.py`, `search/screen_stage2.py`) then manual title/abstract assessment by a single AI reviewer.
- Coding: abstract-level only (publisher full texts were blocked by the network policy). Items not in the abstract are `n/r`.
- 42 studies included (16 forecasting, 11 demand modelling, 15 sustainability nexus).

## Reproduce
```
cd review
python3 search/crossref_search.py   # data/crossref_raw.json, data/search_log.json
python3 search/screen.py && python3 search/screen_stage2.py
python3 search/fetch_candidates.py  # includes manual eligibility decisions (indices) and 6 targeted additions
python3 search/build_dataset.py     # coding + PRISMA counts (decisions are hand-coded in this file)
python3 search/gen_tex.py           # tables/macros for the paper
cd paper && latexmk -pdf main.tex
```
Eligibility decisions and abstract-level coding are hand-coded in `search/build_dataset.py` (not automated).

## Integrity notes
- All 42 included studies and 18 background references had their bibliographic metadata retrieved from Crossref by DOI/title match. Exception: authors of Hansen, Lunde & Nason (2011) were missing in Crossref and added manually.
- `data/stream*.json` are unverified web-search snippet records from earlier passes; used only to seed targeted searches, not as evidence.
- Items required before submission: full-text verification of every included study, second independent reviewer, additional databases (Scopus/WoS), registration (e.g. OSF), author/funding/COI fields, journal template.
