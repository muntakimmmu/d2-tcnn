"""Append Crossref-verified BibTeX entries for the comparison set of prior reviews and early-warning studies."""
import json, re, sys
sys.argv = ["x"]
src = open("search/build_bib.py").read(); exec(src.split("out = []")[0])  # reuse tex()/entry()
o = json.load(open("prior/closest_reviews.json"))
keymap = {"Hot2018":"Liu2018","Zhang2020km":"Zhang2020km","Hotel2022":"Huang2022","Resort2023":"Dowlut2023","Biblio2023":"Wu2023","BigData2024":"Wu2024",
 "HotelAI2024":"Henriques2024","CarbonSR2022":"Sun2022","CarbonBib2021":"Mishra2021","CarbonBib2023":"Liu2023carbon","IndicSDG2020":"Rasoolimanesh2020",
 "Climate2022":"Scott2022","Automation2023":"Majid2023","Gulf2014":"Henderson2014","Religion2020":"CollinsKreiner2020","ESGSaudi2025":"Alhejaili2025",
 "Saleh2022":"Saleh2021","CarryCapSLR2023":"Ajuhari2023","CCreview2022":"Long2022","CCscient2021":"Li2021cc","EW2020su":"Ye2020","EW2020jcr":"Sha2020"}
bib = open("paper/refs.bib").read(); added = []
for k, key in keymap.items():
    if "@article{%s," % key in bib: continue
    e = entry(key, o[k]); e = re.sub(r"[^\x00-ɏ‐-‟…\n]", "", e).replace("i̇", "i")
    bib += "\n" + e; added.append(key)
open("paper/refs.bib", "w").write(bib); json.dump(keymap, open("prior/keymap.json", "w"), indent=1); print(added)
