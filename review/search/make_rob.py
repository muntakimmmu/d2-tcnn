"""Integrate full-text extractions (data/ft_extract_*.json): risk-of-bias traffic-light figures (robvis style),
summary tables for the paper (paper/tab_rob_f.tex, paper/tab_rob_e.tex, paper/tab_results_s.tex) and numbers (data/ft_summary.json)."""
import json, glob, re
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ex = [r for f in sorted(glob.glob("data/ft_extract_*.json")) for r in json.load(open(f))]
inc = {i["key"]: i for i in json.load(open("data/included.json"))}
ex = [r for r in ex if r["key"] in inc]                      # Triki2019 excluded at full text
INK, GRID = "#1f1f1e", "#e4e3dd"
COL = {"Yes": "#1baf7a", "No": "#e34948", "Unclear": "#eda100", "NA": "#d9d8d2"}
SYM = {"Yes": "+", "No": "–", "Unclear": "?", "NA": ""}
def rating(x):
    r = (x or {}).get("rating", "Unclear") if isinstance(x, dict) else "Unclear"
    r = str(r)
    return "NA" if r.upper().startswith("NA") else ("Yes" if r.startswith("Yes") else "No" if r.startswith("No") else "Unclear")
def tx(s):
    s = str(s)
    for a, b in [("\\", "\\textbackslash{}"), ("&", "\\&"), ("%", "\\%"), ("_", "\\_"), ("#", "\\#"), ("$", "\\$"), ("~", "\\textasciitilde{}")]: s = s.replace(a, b)
    return s

def traffic(items, keys, labels, fname, title):
    fig, ax = plt.subplots(figsize=(6.4, 0.32 * len(items) + 1.2))
    for y, r in enumerate(items):
        for x, k in enumerate(keys):
            v = rating(r[k]); ax.scatter(x, y, s=170, color=COL[v], edgecolor="white", linewidth=1.5, zorder=2)
            ax.text(x, y, SYM[v], ha="center", va="center", color="white", fontsize=8, fontweight="bold", zorder=3)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([re.sub(r"(\d{4})", r" (\1)", r["key"]) for r in items], fontsize=8)
    ax.set_xticks(range(len(keys))); ax.set_xticklabels(labels, fontsize=8); ax.xaxis.tick_top()
    ax.set_xlim(-0.6, len(keys) - 0.4); ax.set_ylim(len(items) - 0.5, -0.5)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
    for lab, c in [("Yes (low concern)", COL["Yes"]), ("No (high concern)", COL["No"]), ("Unclear", COL["Unclear"]), ("Not applicable", COL["NA"])]:
        ax.scatter([], [], color=c, s=60, label=lab)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.02), fontsize=7.5, frameon=False)
    fig.savefig(f"paper/figs/{fname}.pdf", bbox_inches="tight"); plt.close(fig)

FK = ["F1_holdout_reported", "F2_naive_or_seasonal_naive_benchmark", "F3_scale_free_or_relative_measure", "F4_statistical_test_of_accuracy",
      "F5_no_information_leakage", "F6_horizon_specified", "F7_prediction_intervals"]
EK = ["E1_unit_root_tests", "E2_cointegration_or_long_run_test", "E3_structural_breaks", "E4_cross_sectional_dependence_or_heterogeneity",
      "E5_endogeneity_or_omitted_variables_addressed", "E6_diagnostics_stability", "E7_data_source_and_period"]
F = sorted([dict(key=r["key"], **r["rob_forecasting"]) for r in ex if r.get("rob_forecasting")], key=lambda r: r["key"])
E = sorted([dict(key=r["key"], **r["rob_econometric"]) for r in ex if r.get("rob_econometric")], key=lambda r: r["key"])
traffic(F, FK, ["F1\nholdout", "F2\nnaïve\nbenchm.", "F3\nscale-free\nmeasure", "F4\naccuracy\ntest", "F5\nno\nleakage", "F6\nhorizon", "F7\nintervals"], "fig_rob_f", "")
traffic(E, EK, ["E1\nunit\nroot", "E2\ncointegr.", "E3\nbreaks", "E4\nCSD /\nhetero.", "E5\nendo-\ngeneity", "E6\ndiagn.", "E7\ndata"], "fig_rob_e", "")
summ = {"n_fulltext": len(ex), "nF": len(F), "nE": len(E),
        "F": {k: {v: sum(1 for r in F if rating(r[k]) == v) for v in COL} for k in FK},
        "E": {k: {v: sum(1 for r in E if rating(r[k]) == v) for v in COL} for k in EK}}
# accuracy table (theme F): best model and its reported accuracy, holdout, benchmark
rows = []
for r in sorted([r for r in ex if r.get("F")], key=lambda r: r["key"]):
    f = r["F"]; acc = [a for a in f.get("accuracy", []) if str(a.get("model", "")).strip()]
    best = f.get("best_model", "n/r"); bacc = [a for a in acc if best and str(best).lower()[:10] in str(a.get("model", "")).lower()] or acc[:1]
    accs = "; ".join(f"{a.get('measure')} {a.get('value')}" + (f" ({a.get('set')})" if a.get("set") not in (None, "n/r") else "") for a in bacc[:2]) or "n/r"
    rows.append(f"\\citet{{{r['key']}}} & {tx(best)[:60]} & {tx(accs)[:70]} & {tx(', '.join(f.get('benchmarks') or []))[:60] or 'n/r'} & {tx(f.get('ex_ante_forecast', {}).get('value', 'n/r'))} \\\\")
open("paper/tab_results_f.tex", "w").write("\\begin{tabular}{@{}p{3.2cm}p{4.2cm}p{4.6cm}p{5.0cm}p{1.6cm}@{}}\n\\toprule\nStudy & Best model (as reported) & Reported accuracy & Comparison models & Ex-ante forecast\\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
# econometric key results (themes D, S): tourism variable effects
rows = []; signs = {"+": 0, "-": 0, "ns": 0}
for r in sorted([r for r in ex if r.get("E")], key=lambda r: (inc[r["key"]]["theme"], r["key"])):
    e = r["E"]; kr = [k for k in e.get("key_results", []) if k.get("horizon") in ("long-run", "n/a", None)] or e.get("key_results", [])
    txt = "; ".join(f"{k.get('variable')}: {k.get('coefficient')} ({k.get('sign')}{', ' + str(k.get('significance')) if k.get('significance') not in (None, 'n/r') else ''})" for k in kr[:2]) or "n/r"
    for k in kr[:1]:
        s = str(k.get("sign", "")).strip(); signs["+" if s.startswith("+") else "-" if s.startswith("-") else "ns"] += 1
    rows.append(f"\\citet{{{r['key']}}} & {inc[r['key']]['theme']} & {tx(e.get('estimator', 'n/r'))[:45]} & {tx(e.get('dependent_variable', 'n/r'))[:45]} & {tx(txt)[:120]} & {tx(e.get('aviation_emissions_included', 'n/r'))} \\\\")
open("paper/tab_results_e_auto.tex", "w").write("\\begin{tabular}{@{}p{3.0cm}p{0.7cm}p{3.2cm}p{3.3cm}p{6.4cm}p{1.4cm}@{}}\n\\toprule\nStudy & Theme & Estimator & Dependent variable & First reported tourism effect (coefficient, sign, significance) & Aviation incl.\\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
summ["first_effect_signs"] = signs
json.dump(summ, open("data/ft_summary.json", "w"), indent=1); print(json.dumps(summ, indent=1))
