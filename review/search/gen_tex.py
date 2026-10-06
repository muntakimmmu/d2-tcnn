import json, csv, collections as C, re
inc = json.load(open("data/included.json")); cnt = json.load(open("data/prisma_counts.json")); log = json.load(open("data/search_log.json"))
def tx(s):
    s = str(s).replace('Turkiye', 'T\\"urkiye')
    s = re.sub(r"[^\x00-\u024F\u2010-\u201F\u2026]", "", str(s))
    for a,b in [("&","\\&"),("%","\\%"),("_","\\_"),("#","\\#")]: s = s.replace(a,b)
    return s
# ---- PRISMA numbers (supplementary: 6 records, 2 already in database set but dropped by automated screen, 4 new)
N = dict(queries=cnt["queries"], retrieved=cnt["retrieved"], dups=cnt["duplicates_removed"], unique=cnt["unique"], other=6, other_new=4, other_reinst=2,
  screened=cnt["unique"]+4, auto_excl=cnt["auto_excl_not_tourism"]+cnt["auto_excl_no_region"]+cnt["auto_excl_no_forecast_sust"]+cnt["auto_excl_stage2"],
  assessed=cnt["pool"]+6, excl_elig=cnt["pool_excluded"]+1, included=cnt["total_included"],
  nF=cnt["theme"]["F"], nD=cnt["theme"]["D"], nS=cnt["theme"]["S"], nabs=cnt["has_abstract"], nnoabs=cnt["total_included"]-cnt["has_abstract"],
  e_notq=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Not a quant")][0]], e_growth=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Tourism-growth")][0]],
  e_geo=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Outside")][0]], e_lang=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Non-English")][0]],
  e_undet=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Eligibility")][0]]+1, e_oper=cnt["excl_reasons"][[k for k in cnt["excl_reasons"] if k.startswith("Operational")][0]])
assert N["screened"]-N["auto_excl"]+N["other_reinst"]==N["assessed"], (N)
N.update(ftsought=cnt["ft_sought"], ftretr=cnt["ft_retrieved"], ftnotret=cnt["ft_sought"]-cnt["ft_retrieved"], ftexcl=cnt["ft_excluded"],
  ftconf=cnt["ft_confirmed"], absonly=cnt["abstract_only"], dupsall=cnt["duplicates_removed"]+2, autonet=N["auto_excl"]-2, identified=cnt["retrieved"]+6)
assert N["assessed"]-N["excl_elig"]==N["ftsought"]
assert N["ftsought"]-N["ftexcl"]==N["included"] and N["ftconf"]+N["absonly"]==N["included"]
assert N["identified"]-N["dupsall"]-N["autonet"]==N["assessed"]
assert N["e_notq"]+N["e_growth"]+N["e_geo"]+N["e_lang"]+N["e_undet"]+N["e_oper"]==N["excl_elig"]
F=[i for i in inc if i["theme"]=="F"]; nonF=[i for i in inc if i["theme"]!="F"]
env=lambda i: any(w in i["sustainability"] for w in ("environ","economic","social","sustainable","SDG","climate"))
sust_flag=lambda i: not i["sustainability"].startswith("none") and not i["sustainability"].startswith("framing")
N.update(saudi_all=sum("Saudi" in i["country"] for i in inc), saudi_F=sum("Saudi" in i["country"] for i in F), turk=sum("Turkiye" in i["country"] for i in inc),
  F_sust=sum(sust_flag(i) for i in F), nonF_sust=sum(sust_flag(i) for i in nonF), nonF_nosust=sum(not sust_flag(i) for i in nonF), F_nosust=sum(not sust_flag(i) for i in F),
  Fabs=sum(i["benchmark"]!="n/r" for i in F), Fbench=sum(i["benchmark"]=="y" for i in F), Ffuture=sum(i["future"].startswith("y") for i in F),
  Fmetric=sum(i["metrics"]!="n/r" for i in F), Fm=sum(i["family"]=="M" for i in F), Fc=sum(i["family"]=="C" for i in F), Fh=sum(i["family"]=="H" for i in F), Fg=sum(i["family"]=="G" for i in F),
  nonF_fut=sum(i["future"].startswith("y") for i in nonF), nonF_econ=sum(i["family"]=="C" for i in nonF), nonFn=len(nonF),
  prerecent=sum(i["year"]<2020 for i in inc), yrecent=sum(i["year"]>=2020 for i in inc), yvrecent=sum(i["year"]>=2025 for i in inc),
  S_env=sum("environ" in i["sustainability"] for i in inc if i["theme"]=="S"))
open("paper/numbers.tex","w").write("\\newcommand{\\Npriorrev}{25}\n"+"".join("\\newcommand{\\N%s}{%s}\n" % (k.replace("_","").replace("1","one"), f"{v:,}".replace(",","{,}") if isinstance(v,int) else v) for k,v in N.items()))
json.dump(N, open("data/final_numbers.json","w"), indent=1)
# ---- tables
def au(i):
    a = i["authors"]; s = lambda x: x["family"] + " " + "".join(w[0] for w in re.split(r"[ .\-]+", x["given"]) if w)
    return (s(a[0]) + " et al." if len(a) > 2 else " \\& ".join(s(x) for x in a)) if a else "n/r"
def row_f(i): return f"\\citet{{{i['key']}}} & {tx(i['country'])} & {tx(i['outcome'])} & {tx(i['data'])} & {tx({'C':'Classical','M':'ML/DL','H':'Hybrid/ensemble','G':'Grey'}[i['family']])} & {tx({'y':'Yes','n':'No','n/r':'n/r'}[i['benchmark']])} & {tx(i['future'].replace('y ','Yes ').replace('n/r','n/r').replace('n','No') if i['future']=='n' else i['future'].replace('y','Yes'))} \\\\\n"
open("paper/tab_forecast.tex","w").write("\\begin{tabularx}{\\linewidth}{@{}p{3.2cm}p{3.0cm}p{4.6cm}p{4.2cm}p{2.6cm}p{1.7cm}p{2.6cm}@{}}\n\\toprule\nStudy & Setting & Outcome & Data & Method family & Benchmark & Forward projection\\\\\n\\midrule\n"+"".join(row_f(i) for i in sorted(F, key=lambda x:(x['country'],x['year'])))+"\\bottomrule\n\\end{tabularx}\n")
def row_n(i): return f"\\citet{{{i['key']}}} & {i['theme']} & {tx(i['country'])} & {tx(i['outcome'])} & {tx(i['data'])} & {tx(i['sustainability'])} \\\\\n"
open("paper/tab_nonforecast.tex","w").write("\\begin{tabularx}{\\linewidth}{@{}p{3.2cm}p{1.0cm}p{3.4cm}p{5.2cm}p{4.3cm}p{5.0cm}@{}}\n\\toprule\nStudy & Theme & Setting & Outcome & Data & Sustainability dimension\\\\\n\\midrule\n"+"".join(row_n(i) for i in sorted(nonF, key=lambda x:(x['theme'],x['country'])))+"\\bottomrule\n\\end{tabularx}\n")
# characteristics: year histogram + country counts for pgfplots
yc = C.Counter(i["year"] for i in inc); open("paper/dat_year.tex","w").write("\\newcommand{\\datayear}{"+"".join(f"({y},{yc.get(y,0)})" for y in range(2016,2027))+"}\n")
def region(c):
    if "Saudi" in c: return "Saudi Arabia"
    if "Turkiye" in c: return "T\\\"urkiye"
    if "GCC" in c or c.startswith("UAE") or c in ("Qatar",): return "Other GCC"
    return "Other Middle East/MENA"
rc = C.Counter(region(i["country"]) for i in inc); open("paper/dat_region.tex","w").write(json.dumps(rc))
# search log table
open("paper/tab_search.tex","w").write("\\begin{longtable}{@{}p{9.2cm}rr@{}}\n\\toprule\nQuery (\\texttt{query.bibliographic}) & Reported total & Retrieved\\\\\n\\midrule\\endhead\n"+"".join(f"{tx(q['query'])} & {q['total_results_reported']:,} & {q['retrieved']} \\\\\n" for q in log["queries"]).replace("{,}", ",")+"\\bottomrule\n\\end{longtable}\n")
# excluded
rows = list(csv.DictReader(open("data/excluded_eligibility.csv")))
print(N); print(rc)
# excluded table
ex = [(r["doi"], r["title"], r["year"], r["reason"]) for r in rows]
ex.append(("10.1016/j.ijhm.2026.104745", "Hybrid machine learning approaches for hotel occupancy forecasting: Evaluating gradient boosting and neural networks", "2026", "Eligibility not determinable from metadata (region or tourism link unconfirmed)"))
short = {"Full text":"Full text: growth nexus only","Not a quant":"Not quantitative forecast/demand/sustainability study","Tourism-grow":"Growth nexus only","Outside geo":"Outside Middle East","Non-English":"Non-English / proceedings","Eligibility n":"Region/tourism link unconfirmed","Operational/":"Operational/crowd/health prediction"}
def sh(r):
    for k,v in short.items():
        if r.startswith(k): return v
open("paper/tab_excluded.tex","w").write("\\begin{longtable}{@{}p{3.6cm}p{7.3cm}p{0.8cm}p{3.4cm}@{}}\n\\toprule\nDOI & Title (truncated) & Year & Reason\\\\\n\\midrule\\endhead\n"+"".join(f"{tx(d)} & {tx(t[:95])} & {y} & {tx(sh(r))} \\\\\n" for d,t,y,r in ex)+"\\bottomrule\n\\end{longtable}\n")
