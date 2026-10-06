"""M5/M8 sensitivity analyses of the forecasting-sustainability split.
S0 = main analysis; S1 = add the growth-nexus studies excluded under criterion R3 (and at full text);
S2 = exclude Turkiye; S3 = restrict to studies confirmed at full text."""
import json, re, csv
inc = json.load(open("data/included.json")); pool = json.load(open("data/screen_stage2.json"))
abst = json.load(open("data/included_abstract_stage.json"))
R3_IDX = (3, 10, 34, 46, 71, 86, 90, 91)  # index 9 re-included in main analysis
def ab(r): return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", r.get("abstract") or ""))
growth = []
for i in R3_IDX:
    r = pool[i]; a = (" ".join(r["title"]) + " " + ab(r))
    growth.append({"key": r["DOI"], "theme": "D", "country": "n/a", "future": "y" if re.search(r"forecast|projection|scenario", a, re.I) else "n",
                   "sustainability": "none", "fulltext_confirmed": False, "title": " ".join(r["title"])[:90]})
growth += [dict(i, theme="D", sustainability="none") for i in abst if i["key"] == "Triki2019"]
sust = lambda i: not i["sustainability"].startswith("none") and not i["sustainability"].startswith("framing")
def table(studies):
    F = [i for i in studies if i["theme"] == "F"]; O = [i for i in studies if i["theme"] != "F"]
    return dict(n=len(studies), F=len(F), F_sust=sum(map(sust, F)), nonF=len(O), nonF_sust=sum(map(sust, O)),
                nonF_forward=sum(1 for i in O if i["future"].startswith("y")))
res = {"S0_main": table(inc), "S1_plus_growth_nexus": table(inc + growth),
       "S2_without_Turkiye": table([i for i in inc if "Turkiye" not in i["country"]]),
       "S3_fulltext_confirmed_only": table([i for i in inc if i.get("fulltext_confirmed")])}
res["growth_nexus_with_forecast_terms"] = [g["title"] for g in growth if g["future"] == "y"]
json.dump(res, open("data/sensitivity.json", "w"), indent=1); print(json.dumps(res, indent=1))
