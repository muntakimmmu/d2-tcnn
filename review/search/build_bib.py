import json, re, html, urllib.request, urllib.parse, difflib, time
inc = json.load(open("data/included.json")); cand = json.load(open("data/candidates_eligibility.json"))
def tex(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s or "")); s = re.sub(r"\s+", " ", s).strip()
    for a,b in [("\\","\\textbackslash{}"),("&","\\&"),("%","\\%"),("_","\\_"),("#","\\#"),("$","\\$")]: s = s.replace(a,b)
    return s
def entry(key, r):
    au = " and ".join(f"{tex(a.get('family',''))}, {tex(a.get('given',''))}" if a.get("given") else tex(a.get("family","")) for a in r.get("author",[]) if a.get("family"))
    yr = (r.get("issued",{}).get("date-parts") or [[None]])[0][0]
    f = {"author":au,"title":"{"+tex(" ".join(r["title"]))+"}","journal":tex((r.get("container-title") or [""])[0]),"year":str(yr),"volume":tex(r.get("volume","")),"number":tex(r.get("issue","")),
         "pages":tex(r.get("page") or r.get("article-number") or "").replace("-","--") if (r.get("page") or r.get("article-number")) else "","doi":r["DOI"]}
    return "@article{%s,\n%s\n}\n" % (key, ",\n".join(f"  {k} = {{{v}}}" for k,v in f.items() if v))
out = []; ok = {}
for i in inc:
    r = cand[i["doi"]]; out.append(entry(i["key"], r))
BG = {  # key: query title (must fuzzy-match Crossref hit >= 0.80)
 "Page2021": "The PRISMA 2020 statement: an updated guideline for reporting systematic reviews",
 "Page2021ee": "PRISMA 2020 explanation and elaboration: updated guidance and exemplars for reporting systematic reviews",
 "Song2019": "Tourism demand forecasting: An overview of the research of the last decade review",
 "Peng2014": "A meta-analysis of international tourism demand forecasting and implications for practice",
 "Jiao2019": "Tourism forecasting: A review of methodological developments over the last decade",
 "Li2021": "Review of tourism forecasting research with internet data",
 "Law2019": "Tourism demand forecasting: A deep learning approach",
 "Sun2019": "Forecasting tourist arrivals with machine learning and internet search index",
 "Zhang2020": "Tourism demand forecasting: A decomposed deep learning approach",
 "Makridakis2020": "The M4 Competition: 100,000 time series and 61 forecasting methods",
 "Makridakis2022": "M5 accuracy competition: Results, findings, and conclusions",
 "Hyndman2006": "Another look at measures of forecast accuracy",
 "Diebold1995": "Comparing predictive accuracy",
 "Hansen2011": "The model confidence set",
 "Wolff2019": "PROBAST: A tool to assess the risk of bias and applicability of prediction model studies",
 "Gusenbauer2020": "Which academic search systems are suitable for systematic reviews or meta-analyses? Evaluating retrieval qualities of Google Scholar, PubMed, and 26 other resources",
 "Tricco2018": "PRISMA extension for scoping reviews (PRISMA-ScR): checklist and explanation",
 "Song2022": "Forecasting competition tourism demand recovery COVID-19",
 "Saudi2024sdg": "Exploring Tourism's Contribution to Saudi Arabia's Vision 2030: Aligning with UN SDG 8 for Sustainable Growth",
}
rep = []
for k,t in BG.items():
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": t, "rows": 5, "mailto": "muntakim.iot@gmail.com", "filter": "type:journal-article"})
    items = json.load(urllib.request.urlopen(u, timeout=40))["message"]["items"]; best = None
    for it in items:
        s = difflib.SequenceMatcher(None, html.unescape(" ".join(it.get("title",[""]))).lower(), t.lower()).ratio()
        if not best or s > best[0]: best = (s, it)
    s, it = best; rep.append((k, round(s,2), it["DOI"], " ".join(it["title"])[:90]))
    if s >= 0.80: out.append(entry(k, it)); ok[k] = it["DOI"]
    time.sleep(0.3)
open("paper/refs.bib","w").write("\n".join(out))
json.dump(ok, open("data/background_verified.json","w"), indent=1)
for r in rep: print(r)
