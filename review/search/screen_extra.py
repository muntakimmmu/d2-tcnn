"""Screen supplementary-database records (data/extra_db/records.json) with the SAME rules as screen.py + screen_stage2.py.
Records already in the Crossref set (by DOI) are counted as duplicates. Survivors go to manual eligibility (data/extra_db/stage2.json)."""
import json, re
recs = json.load(open("data/extra_db/records.json")); raw = json.load(open("data/crossref_raw.json"))
TOUR = re.compile(r"touris|hajj|umrah|pilgrim|hotel|hospitality|visitor|travel|destination|airline|aviation", re.I)
FORE = re.compile(r"forecast|predict|time[- ]series|arima|lstm|neural|machine learning|deep learning|regression|ardl|econometric|projection|scenario|model", re.I)
SUST = re.compile(r"sustainab|carbon|co2|emission|environment|vision 2030|sdg|green|eco", re.I)
REG = re.compile(r"saudi|ksa|makkah|mecca|medina|hajj|umrah|neom|alula|red sea|gulf|gcc|middle east|mena|arab|dubai|abu dhabi|uae|emirates|qatar|oman|bahrain|kuwait|jordan|egypt|turk|t[uü]rkiye|iran|morocc|tunis|leban|israel|palestin|iraq|algeria", re.I)
F2 = re.compile(r"forecast|predict|time[- ]series|arima|lstm|neural network|machine learning|deep learning|ardl|cointegrat|causality|econometric|panel data|projection|random forest|regression|quantile|gmm|fmols|dols|kuznets|simulation", re.I)
st = {"identified_unique": len(recs), "duplicates_of_crossref": 0, "excl_not_tourism": 0, "excl_no_region": 0, "excl_no_forecast_sust": 0, "excl_stage2": 0, "excl_year": 0}
keep = {}
for d, r in recs.items():
    if d in raw: st["duplicates_of_crossref"] += 1; continue
    if not r.get("year") or not (2015 <= int(r["year"]) <= 2026): st["excl_year"] += 1; continue
    t = (r.get("title") or "") + " " + (r.get("abstract") or "")
    if not TOUR.search(t): st["excl_not_tourism"] += 1; continue
    if not REG.search(t): st["excl_no_region"] += 1; continue
    if not (FORE.search(t) or SUST.search(t)): st["excl_no_forecast_sust"] += 1; continue
    if not F2.search(t): st["excl_stage2"] += 1; continue
    keep[d] = r
st["to_manual_eligibility"] = len(keep)
json.dump(keep, open("data/extra_db/stage2.json", "w"), indent=1); json.dump(st, open("data/extra_db/screen_stats.json", "w"), indent=1)
print(json.dumps(st))
for d, r in keep.items(): print(r.get("year"), d, "|", (r.get("title") or "")[:100], "|", (r.get("venue") or "")[:30], "| abs" if r.get("abstract") else "")
