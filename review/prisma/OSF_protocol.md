# OSF registration: protocol (prepared for registration at revision stage)

> **Status.** This protocol records the methods the review actually used, plus the planned revision steps. Registration happens **after** the first search, so it must be registered on OSF as a **retrospective registration with amendments**. Do not present it as prospective. Use the template "OSF Preregistration" or "Generalized Systematic Review Registration".

## 1. Title
Forecasting and sustainability in Middle Eastern tourism, with emphasis on Saudi Arabia: a PRISMA 2020 systematic review (2015–2026).

## 2. Review questions
- **RQ1.** Which forecasting, demand-modelling and tourism–sustainability studies exist for Saudi Arabia and the Middle East, and what settings and methods do they use?
- **RQ2.** How are forecasting studies evaluated: holdout design, benchmarks, accuracy measures, statistical tests, uncertainty?
- **RQ3.** Do forecasting studies incorporate sustainability, and do sustainability studies project forward?
- **RQ4.** Which research agenda follows?

## 3. Eligibility
- Peer-reviewed journal articles, 2015–2026, in English.
- Setting: Saudi Arabia, the GCC, MENA, Türkiye, Iran, Iraq or Israel. Multi-country panels count when Middle Eastern units are analysed.
- Quantitative studies in one of three themes:
  - F: forecasting tourism or hospitality outcomes;
  - D: tourism demand modelling;
  - S: tourism with an environmental, social or economic-sustainability variable.
- Exclusion codes R1–R6 are defined in `second_reviewer/INSTRUCTIONS.md`.

## 4. Information sources and search
- **Crossref REST API.** 70 queries (8 concept strings × 4 regional terms, plus 2 strings × 19 location terms). Top 100 records per query; journal articles only; 2015–2026. Searched 5 October 2026.
- **Amendment A1 (revision).** Supplementary searches in Semantic Scholar and OpenAlex using the same concept × location design (`search/extra_db_search.py`).
- **Planned amendment A2.** Scopus and Web of Science with equivalent Boolean strings. This needs institutional access and will be run by the authors.
- **Other methods.** Targeted Crossref title searches seeded by web-search leads.

## 5. Selection
- **Stage 1–2 (automated).** Deduplication by DOI, then keyword filters for tourism, region and method terms (`search/screen.py`, `search/screen_stage2.py`).
- **Stage 3.** Title/abstract screening by reviewer 1, an AI agent with human oversight.
- **Amendment A3.** An independent human reviewer screens all 98 title/abstract records blind. Report Cohen's kappa; resolve disagreements by consensus.
- **Stage 4.** Full-text eligibility assessment of all retrievable reports.

## 6. Data extraction
- **Full-text extraction protocol:** `search/ft_extraction_protocol.md`. It requires a verbatim evidence quote for every item.
- **Items for forecasting studies:** holdout design, horizon, forecast origin, benchmarks, best model, accuracy values, ex-ante forecasts.
- **Items for econometric studies:** estimator, tourism variables, coefficients with sign and significance, whether aviation emissions are included, out-of-sample forecasts.
- **Fallback:** where no full text is available, items are coded from the abstract and flagged.

## 7. Risk of bias
- **Forecasting checklist (F1–F7).** F1 holdout; F2 naïve or seasonal-naïve benchmark; F3 scale-free measure; F4 statistical accuracy test; F5 no information leakage; F6 horizon stated; F7 prediction intervals. Adapted from PROBAST and forecast-evaluation practice.
- **Econometric checklist (E1–E7).** E1 unit-root tests; E2 cointegration or long-run test; E3 structural breaks; E4 cross-sectional dependence or heterogeneity; E5 endogeneity; E6 diagnostics and stability; E7 data source and period.

## 8. Synthesis
- **Descriptive analysis:** year, journal, setting, method family, accuracy measures.
- **Keyword co-occurrence network:** a 28-term controlled vocabulary, applied to titles and abstracts.
- **Thematic synthesis:** by theme, plus a 2×2 cross-classification (forecasting × sustainability content).
- **No meta-analysis:** the studies are too heterogeneous.

## 9. Sensitivity analyses
- **S1.** Add back the excluded growth-nexus studies.
- **S2.** Exclude Türkiye.
- **S3.** Restrict to full-text-confirmed studies.

## 10. Amendments log
| # | Date | Amendment | Reason |
|---|---|---|---|
| A0 | 2026-10-05 | Network policy blocked publisher full texts, so screening and extraction were done at abstract level | environment constraint |
| A1 | 2026-10-06 | Supplementary searches in Semantic Scholar and OpenAlex | referee M1 |
| A3 | 2026-10-06 | Blind second-reviewer screening of all 98 records | referee M3 |
| A4 | 2026-10-06 | Full-text extraction and risk of bias for all retrieved studies | referees M2, M4 |
| A5 | 2026-10-06 | Second-pass check of R3 exclusions found and corrected one error (Jamel 2020, CO2 variable) | quality control |
| A6 | 2026-10-06 | Sensitivity analyses S1–S3 | referees M5, M8 |

## 11. Data and code
Repository `review/`. Before submission, deposit a versioned snapshot on Zenodo or OSF to obtain a DOI.
