"""Stage 3: eligibility decisions + abstract-level coding -> data/included.json, data/prisma_counts.json, data/excluded.csv"""
import json, re, csv
pool = json.load(open("data/screen_stage2.json"))           # 92 records after automated screening
cand = json.load(open("data/candidates_eligibility.json"))   # includes 6 supplementary records
log = json.load(open("data/search_log.json")); st = json.load(open("data/screen_stats.json"))
D = lambda i: pool[i]["DOI"].lower()
# --- exclusion reasons for the 92-pool (index -> code); anything not included/listed defaults to R2
R1 = "Outside geographic scope (not Middle East)"
R2 = "Not a quantitative forecasting, demand-modelling or tourism-sustainability study (perception/SEM, qualitative, conceptual, educational, technical non-tourism)"
R3 = "Tourism-growth nexus only (no demand forecasting/modelling of tourism outcome, no sustainability dimension)"
R4 = "Operational/crowd/health prediction, not tourism demand or sustainability"
R5 = "Non-English full record or conference proceedings"
R6 = "Eligibility not determinable from metadata (region or tourism link unconfirmed)"
reason = {}
for i in (15,16,36,43,50): reason[i] = R1
for i in (3,9,10,34,46,71,86,90,91): reason[i] = R3
for i in (55,56,61,64): reason[i] = R4
for i in (32,88): reason[i] = R5
for i in (42,47): reason[i] = R6
# --- coded inclusions (abstract-level extraction; n/r = not reported in the abstract/metadata available)
# fields: theme F=forecasting D=demand modelling S=sustainability nexus; fam: C classical stat/econometric, M ML/DL, G grey, H hybrid/ensemble
INC = [
# key, doi, theme, country, outcome, data, fam, bench, metric, future, sust
("Rashad2022", "10.3390/forecast4030036","F","UAE (Dubai)","tourism demand (travel search data)","monthly, 2019-01 to 2022-04","C","y","n/r","n","none"),
("Kurtulay2024","10.54493/jgttr.1408566","F","Turkiye","international visitor demand","monthly, 2002-01 to 2023-08","C","y","MAPE, RMSE","n","none"),
("Ouassou2022","10.3390/forecast4020024","F","Morocco","regional tourist arrivals","annual, 1999-2018","H","y","n/r","n","none"),
("Ahmadian2026","10.1108/jtf-10-2024-0219","F","Iran","inbound tourist arrivals","2020-2023 (small sample)","G","y","MAE, MAPE, RMSE","y (2024-26)","none"),
("Louati2024","10.3390/info15090516","F","Saudi Arabia","tourist spending; economic landscape","2015-2021","H","y","n/r","y (2022-30)","economic, sustainable development (stated)"),
("Alsulami2026","10.1038/s41598-025-32509-6","F","Saudi Arabia","tourism growth","n/r (abstract unavailable)","M","n/r","n/r","n/r","none (not assessable)"),
("AlShehhi2020","10.1016/j.jhtm.2019.11.003","F","GCC cities","hotel room prices","n/r (abstract unavailable)","M","n/r","n/r","n/r","none (not assessable)"),
("Zamzami2026","10.3390/su18115503","F","Saudi Arabia","tourism demand (tourist numbers)","2015-2024","M","y","MAE, RMSE, R2","n","framing (implications only)"),
("Tuncsiper2023","10.55677/ijssers/v03i3y2023-20","F","Turkiye","tourist numbers; tourism revenue","monthly, 2008-2022","M","n","R2","n","none"),
("Laaroussi2023","10.11591/ijece.v13i2.pp1989-1996","F","Morocco (Marrakech)","tourist arrivals","monthly","H","y","n/r","n","none"),
("AlShehhi2018","10.4236/tel.2018.89104","F","MENA cities","hotel prices","n/r (abstract unavailable)","M","n/r","n/r","n/r","none (not assessable)"),
("Cuhadar2020","10.30519/ahtr.765394","F","Turkiye","tourism revenues","n/r","H","y","MAPE","n","none"),
("Cankurt2016","10.3906/elk-1311-134","F","Turkiye","tourism demand","n/r (abstract unavailable)","M","n/r","n/r","n/r","none (not assessable)"),
("Bilek2025","10.3390/su17041396","F","Turkiye","tourism demand","monthly, 2008-2024","C","y","n/r","n","framing only (\"sustainable growth\")"),
("Kayral2023","10.3390/su152215924","F","Turkiye","tourist arrivals; tourism income","n/r","H","y","MAPE, sMAPE","y (scenarios)","none"),
("Alamoudi2020","10.46593/ijaera.2020.v06i08.001","F","Saudi Arabia (Makkah)","international Umrah visitors","annual, 33 years","C","y","MAPE","y (2020-30)","none (Vision 2030 target only)"),
("Shmoto2026","10.64704/alarbaeen.202604020435","D","Iraq (Karbala)","hotel occupancy seasonality","monthly, 5 years, 27 hotels","C","n","n/a","n","none"),
("Rafiei2018","10.1108/ijcthr-03-2017-0030","D","Middle East (panel)","international tourism demand","annual panel, 1995-2013","C","n","n/a","n","none"),
("Kisswani2020","10.3727/108354220x15758301241891","D","MENA (panel)","tourism receipts","n/r","C","n","n/a","n","none"),
("Ulucak2020","10.1177/1354816620901956","D","Turkiye","international arrivals (gravity)","1998-2017, 25 origins","C","n","n/a","n","framing (\"sustainable tourism\")"),
("Agazade2021","10.1177/13548166211055985","D","Turkiye","tourism revenues","monthly, 2008-01 to 2019-09","C","n","n/a","n","none"),
("Hamida2025","10.1177/14673584251350551","D","Tunisia","tourist arrivals vs geopolitical risk","monthly, 1993-2023","C","n","n/a","n","none"),
("Wada2021","10.24818/rej/2021/81/01","D","MENA (panel)","international arrivals","2012-2018","C","n","n/a","n","none"),
("Chouari2025","10.64753/jcasc.v10i3.2758","D","Saudi Arabia","regional/seasonal tourist flows vs climate","2005-2024","C","n","n/a","y (climate scenarios)","environmental (climate)"),
("Abuhulaibah2026","10.3390/su18157602","D","Saudi Arabia","tourism development","annual, 1995-2024","C","n","n/a","n","environmental (climate vulnerability)"),
("Alfehaid2026","10.1002/sd.70756","D","Saudi Arabia","regional tourism spending","13 regions, 2024","C","n","n/a","n","environmental (green infrastructure), SDG"),
("Mabrouk2026","10.3390/su18126295","D","Saudi Arabia","religious/non-religious tourism demand","quarterly, 2015Q1-2024Q4","C","n","n/a","n","none"),
("Triki2019","10.30892/gtg.27417-436","S","Saudi Arabia","sustainable development (religious tourism)","n/r (abstract unavailable)","C","n/r","n/a","n","economic/sustainable development (title)"),
("BinSurayhid2026","10.3390/su18126245","S","Middle East (10 countries)","transport CO2 emissions","annual, 2000-2020","C","n","n/a","n","environmental"),
("Voumik2023","10.3390/su15064919","S","Middle East (10 countries)","CO2 emissions (EKC)","annual, 1997-2019","C","n","n/a","n","environmental"),
("Bahar2023","10.24288/jttr.1252689","S","Turkiye","CO2 emissions","annual, 1984-2021","C","n","n/a","n","environmental"),
("Alnafisah2025","10.3390/su17104272","S","GCC","income equality","quarterly, 2014Q1-2023Q4","C","n","n/a","n","social"),
("Zmami2024","10.18488/31.v11i2.3808","S","GCC","three sustainable-development pillars","n/r","C","n","n/a","n","economic, social, environmental"),
("Farooq2023a","10.1177/13548166231174812","S","GCC (6 countries)","CO2 emissions","annual, 2000-2019","C","n","n/a","n","environmental"),
("Bildirici2025","10.3390/su17146351","S","Saudi Arabia, Turkiye (+Italy)","pollution, air quality, life expectancy","annual, 1975-2019","C","n","n/a","n","environmental, social"),
("Majumdar2022","10.3390/su14137834","S","UAE","CO2 emissions (EKC)","annual, 1984-2019","C","n","n/a","n","environmental"),
("Harazneh2026","10.21511/ppm.24(2).2026.09","S","Jordan","post-COVID recovery index","annual, 2010-2024","C","n","n/a","n","environmental (EPI), innovation"),
("Nair2016","10.1504/ijssoc.2016.079082","S","Qatar","sustainable tourism causality","n/r (abstract unavailable)","C","n/r","n/a","n","sustainable tourism (title)"),
("Raihan2025","10.1016/j.igd.2024.100203","S","Saudi Arabia","carbon neutrality (Hajj)","n/r (abstract unavailable)","C","n/r","n/a","n","environmental (title)"),
("Naseem2025","10.33948/esj-ksu-17-2-8","S","Saudi Arabia","CO2 emissions (pilgrimage)","annual, 1996-2022","C","n","n/a","n","environmental"),
("Ozturk2021","10.1080/1331677x.2021.1985577","S","Saudi Arabia","CO2 emissions (pilgrimage)","n/r (abstract unavailable)","C","n/r","n/a","n","environmental (title)"),
("Farooq2023b","10.1007/s11356-023-25545-0","S","GCC","environmental quality","n/r (abstract unavailable)","C","n/r","n/a","n","environmental (title)"),
]
def meta(doi):
    r = cand[doi]; au = r.get("author", [])
    return dict(title=re.sub(r"\s+"," ",re.sub("<[^>]+>","",(" ".join(r["title"])))).replace("&lt;b&gt;","").replace("&lt;/b&gt;","").replace("&amp;amp;","&").strip(),
      authors=[dict(family=x.get('family','').strip(), given=x.get('given','').strip()) for x in au if x.get('family') or x.get('given')], 
      year=(r.get("issued",{}).get("date-parts") or [[None]])[0][0], journal=(r.get("container-title") or [""])[0], volume=r.get("volume"), pages=r.get("page") or r.get("article-number"), has_abstract=bool(r.get("abstract")))
inc = []
for k,doi,theme,ctry,out,data,fam,bench,metric,fut,sust in INC:
    m = meta(doi); m.update(key=k,doi=doi,theme=theme,country=ctry,outcome=out,data=data,family=fam,benchmark=bench,metrics=metric,future=fut,sustainability=sust,
        from_pool = doi in {p["DOI"].lower() for p in pool}); inc.append(m)
assert all(i["doi"] in cand for i in inc)
json.dump(inc, open("data/included.json","w"), indent=1)
inc_dois = {i["doi"] for i in inc}
rows = []
for i,p in enumerate(pool):
    if p["DOI"].lower() in inc_dois: continue
    rows.append((p["DOI"], " ".join(p["title"])[:140].replace("\n"," "), p.get("_year"), reason.get(i, R2)))
with open("data/excluded_eligibility.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["doi","title","year","reason"]); w.writerows(rows)
from collections import Counter
rc = Counter(r[3] for r in rows)
n_ret = log["n_retrieved_total"]; n_uniq = log["n_unique_doi"]
supp_in = [i for i in inc if not i["from_pool"]]
cnt = dict(queries=len(log["queries"]), retrieved=n_ret, duplicates_removed=n_ret-n_uniq, unique=n_uniq,
  other_methods_records=len(cand)-len({p["DOI"].lower() for p in pool if p["DOI"].lower() in cand}),
  auto_excl_not_tourism=st["excl_not_tourism"], auto_excl_no_region=st["excl_no_region_signal"], auto_excl_no_forecast_sust=st["excl_no_forecast_or_sust"],
  auto_pass1=st["passed_rule_screen"], auto_excl_stage2=st["passed_rule_screen"]-len(pool), pool=len(pool),
  pool_included=len(inc)-len(supp_in), pool_excluded=len(rows), supp_assessed=len(cand)-sum(1 for d in cand if d in {p["DOI"].lower() for p in pool}),
  supp_included=len(supp_in), total_included=len(inc), excl_reasons=dict(rc),
  theme=dict(Counter(i["theme"] for i in inc)), has_abstract=sum(i["has_abstract"] for i in inc))
json.dump(cnt, open("data/prisma_counts.json","w"), indent=1); print(json.dumps(cnt, indent=1))
