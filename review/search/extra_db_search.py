"""M1: supplementary database searches (Semantic Scholar Graph API bulk search; OpenAlex) with patient backoff.
Same concept x location design as the Crossref search, restricted to journal articles 2015-2026. Logs every attempt."""
import json, time, urllib.request, urllib.parse, os, sys, datetime
OUT = "data/extra_db"; os.makedirs(OUT, exist_ok=True)
CON = ["tourism demand forecasting", "tourist arrivals forecasting", "tourism forecasting machine learning", "hotel occupancy forecasting",
       "tourism CO2 emissions", "sustainable tourism", "tourism environmental Kuznets curve", "tourism carbon emissions ARDL"]
LOC = ["Saudi Arabia", "Middle East", "GCC", "Hajj Umrah", "UAE", "Qatar", "Oman", "Jordan", "Egypt", "Turkey", "Iran", "Morocco", "Tunisia", "Bahrain", "Kuwait", "Lebanon", "Iraq"]
Q = [f"{c} {l}" for c in CON[:4] for l in LOC] + [f"{c} {l}" for c in CON[4:] for l in LOC]
def get(url, tries=12):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "prisma-review (mailto:muntakim.iot@gmail.com)"}), timeout=60) as r:
                return json.load(r), None
        except Exception as e:
            err = str(e); time.sleep(min(600, 30 * (i + 1)))
    return None, err
log = json.load(open(f"{OUT}/log.json")) if os.path.exists(f"{OUT}/log.json") else []
done = {(l["db"], l["query"]) for l in log if l.get("ok")}
recs = json.load(open(f"{OUT}/records.json")) if os.path.exists(f"{OUT}/records.json") else {}
for db in sys.argv[1:] or ["s2"]:
    for q in Q:
        if (db, q) in done: continue
        if db == "s2":
            u = "https://api.semanticscholar.org/graph/v1/paper/search/bulk?" + urllib.parse.urlencode({"query": q, "year": "2015-2026",
                "publicationTypes": "JournalArticle", "fields": "title,year,externalIds,venue,abstract,publicationTypes"})
            d, err = get(u); items = (d or {}).get("data", [])[:100] if d else []
            hits = (d or {}).get("total")
            for it in items:
                doi = ((it.get("externalIds") or {}).get("DOI") or "").lower()
                if doi: recs.setdefault(doi, {"title": it.get("title"), "year": it.get("year"), "venue": it.get("venue"), "abstract": it.get("abstract"), "dbs": []})["dbs"].append("s2")
        else:
            u = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": q, "per-page": 100, "mailto": "muntakim.iot@gmail.com",
                "filter": "from_publication_date:2015-01-01,to_publication_date:2026-12-31,type:article"})
            d, err = get(u); items = (d or {}).get("results", []) if d else []; hits = ((d or {}).get("meta") or {}).get("count")
            for it in items:
                doi = (it.get("doi") or "").replace("https://doi.org/", "").lower()
                if doi:
                    ab = it.get("abstract_inverted_index") or {}
                    words = sorted(((p, w) for w, ps in ab.items() for p in ps)); abstract = " ".join(w for _, w in words) or None
                    recs.setdefault(doi, {"title": it.get("title"), "year": it.get("publication_year"), "venue": ((it.get("primary_location") or {}).get("source") or {}).get("display_name"), "abstract": abstract, "dbs": []})["dbs"].append("openalex")
        log.append({"db": db, "query": q, "ok": d is not None, "reported_total": hits, "retrieved": len(items), "error": None if d else err, "time": datetime.datetime.utcnow().isoformat()})
        json.dump(log, open(f"{OUT}/log.json", "w"), indent=1); json.dump(recs, open(f"{OUT}/records.json", "w"))
        print(db, q, len(items), "unique", len(recs), flush=True); time.sleep(4 if db == "s2" else 1)
