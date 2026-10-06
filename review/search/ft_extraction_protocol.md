# Full-text extraction and risk-of-bias protocol (v1, 2026-10-06)

Read each assigned full text (`pdftotext -layout <file> -` for PDFs). Extract ONLY what the paper states.
- Every non-trivial field must carry an `evidence` quote (verbatim, ≤ 30 words) with page number if visible.
- If the paper does not state it: `"n/r"`. Never infer, never compute values the paper does not report.
- Numbers must be copied exactly as printed (keep units, decimals).

## Output: one JSON object per study (list), schema

```json
{
 "key": "...", "file": "...", "theme_confirmed": "F|D|S|mismatch (explain)",
 "setting": "...", "data_source": "...", "period": "...", "frequency": "...", "n_obs": "...",
 "outcome_variables": ["..."], "methods": ["..."],
 "F": {                                  // only for forecasting studies (theme F); else null
   "holdout": {"value": "Yes|No|Unclear", "detail": "train/test periods", "evidence": "..."},
   "horizon": "...", "forecast_origin": "fixed|rolling|recursive|n/r",
   "benchmarks": ["e.g. naive, seasonal naive, ARIMA"],
   "best_model": "...",
   "accuracy": [{"model": "...", "measure": "MAPE|RMSE|MAE|MASE|...", "value": "...", "set": "test|train|n/r", "evidence": "..."}],
   "ex_ante_forecast": {"value": "Yes|No", "detail": "period forecast beyond data", "evidence": "..."},
   "sustainability_variables": "none|list"
 },
 "E": {                                  // only for D and S studies; else null
   "estimator": "...", "tourism_variables": ["..."], "dependent_variable": "...",
   "key_results": [{"variable": "...", "horizon": "long-run|short-run|n/a", "coefficient": "...", "sign": "+|-|ns", "significance": "...", "evidence": "..."}],
   "aviation_emissions_included": "Yes|No|n/r|n/a",
   "out_of_sample_forecast": {"value": "Yes|No", "evidence": "..."}
 },
 "rob_forecasting": {   // theme F only (else null). Each item: {"rating": "Yes|No|Unclear", "evidence": "..."}
   "F1_holdout_reported": {}, "F2_naive_or_seasonal_naive_benchmark": {}, "F3_scale_free_or_relative_measure": {},
   "F4_statistical_test_of_accuracy": {}, "F5_no_information_leakage": {}, "F6_horizon_specified": {}, "F7_prediction_intervals": {}
 },
 "rob_econometric": {   // themes D and S only (else null)
   "E1_unit_root_tests": {}, "E2_cointegration_or_long_run_test": {}, "E3_structural_breaks": {},
   "E4_cross_sectional_dependence_or_heterogeneity": {"rating": "Yes|No|Unclear|NA (not panel)"},
   "E5_endogeneity_or_omitted_variables_addressed": {}, "E6_diagnostics_stability": {}, "E7_data_source_and_period": {}
 },
 "notes": "anything affecting eligibility or interpretation"
}
```

Rating guidance:
- F1 Yes = an explicit out-of-sample / test period is described.  F2 Yes = naive, seasonal naive or random walk benchmark included.
- F3 Yes = MAPE/MASE/sMAPE/Theil U or relative skill reported.  F4 Yes = Diebold–Mariano, MCS or another formal accuracy test.
- F5 Yes = predictors used for test-period forecasts are known at forecast origin (or univariate); No = contemporaneous exogenous
  regressors' actual future values used without saying so; Unclear otherwise.  F6 Yes = horizon(s) stated.  F7 Yes = intervals/densities.
- E1 unit-root tests reported; E2 cointegration/bounds/long-run test; E3 break tests or break dummies; E4 CSD/slope heterogeneity tests
  (panels) else NA; E5 IV/GMM/DOLS/controls justified; E6 residual diagnostics or CUSUM; E7 data source and period stated.
