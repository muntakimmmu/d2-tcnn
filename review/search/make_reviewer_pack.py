"""M3: blinded screening pack for an independent human reviewer (all 98 title/abstract records, random order, no AI decisions),
plus the answer key kept separately for computing Cohen's kappa (search/kappa.py)."""
import json, re, csv, random, html
pool = json.load(open("data/screen_stage2.json")); cand = json.load(open("data/candidates_eligibility.json"))
inc = {i["doi"]: i for i in json.load(open("data/included_abstract_stage.json"))}
excl = {r["doi"].lower(): r["reason"] for r in csv.DictReader(open("data/excluded_eligibility.csv"))}
recs = {p["DOI"].lower(): p for p in pool}
for d in ["10.1016/j.igd.2024.100203", "10.46593/ijaera.2020.v06i08.001", "10.33948/esj-ksu-17-2-8", "10.1080/1331677x.2021.1985577",
          "10.1007/s11356-023-25545-0", "10.1016/j.ijhm.2026.104745"]: recs[d] = cand[d]
assert len(recs) == 98, len(recs)
clean = lambda s: html.unescape(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", s or ""))).strip()
rows = list(recs.items()); random.Random(2026).shuffle(rows)
with open("prisma/second_reviewer/screening_blind.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["record_id", "doi", "year", "journal", "title", "abstract", "DECISION (Include/Exclude)", "THEME if include (F/D/S)", "REASON CODE if exclude (R1-R6)", "notes"])
    for k, (d, r) in enumerate(rows, 1):
        w.writerow([f"R{k:03d}", d, (r.get("issued", {}).get("date-parts") or [[""]])[0][0], (r.get("container-title") or [""])[0],
                    clean(" ".join(r.get("title", []))), clean(r.get("abstract")) or "(no abstract in Crossref - decide on title)", "", "", "", ""])
key = []
for k, (d, _) in enumerate(rows, 1):
    i = inc.get(d)
    key.append({"record_id": f"R{k:03d}", "doi": d, "ai_decision": "Include" if (i or d == "10.34021/ve.2020.03.04(2)") else "Exclude",
                "ai_theme": (i or {}).get("theme", "S" if d == "10.34021/ve.2020.03.04(2)" else ""), "ai_reason": excl.get(d, "")})
json.dump(key, open("prisma/second_reviewer/ai_answer_key_DO_NOT_SHARE.json", "w"), indent=1)
print(sum(1 for x in key if x["ai_decision"] == "Include"), "AI includes of", len(key))
