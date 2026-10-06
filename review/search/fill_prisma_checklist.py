"""Fill the user-supplied PRISMA 2020 checklist template (main + abstract checklists) with this review's locations.
Keeps the template's formatting: only the text of the last cell in each item row is replaced."""
import sys, re, zipfile, shutil, os
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ns = {"w": W}
q = lambda t: "{%s}%s" % (W, t)

MAIN = {
 "1": "Title page: \"... A PRISMA 2020 Systematic Review of the Empirical Literature, 2015-2026\".",
 "2": "Abstract (structured; see PRISMA 2020 for Abstracts checklist below).",
 "3": "Section 1 (Introduction) and Section 2 (Literature Background and Related Reviews; Table 1).",
 "4": "Section 1, \"Objectives\": research questions RQ1-RQ4.",
 "5": "Section 3.4 and Table 3 (inclusion/exclusion criteria); grouping into themes F, D and S for synthesis (Section 3.4; Appendix B).",
 "6": "Section 3.2: Crossref REST API, last searched 5 October 2026; targeted Crossref title searches; Scopus/WoS not accessible (Section 6.1).",
 "7": "Section 3.3, Table 2 and Appendix C (all 70 query strings, filters and limits).",
 "8": "Section 3.5: two automated keyword stages (search/screen.py, screen_stage2.py), title/abstract assessment and full-text check of retrieved reports (21 of 42) by one reviewer (an AI agent); no independent duplicate screening.",
 "9": "Section 3.6: one reviewer (AI agent) extracted data from abstracts and Crossref metadata; no confirmation from study authors.",
 "10a": "Section 3.6 and Table 4: outcomes coded per study (outcome, method family, benchmark, accuracy measure, forward projection, sustainability dimension); all abstract-reported measures collected.",
 "10b": "Section 3.6 and Table 4 (setting, data period, open-access status); items not reported in the abstract coded \"n/r\" and never inferred (Appendix B).",
 "11": "Section 3.7: six-item reporting-transparency screen (abstract level), one reviewer; formal risk-of-bias tool (e.g. PROBAST) not applied - stated as a limitation (Section 6.1).",
 "12": "Not applicable: no effect measures pooled; accuracy measures are described (Section 3.8; Figure 7).",
 "13a": "Section 3.8: studies grouped by theme (F, D, S) per eligibility coding (Section 3.4).",
 "13b": "Section 3.6: missing items coded \"n/r\"; no data conversions.",
 "13c": "Section 3.8: descriptive figures (Figures 2-7), keyword network (Figure 5), study tables (Tables 5-7).",
 "13d": "Section 3.8: descriptive, keyword co-occurrence (controlled vocabulary, modularity clustering) and thematic synthesis; no meta-analysis (heterogeneous outcomes).",
 "13e": "Not performed (no meta-analysis); heterogeneity described narratively (Sections 4.3-4.4).",
 "13f": "Not performed; recall check of the automated screening reported (Section 6.1).",
 "14": "Not performed (stated in Section 3.8).",
 "15": "Not performed (stated in Section 3.8).",
 "16a": "Section 4.1 and Figure 1 (PRISMA flow diagram; supplementary completed template PRISMA_2020_flow_diagram_completed.docx).",
 "16b": "Appendix E lists all records excluded at title/abstract and full-text assessment with reasons.",
 "17": "Tables 5 and 6 (each included study cited with its characteristics); Figures 2-4.",
 "18": "Section 4.6 (reporting quality of forecasting studies, abstract level); formal risk of bias not assessed.",
 "19": "Tables 5-6 (abstract-level characteristics); effect estimates not extracted because full texts were not assessed (Section 6.1).",
 "20a": "Sections 4.3-4.4 and Table 7 (characteristics of contributing studies per theme).",
 "20b": "Sections 4.2-4.5: descriptive counts and cross-classification (Table 7); no statistical synthesis.",
 "20c": "Not applicable (no statistical synthesis).",
 "20d": "Not applicable (no sensitivity analysis).",
 "21": "Not assessed (Section 3.8).",
 "22": "Not assessed (Section 3.8).",
 "23a": "Sections 5.1-5.2 (principal findings; comparison with prior reviews).",
 "23b": "Sections 5.1 and 6.1 (abstract-level evidence, missing abstracts, heterogeneous reporting).",
 "23c": "Section 6.1 (single database, capped retrieval, automated screening recall, single AI reviewer, partial full-text assessment).",
 "23d": "Sections 5.3-5.5 (framework, practical implications, future research agenda; Table 8).",
 "24a": "Not registered (Section 3.1).",
 "24b": "No protocol was prepared in advance; criteria and code archived in the repository (Section 3.1).",
 "24c": "Not applicable (no registration or protocol).",
 "25": "Declarations: funding none declared [to be completed by the authors].",
 "26": "Declarations: none declared [to be completed by the authors].",
 "27": "Declarations and Appendix D: search logs, screening outputs, extraction data (data/included.json) and all code in the repository directory review/.",
}
ABSTRACT = {str(i): "Yes" for i in range(1, 13)}
ABSTRACT["7"] = "Yes"

def text(el): return "".join(el.itertext()).strip()

REF = {}
def set_cell(tc, value, key):
    ps = tc.findall("w:p", ns)
    keep = ps[0]
    for p in ps[1:]: tc.remove(p)
    runs = keep.findall("w:r", ns)
    rpr = None
    for r in runs:
        if r.find("w:rPr", ns) is not None and rpr is None: rpr = r.find("w:rPr", ns)
    import copy
    if key not in REF and rpr is not None:
        ref = copy.deepcopy(rpr)
        for tag in ("b", "bCs", "i", "iCs"):
            for e in ref.findall("w:" + tag, ns): ref.remove(e)
        REF[key] = ref
    rpr = copy.deepcopy(REF.get(key)) if REF.get(key) is not None else rpr
    for child in list(keep):
        if child.tag != q("pPr"): keep.remove(child)
    r = etree.SubElement(keep, q("r"))
    if rpr is not None: r.append(rpr)
    t = etree.SubElement(r, q("t")); t.text = value; t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

tmp = OUT + ".d"; shutil.rmtree(tmp, ignore_errors=True)
with zipfile.ZipFile(SRC) as z: z.extractall(tmp)
path = os.path.join(tmp, "word", "document.xml")
tree = etree.parse(path); root = tree.getroot()
tables = root.findall(".//w:tbl", ns)
done_main, done_abs = set(), set()
for ti, tbl in enumerate(tables):
    header = text(tbl.find("w:tr", ns))
    is_abstract = "Reported" in header
    last = None
    for tr in tbl.findall("w:tr", ns):
        tcs = tr.findall("w:tc", ns)
        if len(tcs) < 3: continue
        no = re.sub(r"\s+", "", text(tcs[1]))
        if not re.fullmatch(r"\d{1,2}[a-f]?", no): continue
        if is_abstract and no in ABSTRACT: set_cell(tcs[-1], ABSTRACT[no], 'abs'); done_abs.add(no)
        elif not is_abstract and no in MAIN: set_cell(tcs[-1], MAIN[no], 'main'); done_main.add(no)
tree.write(path, xml_declaration=True, encoding="UTF-8", standalone=True)
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for d, _, fs in os.walk(tmp):
        for f in fs:
            full = os.path.join(d, f); z.write(full, os.path.relpath(full, tmp))
shutil.rmtree(tmp)
print("main filled:", len(done_main), "missing:", sorted(set(MAIN) - done_main))
print("abstract filled:", len(done_abs), "missing:", sorted(set(ABSTRACT) - done_abs))
