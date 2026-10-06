"""Figures in the style of the competing reviews (trend, journals, countries, methods-by-year,
performance measures, keyword co-occurrence network). All computed from data/included.json and
the Crossref titles/abstracts of the included studies. Output: paper/figs/*.pdf"""
import json, re, html, collections as C, itertools, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

os.makedirs("paper/figs", exist_ok=True)
inc = json.load(open("data/included.json")); cand = json.load(open("data/candidates_eligibility.json"))
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e4e3dd"
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"      # validated categorical slots 1-4 (light)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "pdf.fonttype": 42})
THEME = {"F": ("Forecasting", S1), "D": ("Demand modelling", S2), "S": ("Sustainability", S3)}

def abstract(i): return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", cand[i["doi"]].get("abstract") or ""))
def save(fig, name): fig.savefig(f"paper/figs/{name}.pdf", bbox_inches="tight"); plt.close(fig)

# --- Fig: annual publications by theme (stacked bars, 2px gaps via white edges, totals labelled)
years = list(range(2016, 2027)); fig, ax = plt.subplots(figsize=(6.2, 2.8)); bottom = [0] * len(years)
for t, (lab, col) in THEME.items():
    v = [sum(1 for i in inc if i["year"] == y and i["theme"] == t) for y in years]
    ax.bar(years, v, bottom=bottom, color=col, edgecolor="white", linewidth=1.2, width=0.7, label=lab)
    bottom = [b + x for b, x in zip(bottom, v)]
for y, b in zip(years, bottom):
    if b: ax.text(y, b + 0.15, str(b), ha="center", va="bottom", color=INK, fontsize=8)
ax.set_xticks(years); ax.set_ylabel("Number of studies"); ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(ncol=3, loc="upper left", fontsize=8); ax.set_ylim(0, max(bottom) + 2); save(fig, "fig_trend")

# --- Fig: journals (top sources; others pooled)
def jn(j): return html.unescape(j).replace("&amp;", "&").strip()
jc = C.Counter(jn(i["journal"]) for i in inc); top = [(j, n) for j, n in jc.most_common() if n >= 2]
other = sum(n for j, n in jc.items() if n < 2)
lab = [j for j, _ in top][::-1] + []; val = [n for _, n in top][::-1]
fig, ax = plt.subplots(figsize=(6.2, 0.32 * (len(top) + 1) + 0.6))
ax.barh([f"Other journals ({sum(1 for n in jc.values() if n < 2)} titles, 1 study each)"] + lab, [other] + val, color=S1, height=0.6)
for k, v in enumerate([other] + val): ax.text(v + 0.2, k, str(v), va="center", color=INK, fontsize=8)
ax.set_xlabel("Number of studies"); ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True); save(fig, "fig_journals")

# --- Fig: setting (country / region), stacked by theme
def setting(c):
    for k in ["Saudi Arabia", "Turkiye", "Morocco", "Iran", "Iraq", "Jordan", "Tunisia", "Qatar"]:
        if c.startswith(k) or c.startswith(k.split()[0]): return "Türkiye" if k == "Turkiye" else k
    if c.startswith("UAE"): return "UAE"
    if "GCC" in c: return "GCC (multi-country)"
    return "Middle East / MENA (multi-country)"
sets = C.Counter(setting(i["country"]) for i in inc); order = [s for s, _ in sets.most_common()][::-1]
fig, ax = plt.subplots(figsize=(6.2, 0.3 * len(order) + 0.7)); left = [0] * len(order)
for t, (labt, col) in THEME.items():
    v = [sum(1 for i in inc if setting(i["country"]) == s and i["theme"] == t) for s in order]
    ax.barh(order, v, left=left, color=col, edgecolor="white", linewidth=1.2, height=0.6, label=labt); left = [a + b for a, b in zip(left, v)]
for k, v in enumerate(left): ax.text(v + 0.2, k, str(v), va="center", color=INK, fontsize=8)
ax.set_xlabel("Number of studies"); ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True); ax.legend(loc="lower right", fontsize=8)
save(fig, "fig_settings")

# --- Fig: forecasting method family by year (cf. Dowlut et al. Fig. 5; Song et al. Fig. 2)
F = [i for i in inc if i["theme"] == "F"]
FAM = {"C": ("Classical (time series / econometric)", S1), "M": ("Machine / deep learning", S2), "H": ("Hybrid, ensemble or multi-family", S3), "G": ("Grey models", S4)}
fy = sorted({i["year"] for i in F}); fig, ax = plt.subplots(figsize=(6.2, 2.6)); bottom = [0] * len(fy)
for f, (labf, col) in FAM.items():
    v = [sum(1 for i in F if i["year"] == y and i["family"] == f) for y in fy]
    ax.bar([str(y) for y in fy], v, bottom=bottom, color=col, edgecolor="white", linewidth=1.2, width=0.6, label=labf); bottom = [a + b for a, b in zip(bottom, v)]
for k, b in enumerate(bottom): ax.text(k, b + 0.08, str(b), ha="center", va="bottom", fontsize=8, color=INK)
ax.set_ylabel("Forecasting studies"); ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True); ax.set_ylim(0, max(bottom) + 1.2)
ax.legend(ncol=2, loc="upper left", fontsize=7.5); save(fig, "fig_methods_year")

# --- Fig: accuracy measures reported by forecasting studies (full text where extracted, else abstract; cf. Dowlut et al. Fig. 4)
meas = ["MAPE", "RMSE", "MAE", "R2", "MSE", "sMAPE", "MAD", "Theil's U"]
known = [i for i in F if i["metrics"] not in ("n/r",) or i.get("coding_source") == "full text"]
mc = {m: sum(1 for i in known if m in [x.strip() for x in i["metrics"].split(",")]) for m in meas}
none = sum(1 for i in known if i["metrics"] == "n/r")
items = sorted([(k.replace("R2", "R²"), v) for k, v in mc.items() if v], key=lambda x: x[1]); items = [("None reported", none)] + items
fig, ax = plt.subplots(figsize=(6.2, 2.4))
ax.barh([k for k, _ in items], [v for _, v in items], color=[MUTED] + [S1] * (len(items) - 1), height=0.6)
for k, (_, v) in enumerate(items): ax.text(v + 0.1, k, str(v), va="center", fontsize=8, color=INK)
ax.set_xlabel(f"Forecasting studies with assessable reporting (n = {len(known)}; full text for {sum(1 for i in known if i.get('coding_source') == 'full text')})")
ax.xaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
save(fig, "fig_measures")
withab = known

# --- Fig: keyword co-occurrence network (controlled vocabulary over titles + abstracts)
VOC = {"tourism demand": r"tourism demand|demand for tourism", "tourist arrivals": r"tourist arrivals|international arrivals|visitor", "forecasting": r"forecast",
 "machine learning": r"machine learning|random forest|gradient boosting|xgboost|extra trees|svr|support vector", "deep learning / ANN": r"deep learning|lstm|neural network|\bann\b",
 "ARIMA / SARIMA": r"arima", "ARDL / cointegration": r"ardl|cointegrat|bounds test", "causality": r"causality|granger", "panel data": r"panel",
 "CO2 emissions": r"co2|co 2|carbon|emission", "EKC": r"kuznets", "energy": r"energy|fossil|electricity|petroleum", "economic growth": r"economic growth|gdp",
 "sustainability": r"sustainab", "climate": r"climat", "COVID-19": r"covid|pandemic", "Vision 2030": r"vision 2030", "religious tourism": r"religious|pilgrim|hajj|umrah|arbaeen",
 "oil price": r"oil price", "geopolitical risk": r"geopolitic|political risk|instability|crisis", "hotel": r"hotel", "search data": r"google|search quer|search data|internet search",
 "Saudi Arabia": r"saudi|makkah", "Türkiye": r"turk", "GCC": r"\bgcc\b|gulf", "seasonality": r"seasonal", "infrastructure": r"infrastructure", "income / equality": r"income equal|inequal|income distribution"}
docs = [(" ".join(cand[i["doi"]]["title"]) + " " + abstract(i)).lower() for i in inc]
occ = {k: {d for d, t in enumerate(docs) if re.search(p, t, re.I)} for k, p in VOC.items()}
G = nx.Graph()
for k, s in occ.items():
    if len(s) >= 3: G.add_node(k, n=len(s))
for a, b in itertools.combinations(list(G.nodes), 2):
    w = len(occ[a] & occ[b])
    if w >= 2: G.add_edge(a, b, w=w)
G.remove_nodes_from([n for n in list(G.nodes) if G.degree(n) == 0])
comms = sorted(nx.algorithms.community.greedy_modularity_communities(G, weight="w"), key=len, reverse=True)
cmap = {n: [S1, S2, S3, S4][min(ci, 3)] for ci, c in enumerate(comms) for n in c}
pos = nx.kamada_kawai_layout(G, weight=None)
fig, ax = plt.subplots(figsize=(7.0, 6.0)); ax.axis("off")
for a, b, d in G.edges(data=True):
    ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color="#b9b8b0", lw=0.3 + 0.25 * d["w"], alpha=0.7, zorder=1)
for n, d in G.nodes(data=True):
    ax.scatter(*pos[n], s=40 + 22 * d["n"], color=cmap[n], edgecolor="white", linewidth=1.5, zorder=2)
    ax.text(pos[n][0], pos[n][1] - 0.06, f"{n} ({d['n']})", ha="center", va="top", fontsize=7.2, color=INK, zorder=3)
save(fig, "fig_keywords")
json.dump({"nodes": {n: d["n"] for n, d in G.nodes(data=True)}, "edges": [(a, b, d["w"]) for a, b, d in G.edges(data=True)],
           "clusters": [sorted(c) for c in comms], "vocabulary": VOC, "journals": jc, "settings": sets, "measures": mc, "measures_none": none,
           "n_with_abstract_F": len(withab)}, open("data/figure_data.json", "w"), indent=1, ensure_ascii=False)
print("clusters:", [sorted(c) for c in comms]); print("journals:", top, "other", other); print("measures", mc, "none", none)
