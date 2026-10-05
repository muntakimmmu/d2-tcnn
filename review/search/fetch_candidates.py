"""Assemble eligibility candidates: pool records judged includable at title/abstract + supplementary records
found by targeted Crossref title searches (seeded by web-search leads). Full Crossref records are stored for abstract-level coding."""
import json, urllib.request, urllib.parse
pool = json.load(open("data/screen_stage2.json"))
inc_idx = [4,6,8,12,17,18,19,26,30,33,35,79,81,82,84,44,29,39,80,85,89,67,13,24,27,23,5,37,38,41,45,48,49,69,70,78,51]
extra = ["10.1016/j.igd.2024.100203","10.46593/ijaera.2020.v06i08.001","10.33948/esj-ksu-17-2-8","10.1080/1331677x.2021.1985577","10.1007/s11356-023-25545-0","10.1016/j.ijhm.2026.104745"]
recs = {pool[i]["DOI"].lower(): pool[i] for i in inc_idx}
for d in extra:
    u = "https://api.crossref.org/works/" + urllib.parse.quote(d) + "?mailto=muntakim.iot@gmail.com"
    recs[d] = json.load(urllib.request.urlopen(u, timeout=40))["message"]
json.dump(recs, open("data/candidates_eligibility.json", "w")); print(len(recs))
