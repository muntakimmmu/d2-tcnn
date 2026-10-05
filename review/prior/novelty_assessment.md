# Novelty and contribution assessment of the review

Assessment date: 2026-10-05. Scope: the PRISMA 2020 review in `review/paper/main.tex`.
Labels: **KNOWN** (from a verified source), **OBSERVED** (from our coded data), **HYPOTHESIZED**, **NOT YET VERIFIED**.

## 1. Question
Is the review novel compared with the closest existing reviews, and is it a PhD-level contribution?

**Short answer.** The review has a defensible *scope and synthesis* novelty. It is not yet PhD-level or Q1-ready. Three items lower its standing: the coding is abstract-level only, it used a single database and a single reviewer, and its research agenda partly overlaps existing carrying-capacity early-warning work. Verdict: **MODIFY** (Section 9).

## 2. Prior-review search (Agent B: prior-art collision)
- **Crossref search:** 24 logged queries in `prior/prior_search_log.json`, giving 265 titled reviews in `prior/prior_reviews_raw.json`.
- **Targeted checks:** additional regional and carrying-capacity reviews were found by web search.
- **Comparison set:** 25 reviews, each with a Crossref record in `prior/closest_reviews.json`.
- **Scope coding:** taken from the deposited abstract, or from the title when no abstract exists. Two entries rely on web-search snippets and are **NOT YET VERIFIED**: Sun et al. 2022 and Iqbal & Aftab 2025.

## 3. Closest prior work (collision table)

| Our candidate contribution | Closest prior review | Shared component | Actual difference | Collision risk |
|---|---|---|---|---|
| PRISMA review of Gulf/Saudi tourism | Saleh, Bassil & Safari (Tourism Economics 28, 2021/22), PRISMA review of 23 GCC studies, mostly Dubai and planning | Region, PRISMA | They do not indicate a forecasting focus; ours covers 2015–2026, the wider Middle East, 42 studies, and quantitative forecasting plus sustainability | **MEDIUM** |
| Synthesis of tourism–emission econometric studies | Sun, Gössling & Zhou (Annals of Tourism Research 97, 2022), review of 81 econometric studies 2013–2021 [snippet] | Outcome and designs (Theme S) | Theirs is global; ours is regional but shallower (abstract-level). On its own, our Theme S adds little. | **HIGH for Theme S alone** |
| Saudi tourism and sustainability | Iqbal & Aftab (IJSDP 20(3), 2025), SLR on Vision 2030 and SDG 8 [snippet]; Alhejaili & Ahmad (2025), ESG review of Saudi hotels | Country, sustainability | Neither indicates forecasting or quantitative modelling | LOW–MEDIUM |
| Forecasting synthesis | Jiao & Chen 2018; Song et al. 2019; Wu et al. 2023, 2024; Huang & Zheng 2022; Henriques & Nobre Pereira 2024 | Forecasting methods and accuracy | All are global, with no sustainability lens. Our regional forecasting set (16 studies) is small. | LOW for the joint scope; HIGH if presented as a forecasting review alone |
| "Capacity-aware forecasting" agenda | Long et al. (IJERPH 2022) call for dynamic forecasting and early warning of carrying capacity; Ye et al. (Sustainability 2020) forecast early-warning indices with a back-propagation (BP) neural network; Sha (2020) | Idea of forecasting toward capacity limits | Ours derives exceedance probabilities from probabilistic **demand** forecasts and evaluates them for calibration; theirs forecast composite indicator indices | **MEDIUM–HIGH**; reframed in the paper as an extension, not a new idea |
| Forecasting–sustainability disconnect (2×2) and typology of link direction | None located | – | No located review cross-classifies these two literatures for any region | **LOW** (closest: Long 2022, which only calls for the link) |

**Closest paper, P\*:** Saleh et al. (2021) on region and reporting standard, and Sun et al. (2022) on sustainability content. The difference from both can be stated clearly, so Tier 2 (novelty) passes.

## 4. What disappears without this review (Tier 3, the Δ test for reviews)
- Without the joint coding, nobody can see that, within this regional corpus, 1 of 16 forecasting studies includes sustainability and 0 of 26 other studies evaluates forecasts (**OBSERVED**). Separate forecasting reviews and sustainability reviews cannot show this by construction.
- Without the typology of link direction, three distinct directions are blurred together: tourism → environment (Theme S), climate → tourism (Chouari 2025), and forecast load → capacity (absent).
- This is a **genuine but modest** capability. It is a gap map, not a new method.

## 5. Contribution levels (N_P, N_M, N_T, N_E)
- **N_P (problem/scope novelty):** medium. The intersection is new, but each part is well reviewed.
- **N_M (method novelty):** low. Standard PRISMA procedure, weaker than usual (single reviewer, abstract-level).
- **N_T (theory/framework):** low to medium. The typology of link direction is a nascent framework, not yet formalised or validated.
- **N_E (empirical insight):** medium. The disconnect finding plus the regional-versus-global comparison (search-data lag, Saudi shift since Saleh 2021, mixed emission signs echoing Sun 2022).

## 6. Adversarial reviewer report (simulated Q1 referee)
1. *"Abstract-level only."* This is fatal for a Q1 systematic review. Item 19 (results of individual studies) and items 11/18 (risk of bias) cannot be met.
2. *"Crossref only, top 100 per query."* Retrieval is not reproducible to Scopus or Web of Science standards; the recall check found 5 missed included studies.
3. *"Single AI reviewer."* No inter-rater reliability. Many journals now restrict AI-performed screening.
4. *"Small and heterogeneous corpus (42), no quantitative synthesis."* No effect sizes or accuracy pooling.
5. *"Theme S duplicates Sun et al. (2022) regionally."* Justify why a regional subset matters.
6. *"The capacity-aware agenda exists in the early-warning literature."* Partly answered by the new positioning text.
7. *"Disconnect may be an artefact of the eligibility themes."* Studies were coded into F/D/S themes, which mechanically separates them. The 2×2 table uses content flags, not themes, but a referee will still probe this point.

Scores (1–10): originality 6, technical quality 4, significance 6, evidence 4, clarity 7, reproducibility 7. Below 7 on four criteria, so the paper returns for redesign under the skill's rule.

## 7. Rebuttal simulation (evidence-supported only)
- **On 5:** the regional subset shows Saudi growth and pilgrimage-specific emission studies (Naseem 2025; Raihan 2025; Ozturk 2021) that the global review period (2013–2021) only partly covers. This holds only if those papers are confirmed at full text.
- **On 7:** the 2×2 table uses abstract content flags (sustainability variable present; forward projection present) that are independent of the theme label. Chouari (2025) shows that the coding can detect a crossover when one exists.
- **On 1–4:** these cannot be rebutted. They must be fixed (Section 9).

## 8. Scorecard
```text
Importance:                 7/10
Novelty:                    6/10  (scope + synthesis, not method)
Mechanistic clarity:        6/10  (typology of link direction needs formalisation)
Technical depth:            4/10  (abstract-level, no RoB, no pooling)
Evidence potential:         7/10  (high if full-text extraction is done)
Generalization:             5/10
Reproducibility:            7/10  (code + logs in repo)
Computational feasibility:  9/10
Risk of prior-art collision: MEDIUM (Saleh 2021, Sun 2022, early-warning literature)
Overall research potential: 6/10
```

## 9. Verdict: MODIFY
Doing the work below would move the review from a gap map toward a PhD-chapter or Q1 standard:
1. **Full-text, dual-reviewer extraction** for all included studies and a sample of exclusions; report Cohen's κ.
2. **Scopus and Web of Science searches** (plus Arabic sources such as the Saudi Digital Library) with documented strings; rerun the PRISMA flow.
3. **Forecast-evaluation audit** of Theme F: extract horizon, holdout design, benchmark (naïve or seasonal naïve), MAPE/MASE, and tests (Diebold–Mariano, model confidence set). Score risk of bias with a PROBAST adaptation. This turns "reporting transparency" into an evidence-quality finding.
4. **Formalise the typology of link direction** (T→E, E→T, F→C, C→F) as a coding framework with definitions; apply it with two coders.
5. **Sharpen the Theme S contribution against Sun et al. (2022):** report whether regional studies include aviation, and what sign and elasticity they find, with full-text values.
6. **Optional, but the step that would make it original research:** a small empirical demonstration using public Saudi arrivals data and a capacity proxy, comparing exceedance warnings from a probabilistic forecast with an index-based early warning (Ye 2020 style). This would test the agenda rather than only propose it.

## 10. One-sentence test (review version)
> Existing reviews synthesise tourism forecasting (globally) or tourism sustainability (globally, or regionally without forecasting). For Saudi Arabia and the Middle East we show that the two evidence bases are largely disconnected: forecasts ignore sustainability, and sustainability studies do not forecast. We type the missing link and position a probabilistic, capacity-aware agenda against existing early-warning work.

This sentence is defensible now. Whether the paper is "PhD-level" depends on completing items 1–3 above.
