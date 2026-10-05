"""Try every OA location (PDF first) with a browser user-agent; keep only real PDFs (%PDF magic). Logs outcome per paper."""
import json, subprocess, os, re, urllib.parse
oa = json.load(open("data/oa_status.json")); log = []
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
for o in oa:
    fn = f"fulltext/{o['n']:02d}.pdf"; res = {"n": o["n"], "doi": o["doi"], "oa_status": o["oa_status"], "file": None, "tried": []}
    if os.path.exists(fn) and open(fn, "rb").read(4) == b"%PDF": res["file"] = fn; log.append(res); continue
    urls = []
    for l in o["locations"]:
        for u in (l["pdf"], l["url"]):
            if u and u not in urls: urls.append(u)
    for u in urls:
        r = subprocess.run(["curl", "-sL", "-m", "45", "-A", UA, "-o", fn, "-w", "%{http_code}", u], capture_output=True, text=True)
        ok = os.path.exists(fn) and open(fn, "rb").read(4) == b"%PDF"
        res["tried"].append((u, r.stdout, ok))
        if ok: res["file"] = fn; break
        if os.path.exists(fn): os.remove(fn)
    log.append(res); print(o["n"], o["oa_status"], "OK" if res["file"] else "--", res["tried"][-1][:2] if res["tried"] else "")
json.dump(log, open("data/download_log.json", "w"), indent=1)
print("downloaded", sum(1 for r in log if r["file"]), "of", sum(1 for o in oa if o["is_oa"]), "OA")
