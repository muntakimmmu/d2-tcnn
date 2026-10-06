"""Fill the user-supplied PRISMA 2020 flow diagram template (new SRs, databases and registers) with this review's counts.
The template stores every text box twice (DrawingML + VML fallback), so each label is replaced wherever it occurs.
Numbers come from data/final_numbers.json (written by search/gen_tex.py)."""
import sys, json, zipfile, shutil, os, subprocess
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
N = json.load(open("data/final_numbers.json"))
f = lambda k: f"{N[k]:,}"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"; ns = {"w": W}

FIXED = {
 "Databases (n = )": f"Databases: Crossref (n = {f('retrieved')})",
 "Registers (n = )": f"Registers (n = 0); targeted title searches (n = {N['other']})",
 "Duplicate records removed  (n = )": f"Duplicate records removed (n = {f('dupsall')})",
 "Records marked as ineligible by automation tools (n = )": f"Marked ineligible by automation (n = {f('autonet')})†",
 "Records removed for other reasons (n = )": "Other reasons (n = 0)",
 "Reason 1 (n = )": f"Tourism–growth nexus only (n = {N['ftexcl']})",
 "Reason 2 (n = )": "", "Reason 3 (n = )": "", "etc.": "",
 "*Consider, if feasible to do so, reporting the number of records identified from each database or register searched (rather than the total number across all databases/registers).":
   f"*Crossref was the only database searched ({N['queries']} queries, top 100 records each); no registers were searched. Duplicates include the {N['other_reinst']} targeted-search records already retrieved from Crossref.",
 "**If automation tools were used, indicate how many records were excluded by a human and how many were excluded by automation tools.":
   f"**Excluded by one reviewer (an AI agent) on title and abstract: not a quantitative forecasting, demand or sustainability study ({N['e_notq']}); "
   f"tourism–growth nexus only ({N['e_growth']}); outside the Middle East ({N['e_geo']}); operational or health prediction ({N['e_oper']}); "
   f"region or tourism link unconfirmed ({N['e_undet']}); non-English or proceedings ({N['e_lang']}). "
   f"†Keyword filters (automation) flagged {f('auto_excl')} records; {N['other_reinst']} were retained because targeted searches also identified them. "
   f"††{N['ftnotret']} reports not retrieved: 11 closed access and 10 open access on hosts blocked from the review environment. "
   f"‡{N['ftconf']} studies confirmed at full text; {N['absonly']} included on title-and-abstract evidence pending full-text retrieval.",
}
# "(n = )" values depend on the label that precedes them
AFTER = {"Records screened": f"(n = {N['assessed']})", "Records excluded**": f"(n = {N['exclelig'] if 'exclelig' in N else N['excl_elig']})",
         "Reports sought for retrieval": f"(n = {N['ftsought']})", "Reports not retrieved": f"(n = {N['ftnotret']})††",
         "Reports assessed for eligibility": f"(n = {N['ftretr']})", "Studies included in review": f"(n = {N['included']})‡",
         "Reports of included studies": f"(n = {N['included']})"}

tmp = OUT + ".d"; shutil.rmtree(tmp, ignore_errors=True)
with zipfile.ZipFile(SRC) as z: z.extractall(tmp)
for root_, _, fs in os.walk(tmp):                      # untrusted archive: drop symlinks
    for x in fs:
        if os.path.islink(os.path.join(root_, x)): os.remove(os.path.join(root_, x))
skill = sys.argv[3] if len(sys.argv) > 3 else None
if skill: subprocess.run(["python3", os.path.join(skill, "scripts/merge_runs.py"), tmp], check=True, capture_output=True)
path = os.path.join(tmp, "word", "document.xml"); tree = etree.parse(path)
last, changed = None, 0
for t in tree.iter("{%s}t" % W):
    s = t.text or ""
    if s in FIXED: t.text = FIXED[s]; changed += 1
    elif s.strip() == "(n = )" and last in AFTER: t.text = AFTER[last]; changed += 1
    if s.strip() in AFTER: last = s.strip()
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk(tmp):
        for x in fs:
            full = os.path.join(d, x); z.write(full, os.path.relpath(full, tmp))
shutil.rmtree(tmp)
left = subprocess.run(["unzip", "-p", OUT, "word/document.xml"], capture_output=True, text=True).stdout.count("(n = )")
print("replaced", changed, "| unfilled '(n = )' left:", left)
