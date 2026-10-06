# Independent second-reviewer screening (addresses referee comment M3)

**Who:** a human reviewer who has **not** seen the AI decisions. Do not open `ai_answer_key_DO_NOT_SHARE.json`.

**What:** `screening_blind.csv` holds all 98 records that reached title/abstract screening, in random order. For each row, fill:
- `DECISION (Include/Exclude)`
- `THEME if include`: F = forecasting a tourism or hospitality outcome; D = modelling tourism demand or outcomes without a forecasting objective; S = quantitative tourism study with an environmental, social or economic-sustainability variable.
- `REASON CODE if exclude`, one of:
  - R1: outside the Middle East (Saudi Arabia, GCC, MENA, Türkiye, Iran, Iraq, Israel)
  - R2: not a quantitative forecasting, demand or sustainability study (perception or SEM survey, qualitative, conceptual, educational, technical non-tourism)
  - R3: tourism–growth nexus only, with no demand outcome and no sustainability variable
  - R4: operational, crowd or health prediction
  - R5: non-English record or conference proceedings
  - R6: region or tourism link cannot be determined from the record

Inclusion also requires a peer-reviewed journal article published 2015–2026 (paper Table 3).

**Time needed:** about 2–3 hours.

**Save as:** `screening_blind_<your initials>.csv`.

**Then run:**

```bash
python3 search/kappa.py prisma/second_reviewer/screening_blind_<initials>.csv
```

This reports Cohen's kappa with a 95% bootstrap confidence interval and writes `disagreements.csv`. Resolve each disagreement by discussion, or with a third person, and record the outcome in the `consensus` column. The paper reports the kappa value and any decisions that change.

**Optional: extraction check.** Independently extract the same items for 5 full texts, chosen with the random seed in this note: `random.Random(2026).sample(full-text list, 5)`. Use the protocol in `search/ft_extraction_protocol.md`, then compare with `data/ft_extract_*.json`.
