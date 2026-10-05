"""Prior-art search for the closest REVIEW papers (Crossref). Logs queries; keeps records whose title signals a review."""
import json, re, time, urllib.request, urllib.parse, html
Q = ["systematic review tourism demand forecasting","bibliometric analysis tourism demand forecasting","review tourism forecasting machine learning deep learning",
 "review artificial intelligence tourism forecasting","literature review hotel demand forecasting","review big data tourism forecasting",
 "systematic literature review tourism Saudi Arabia","review tourism Saudi Vision 2030 sustainability","systematic review sustainable tourism Middle East",
 "review tourism research Gulf Cooperation Council","bibliometric tourism Middle East","systematic review tourism carbon emissions",
 "review tourism environment nexus","meta-analysis tourism emissions economic growth","systematic review religious tourism Hajj Umrah",
 "review sustainable tourism indicators","review tourism carrying capacity overtourism","systematic review tourism sustainability forecasting",
 "review smart tourism artificial intelligence sustainability","scoping review tourism demand forecasting","review tourism forecasting COVID-19 recovery",
 "review halal tourism", "review tourism MENA region", "review probabilistic tourism forecasting interval"]
REV = re.compile(r"review|bibliometric|meta-analys|state of the art|survey|overview|systematic|scoping|mapping", re.I)
out, log = {}, []
for q in Q:
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": 40, "filter": "from-pub-date:2014-01-01,type:journal-article",
        "select": "DOI,title,author,issued,container-title,volume,page,article-number,abstract,is-referenced-by-count", "mailto": "muntakim.iot@gmail.com"})
    items = json.load(urllib.request.urlopen(u, timeout=40))["message"]["items"]
    k = [it for it in items if REV.search(" ".join(it.get("title", [""])))]
    log.append({"query": q, "retrieved": len(items), "review_titled": len(k)})
    for it in k: out.setdefault(it["DOI"].lower(), it)
    time.sleep(0.4)
json.dump(out, open("prior/prior_reviews_raw.json", "w")); json.dump(log, open("prior/prior_search_log.json", "w"), indent=1)
print(len(out))
for d, it in sorted(out.items(), key=lambda x: -(x[1].get("is-referenced-by-count") or 0)):
    y = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
    print(f"{it.get('is-referenced-by-count',0):5d} | {y} | {d} | {html.unescape(' '.join(it['title']))[:105]} | {(it.get('container-title') or [''])[0][:28]}")
