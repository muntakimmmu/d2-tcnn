"""Second pass: for OA papers not yet downloaded, try Wayback Machine raw copies (id_) of each OA PDF URL,
and scholar.archive.org (fatcat) archived files. Keeps only real PDFs."""
import json, subprocess, os, re, urllib.parse, urllib.request, time
oa = json.load(open("data/oa_status.json")); log = {r["n"]: r for r in json.load(open("data/download_log.json"))}
UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0"
def ok(fn): return os.path.exists(fn) and open(fn, "rb").read(4) == b"%PDF"
def get(u, fn):
    subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-o", fn, u], capture_output=True)
    good = ok(fn)
    if not good and os.path.exists(fn): os.remove(fn)
    return good
for o in oa:
    r = log[o["n"]]; fn = f"fulltext/{o['n']:02d}.pdf"
    if r["file"] or not o["is_oa"]: continue
    cands = []
    for l in o["locations"]:
        for u in (l["pdf"], l["url"]):
            if u: cands.append("https://web.archive.org/web/2026id_/" + u)
    try:  # scholar.archive.org search API
        q = urllib.parse.quote(f'doi:"{o["doi"]}"')
        h = urllib.request.urlopen(urllib.request.Request(f"https://scholar.archive.org/search?q={q}", headers={"User-Agent": UA}), timeout=40).read().decode("utf8", "ignore")
        cands += sorted(set(re.findall(r'https://web\.archive\.org/web/\d+/[^"\s<>]+', h)))
        cands += sorted(set(re.findall(r'https://archive\.org/download/[^"\s<>]+\.pdf', h)))
    except Exception as e: pass
    for u in cands:
        u2 = re.sub(r"web\.archive\.org/web/(\d+)/", r"web.archive.org/web/\1id_/", u) if "id_/" not in u else u
        r["tried"].append((u2, "archive", False))
        if get(u2, fn): r["file"] = fn; r["tried"][-1] = (u2, "archive", True); break
        time.sleep(0.5)
    print(o["n"], o["oa_status"], "OK" if r["file"] else "--", len(cands))
json.dump(list(log.values()), open("data/download_log.json", "w"), indent=1)
print("downloaded", sum(1 for r in log.values() if r["file"]))
