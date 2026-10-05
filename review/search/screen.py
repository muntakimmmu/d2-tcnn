"""Stage 2: rule-based title/abstract screening (transparent, reproducible). Human-style judgment applied afterwards to survivors."""
import json, re, collections
R = json.load(open("data/crossref_raw.json"))
TOUR = re.compile(r"touris|hajj|umrah|pilgrim|hotel|hospitality|visitor|travel|destination|airline|aviation", re.I)
FORE = re.compile(r"forecast|predict|time[- ]series|arima|lstm|neural|machine learning|deep learning|regression|ardl|econometric|projection|scenario|model", re.I)
SUST = re.compile(r"sustainab|carbon|co2|emission|environment|vision 2030|sdg|green|eco", re.I)
REG = re.compile(r"saudi|ksa|makkah|mecca|medina|hajj|umrah|neom|alula|red sea|gulf|gcc|middle east|mena|arab|dubai|abu dhabi|uae|emirates|qatar|oman|bahrain|kuwait|jordan|egypt|turk|t[uü]rkiye|iran|morocc|tunis|leban|israel|palestin|iraq|algeria", re.I)
def txt(r):
    t = " ".join(r.get("title") or []); a = re.sub("<[^>]+>", " ", r.get("abstract") or "")
    return t, a
out, stats = [], collections.Counter()
stats["identified_unique"] = len(R)
for doi, r in R.items():
    t, a = txt(r); full = t + " " + a
    year = (r.get("issued", {}).get("date-parts") or [[None]])[0][0]
    if not r.get("title"): stats["excl_no_title"] += 1; continue
    if not TOUR.search(full): stats["excl_not_tourism"] += 1; continue
    if not REG.search(full): stats["excl_no_region_signal"] += 1; continue
    if not (FORE.search(full) or SUST.search(full)): stats["excl_no_forecast_or_sust"] += 1; continue
    r["_year"] = year; r["_has_abs"] = bool(a); r["_forecast"] = bool(FORE.search(full)); r["_sust"] = bool(SUST.search(full)); r["_saudi"] = bool(re.search(r"saudi|ksa|makkah|mecca|hajj|umrah|neom|alula|red sea", full, re.I))
    out.append(r)
stats["passed_rule_screen"] = len(out)
stats["passed_with_abstract"] = sum(r["_has_abs"] for r in out)
stats["passed_saudi"] = sum(r["_saudi"] for r in out)
json.dump(out, open("data/screen_pass.json", "w"))
json.dump(stats, open("data/screen_stats.json", "w"), indent=1); print(json.dumps(stats, indent=1))
