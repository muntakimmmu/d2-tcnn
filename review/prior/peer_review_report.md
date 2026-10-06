# Referee report

**Manuscript:** *Forecasting and Sustainability in Middle Eastern Tourism, with Emphasis on Saudi Arabia: A PRISMA 2020 Systematic Review of the Empirical Literature, 2015–2026* (version of 6 October 2026, 29 pp.)
**Type:** systematic review (PRISMA 2020)
**Benchmark:** nine published reviews in the same domain, read at full text.
**Reviewer stance:** a referee for a Q1 tourism or sustainability journal. Statements about competitor reviews come from their full texts (`review/fulltext/`); the extraction is in `prior/structure/benchmark.json` and the table below.

---

## 1. Summary of the submission

The manuscript maps the Middle East literature from 2015 to 2026, with a Saudi focus, on three themes:
- tourism and hospitality **forecasting** (F, n = 16);
- **demand modelling** (D, n = 11);
- **tourism–sustainability** analysis (S, n = 14).

The search used Crossref: 70 queries, 7,000 records, 2,237 unique. Two automated keyword stages and a title/abstract assessment by one AI reviewer left 42 provisionally included studies. Full texts were retrieved for 21 of these; one was excluded at full text, leaving 41.

The central claim is that the two literatures are disconnected:
- only 1 of 16 forecasting studies includes a sustainability dimension;
- only 1 of 25 non-forecasting studies projects forward (climate scenarios);
- none evaluates out-of-sample accuracy;
- a keyword co-occurrence network separates into a forecasting cluster and a sustainability/econometrics cluster, with 24% cross-cluster weight.

The paper also offers a framework of link directions and a "capacity-aware forecasting" agenda, which it positions against the existing early-warning literature.

## 2. Benchmark against published reviews in the domain

| Review (journal) | Sources searched | Included | PRISMA flow | Duplicate screening reported | Quality appraisal | Figures / tables | Analysis |
|---|---|---|---|---|---|---|---|
| Ajuhari et al. 2023 (*Sustainability*) | Google Scholar, Scopus, MDPI | 100 | yes | no | not formal | 1 / 7 | descriptive + tabular |
| Alhejaili & Ahmad 2025 (*JTHEM*) | Google Scholar only | not reported as a count | steps figure | no | no | 2 / 1 | narrative |
| Dowlut & Gobin-Rahimbux 2023 (*Heliyon*) | snowballing (start set + forward/backward) | 50 | snowballing flow | mentioned (detail not verified) | partial | 5 / 12 | descriptive + tabular |
| Henriques & Nobre Pereira 2024 (*Tourism & Management Studies*) | Scopus, Web of Science | 20 | yes | no | no | 1 / 7 | thematic tables |
| Long et al. 2022 (*IJERPH*) | Scopus | 297 | no | no | no | 6 / 1 | CiteSpace/VOSviewer bibliometrics |
| Majid et al. 2023 (*Journal of Sustainable Tourism*) | WoS, Scopus, ScienceDirect, IEEE, ACM, Google Scholar | 306 full texts screened | yes | no | no | 5 / 2 | bibliometric + framework |
| Iqbal & Aftab 2025 (*IJSDP*) | Scopus, WoS, ScienceDirect, Google Scholar, Emerald | from 500 records | yes | no | no | 1 / 6 | thematic tables |
| Song, Qiu & Park 2019 (*Annals of Tourism Research*) | curated collection | 211 key studies | no | no | no | 2 / 1 | method–performance synthesis |
| Zhang et al. 2020 (*Tourism Management Perspectives*) | WoS Core Collection | bibliometric corpus | no | no | no | 14 / 5 | CiteSpace knowledge mapping |
| **This manuscript** | **Crossref only** (+ targeted searches) | **41** (20 full-text confirmed) | **yes (official template)** + full checklist | **no (single AI reviewer)** | **reporting screen only** | **8 / 8** (+ appendices) | descriptive + keyword network + thematic + cross-theme |

**Reading of the benchmark.** The manuscript is at or above the median of this comparison set on four counts:
- **PRISMA reporting:** it is the only one with a completed item-by-item checklist.
- **Transparency:** code, logs and every exclusion with its reason are public.
- **Structure and figures:** it covers the full set of competitor figure types.
- **Honesty about limitations.**

It falls below the set on two counts:
- **Search coverage:** every other review used Scopus and/or Web of Science, or a documented snowballing protocol. This manuscript uses Crossref only, with each query capped at its top 100 records.
- **Depth of extraction:** the competitor reviews extract from full texts. Here, half of the evidence base and all of the coded data items rest on abstracts.

Duplicate screening and formal quality appraisal are weak across the whole set, so on those points the manuscript is not an outlier. A Q1 referee will still raise them.

## 3. Assessment by criterion

**Significance and originality (moderate to good).**
- *Scope intersection.* Of the 25 verified prior reviews, the closest are Saleh et al. 2021 (GCC, PRISMA, 23 studies, no forecasting lens) and Sun, Gössling & Zhou 2022 (global tourism–carbon econometrics). None of the 25 jointly synthesises forecasting and sustainability evidence for this region.
- *The split is a useful insight.* It is shown two independent ways: by thematic cross-classification and by the keyword network.
- *Positioning is fair and not overstated.* The agenda is correctly positioned as an extension of carrying-capacity early-warning work (Ye et al. 2020; Long et al. 2022), not as a new idea.
- *Theme S adds little alone.* Taken by itself, it is a thinner regional subset of Sun et al. 2022.

**Methodological rigour (weak to moderate).** Five issues; the major comments below detail each:
- a single database;
- capped retrieval, with a documented recall shortfall;
- automated keyword pre-screening;
- a single AI reviewer;
- abstract-level extraction, and no formal risk-of-bias assessment.

The manuscript discloses all of these honestly. Disclosure does not remove them.

**Synthesis (moderate).**
- The descriptive and cross-theme analyses are clear, and the 2×2 table is the right summary device.
- The synthesis lacks effect directions and magnitudes:
  - forecasting accuracy (MAPE values against a naïve benchmark);
  - tourism–emission elasticities and their signs;
  - comparison of these with the global reviews.

**Presentation (good).** The structure mirrors the competitor reviews. The figures are clean and colour-validated, and the tables are complete. The main text is long relative to the evidence base: 29 pages against 7–22 for most competitors.

**Reproducibility (very good).** Every count is regenerated from logged data by scripts, which is better than any review in the comparison set.

## 4. Major comments

**M1. Search coverage.** Crossref with top-100 retrieval per query is not accepted as a primary source in tourism or sustainability systematic reviews. Every competitor review used Scopus and/or Web of Science. The authors' own recall check found 5 of 42 provisionally included studies outside the automated pipeline, 4 of them not retrieved at all.
- *Required:* rerun the search in Scopus and Web of Science, plus an Arabic or regional source such as the Saudi Digital Library, with full Boolean strings and dates.
- *Required:* report per-database counts in the flow diagram.

**M2. Full-text assessment and extraction.**
- 21 of 41 included studies are included on abstract evidence only.
- All data items, including benchmark, accuracy measure and sustainability dimension, are coded from abstracts.
- The one full-text check performed already changed a decision (Triki 2019 was excluded), which shows abstract-level coding is unreliable here.

*Required:* complete full-text eligibility for all included studies, and re-extract every data item from full texts.

**M3. Reviewer independence.** Screening and coding were done by one AI agent with no human duplicate, so no agreement statistic can be reported.
- *Required:* two independent human reviewers for at least the title/abstract stage (or a 20% calibration sample) and for all extraction, with Cohen's κ.
- *Required:* a disclosure of AI assistance that meets the target journal's policy.

**M4. Quality and risk of bias.** The six-item "reporting-transparency screen" is not a risk-of-bias assessment.
- *Required:* for Theme F, an adapted PROBAST or forecasting-specific checklist covering holdout design, leakage, naïve or seasonal-naïve benchmark, scale-free error measure (MASE), statistical comparison (Diebold–Mariano) and horizon.
- *Required:* for Themes D and S, an econometric checklist covering stationarity and cointegration testing, structural breaks, cross-sectional dependence in panels, and endogeneity.

Only full texts can support either of these.

**M5. Is the central finding partly built into the design?** The themes F, D and S are defined by the very property being cross-tabulated: forecasting, or not. A referee will ask whether the split is a classification artefact. The 2×2 table uses content flags, and the keyword network is independent of the themes, which is a good partial answer. Two further steps would settle it:
- *Required:* report the 2×2 table on full-text coding.
- *Required:* add a sensitivity check that retains growth-nexus studies, which were excluded under criterion R3, to show the split survives a broader corpus.

**M6. Depth of the Theme S synthesis compared with Sun et al. 2022.** To justify a regional review of tourism–emission studies, extract from full texts the elasticities, their signs and significance, and whether aviation is included. Then test whether the regional pattern differs from Sun et al.'s global "low consensus" finding. As written, this section describes and does not compare.

**M7. Small and heterogeneous forecasting corpus.** There are 16 Theme F studies across six settings, including hotel prices and spending.
- Statements such as "a lag in adopting search data" (3 of 16 studies) need either a denominator comparison with the global reviews or softer wording.
- *Required:* extract accuracy figures and benchmark-relative skill from full texts, so that the paper says something about which methods forecast well in this region. This is the question every forecasting review in the comparison set answers.

**M8. Scope definition.** Including Türkiye (9 studies, 6 of them forecasting) moves the "Middle East" results towards a single country.
- *Required:* report the main results with and without Türkiye.
- *Required:* justify the regional definition with a source.

**M9. Protocol.** There is no registration and no prospective protocol, which several Q1 tourism journals now expect for PRISMA reviews. Register on OSF before the re-search, and report amendments.

## 5. Minor comments

1. The title is long. Consider: "Forecasting and sustainability in Middle Eastern tourism: a systematic review with a Saudi Arabia focus".
2. Table 1 (prior reviews) codes two entries from web-search snippets. Code them from full texts; Iqbal & Aftab 2025 is now available.
3. The framework figure hard-codes "n = 3" while other counts are macros. Generate it from the data like the others.
4. The keyword network uses a 28-term controlled vocabulary, so it is partly subjective. Report the vocabulary in an appendix, and add a robustness check (for example, a different co-occurrence threshold).
5. The journals figure adds little; most competitor reviews use a table for this. Consider merging it.
6. Appendix A duplicates the supplementary checklist. Keep one.
7. Data availability points to a git branch. Deposit a versioned snapshot with a DOI (Zenodo or OSF).
8. The declarations (funding, competing interests, authors) are still placeholders.
9. Use one form of the country name: "Türkiye" in the text, while some author titles use "Turkey".
10. At 29 pages the manuscript is long. The methods are longer than the results; move the search log and the exclusion list fully into the supplement.

## 6. Scores (1–10)

| Criterion | Score | Note |
|---|---|---|
| Originality | 6 | real scope gap; the contribution is synthesis, not method |
| Technical quality | 4 | one database; abstract-level extraction; single AI reviewer |
| Significance | 6 | the split is useful for Vision 2030 planning research |
| Evidence | 4 | 21/41 studies at abstract level; no risk of bias |
| Clarity | 7 | well structured; somewhat long |
| Reproducibility | 9 | best in the comparison set |

## 7. Recommendation

- **For a Q1 tourism or sustainability journal** (the level of *Journal of Sustainable Tourism*, *Tourism Management Perspectives*, *Annals of Tourism Research*): **Reject in current form, encourage resubmission.** M1–M4 are standard requirements that the competitor reviews at that level satisfy, at least for database coverage and full-text extraction.
- **For a mid-tier or open-access journal** (comparable to several reviews in the benchmark): **Major revision.** The paper's transparency and design already exceed some published comparators, but M1 and M2 still have to be done.

**Path to acceptance, in priority order:** M2 (full texts) → M1 (Scopus/WoS re-search) → M3 (second reviewer, κ) → M4 (risk of bias) → M6–M7 (quantitative extraction) → M5 and M8 (sensitivity checks). Doing M1–M4 would make the review methodologically stronger than every review in the benchmark set except on corpus size. M6–M7 would make it substantively distinctive.

---
*This report was written by the AI agent that also assisted in preparing the manuscript, so it is not an independent review. The competitor-review facts in Section 2 come from their full texts; check them before citing them in a response to referees.*
