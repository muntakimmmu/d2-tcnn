"""M3: agreement between the AI screening decisions and an independent human reviewer.
Usage: python3 search/kappa.py prisma/second_reviewer/screening_blind_<initials>.csv
Reports Cohen's kappa (include/exclude) with 95% CI (bootstrap), confusion matrix, theme agreement among joint includes,
and lists every disagreement for consensus discussion (prisma/second_reviewer/disagreements.csv)."""
import csv, json, sys, random
human = {r["record_id"]: r for r in csv.DictReader(open(sys.argv[1]))}
key = {k["record_id"]: k for k in json.load(open("prisma/second_reviewer/ai_answer_key_DO_NOT_SHARE.json"))}
ids = [i for i in key if human.get(i, {}).get("DECISION (Include/Exclude)", "").strip()]
norm = lambda s: "Include" if s.strip().lower().startswith("i") else "Exclude"
a = [key[i]["ai_decision"] for i in ids]; h = [norm(human[i]["DECISION (Include/Exclude)"]) for i in ids]
def kappa(a, h):
    n = len(a); po = sum(x == y for x, y in zip(a, h)) / n
    pe = sum((a.count(c) / n) * (h.count(c) / n) for c in ("Include", "Exclude"))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po
k, po = kappa(a, h); rng = random.Random(1); boots = []
for _ in range(2000):
    s = [rng.randrange(len(ids)) for _ in ids]; boots.append(kappa([a[j] for j in s], [h[j] for j in s])[0])
boots.sort()
cm = {(x, y): sum(1 for p, q in zip(a, h) if p == x and q == y) for x in ("Include", "Exclude") for y in ("Include", "Exclude")}
both = [i for i, x, y in zip(ids, a, h) if x == y == "Include"]
th = sum(1 for i in both if human[i]["THEME if include (F/D/S)"].strip().upper()[:1] == key[i]["ai_theme"]) / max(1, len(both))
print(f"records rated: {len(ids)}/{len(key)}  observed agreement {po:.3f}  Cohen's kappa {k:.3f}  95% CI [{boots[49]:.3f}, {boots[1949]:.3f}]")
print("confusion (AI x human):", cm); print(f"theme agreement among joint includes: {th:.2f} (n={len(both)})")
with open("prisma/second_reviewer/disagreements.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["record_id", "doi", "title", "ai_decision", "ai_theme", "ai_reason", "human_decision", "human_theme", "human_reason", "consensus"])
    for i, x, y in zip(ids, a, h):
        if x != y: w.writerow([i, key[i]["doi"], human[i]["title"][:120], x, key[i]["ai_theme"], key[i]["ai_reason"], y, human[i]["THEME if include (F/D/S)"], human[i]["REASON CODE if exclude (R1-R6)"], ""])
json.dump({"n": len(ids), "observed_agreement": po, "kappa": k, "ci95": [boots[49], boots[1949]], "confusion": {f"{x}|{y}": v for (x, y), v in cm.items()}, "theme_agreement": th},
          open("prisma/second_reviewer/kappa_result.json", "w"), indent=1)
