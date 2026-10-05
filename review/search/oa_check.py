"""Open-access status for every paper in the download list via Unpaywall (all OA locations kept)."""
import csv, json, time, urllib.request, urllib.parse
rows = list(csv.DictReader(open("paper_download_list.csv")))
out = []
for i, r in enumerate(rows, 1):
    u = "https://api.unpaywall.org/v2/" + urllib.parse.quote(r["doi"]) + "?email=muntakim.iot@gmail.com"
    d = None
    for k in range(4):
        try: d = json.load(urllib.request.urlopen(u, timeout=40)); break
        except Exception as e: err = str(e); time.sleep(2 * (k + 1))
    locs = [] if not d else [{"url": l.get("url_for_pdf") or l.get("url"), "pdf": l.get("url_for_pdf"), "host": l.get("host_type"), "version": l.get("version"), "license": l.get("license")} for l in d.get("oa_locations") or []]
    out.append(dict(n=i, group=r["group"], authors=r["authors"], year=r["year"], title=r["title"], doi=r["doi"],
        is_oa=(d or {}).get("is_oa"), oa_status=(d or {}).get("oa_status", "lookup_failed"), locations=locs))
    time.sleep(0.2)
json.dump(out, open("data/oa_status.json", "w"), indent=1)
from collections import Counter
for g in ["A.", "B.", "C."]:
    print(g, Counter(o["oa_status"] for o in out if o["group"].startswith(g)))
