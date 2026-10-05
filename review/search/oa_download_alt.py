"""Third pass for missing OA papers: Semantic Scholar openAccessPdf, then Europe PMC full-text XML (via ebi.ac.uk REST)."""
import json, subprocess, os, urllib.request, urllib.parse, time
oa = json.load(open("data/oa_status.json")); log = {r["n"]: r for r in json.load(open("data/download_log.json"))}
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0"
def js(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40))
        except Exception: time.sleep(3 * (i + 1))
for o in oa:
    r = log[o["n"]]
    if r["file"] or not o["is_oa"]: continue
    fn = f"fulltext/{o['n']:02d}.pdf"
    s2 = js(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(o['doi'])}?fields=openAccessPdf,externalIds")
    u = ((s2 or {}).get("openAccessPdf") or {}).get("url")
    if u:
        for cand in (u, "https://web.archive.org/web/2026id_/" + u):
            subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-o", fn, cand], capture_output=True)
            if os.path.exists(fn) and open(fn, "rb").read(4) == b"%PDF": r["file"] = fn; r["tried"].append((cand, "s2", True)); break
            if os.path.exists(fn): os.remove(fn)
    if not r["file"]:
        e = js("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode({"query": f'DOI:"{o["doi"]}"', "format": "json"}))
        res = ((e or {}).get("resultList") or {}).get("result") or []
        pmcid = next((x.get("pmcid") for x in res if x.get("pmcid")), None)
        if pmcid:
            xn = f"fulltext/{o['n']:02d}.xml"
            subprocess.run(["curl", "-sL", "-m", "60", "-o", xn, f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"], capture_output=True)
            if os.path.exists(xn) and b"<article" in open(xn, "rb").read(3000): r["file"] = xn; r["tried"].append((pmcid, "europepmc-xml", True))
            elif os.path.exists(xn): os.remove(xn)
    print(o["n"], o["oa_status"], r["file"] or "--"); time.sleep(1)
json.dump(list(log.values()), open("data/download_log.json", "w"), indent=1)
print("have", sum(1 for r in log.values() if r["file"]))
