"""Append BibTeX entries (from Crossref records) for included studies missing from paper/refs.bib, without touching existing entries."""
import json, re, sys
sys.argv = ["x"]; exec(open("search/build_bib.py").read().split("out = []")[0])  # tex(), entry()
inc = json.load(open("data/included.json")); cand = json.load(open("data/candidates_eligibility.json"))
bib = open("paper/refs.bib").read(); added = []
for i in inc:
    if "@article{%s," % i["key"] in bib: continue
    e = entry(i["key"], cand[i["doi"]])
    e = re.sub(r"[^\x00-ɏ‐-‟…\n]", "", e).replace("i̇", "i")
    e = "\n".join((re.sub(r"\b[^\W\d_]{3,}\b", lambda m: m.group(0).capitalize() if m.group(0).isupper() else m.group(0), l) if l.strip().startswith("author") else l) for l in e.split("\n"))
    bib += "\n" + e; added.append(i["key"])
open("paper/refs.bib", "w").write(bib); print("added", added)
