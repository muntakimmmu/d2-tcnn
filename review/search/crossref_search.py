"""PRISMA 2020 identification stage: reproducible Crossref search.
Logs every query, date, hit count; dedups by DOI; writes records + log."""
import json, time, urllib.parse, urllib.request, datetime, os, sys
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
MAILTO = "muntakim.iot@gmail.com"
FROM, UNTIL = "2015-01-01", "2026-12-31"
REGION = ["Saudi Arabia", "Saudi", "Kingdom of Saudi Arabia", "Hajj", "Umrah", "Makkah", "Mecca",
          "Gulf Cooperation Council", "GCC", "Middle East", "MENA", "Dubai", "UAE", "United Arab Emirates",
          "Qatar", "Oman", "Bahrain", "Kuwait", "Jordan", "Egypt", "Turkey", "Iran", "Morocco", "Tunisia", "Lebanon", "Israel"]
CORE = [
 "tourism demand forecasting", "tourist arrivals forecasting", "tourism forecasting machine learning",
 "tourism forecasting deep learning", "hotel occupancy forecasting", "tourism sustainability prediction",
 "tourism CO2 emissions", "sustainable tourism modelling",
]
QUERIES = []
for r in ["Saudi Arabia", "Middle East", "GCC", "Hajj Umrah"]:
    for c in CORE: QUERIES.append(f"{c} {r}")
for r in REGION[7:]:
    QUERIES.append(f"tourism demand forecasting {r}")
    QUERIES.append(f"tourism sustainability {r}")
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": f"prisma-review/1.0 (mailto:{MAILTO})"}), timeout=40) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 * (i + 1)); err = e
    print("FAIL", url, err, file=sys.stderr); return None
records, log = {}, []
for q in QUERIES:
    params = {"query.bibliographic": q, "rows": 100, "filter": f"from-pub-date:{FROM},until-pub-date:{UNTIL},type:journal-article",
              "select": "DOI,title,author,issued,container-title,volume,issue,page,article-number,abstract,type,publisher,subject,is-referenced-by-count", "mailto": MAILTO}
    d = get("https://api.crossref.org/works?" + urllib.parse.urlencode(params))
    items = d["message"]["items"] if d else []
    total = d["message"]["total-results"] if d else None
    log.append({"query": q, "date": datetime.date.today().isoformat(), "total_results_reported": total, "retrieved": len(items)})
    for it in items:
        records.setdefault(it["DOI"].lower(), it)
    print(q, len(items), "unique so far", len(records), flush=True); time.sleep(0.5)
json.dump(records, open(os.path.join(OUT, "crossref_raw.json"), "w"))
json.dump({"database": "Crossref REST API", "filter": f"{FROM}..{UNTIL}, journal-article", "queries": log,
           "n_retrieved_total": sum(l["retrieved"] for l in log), "n_unique_doi": len(records)}, open(os.path.join(OUT, "search_log.json"), "w"), indent=1)
