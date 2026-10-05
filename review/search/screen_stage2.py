"""Stage 2 automated screen (title+abstract term filter), applied to survivors of screen.py. Reproduces data/screen_stage2.json."""
import json, re
o = json.load(open("data/screen_pass.json"))
F = re.compile(r"forecast|predict|time[- ]series|arima|lstm|neural network|machine learning|deep learning|ardl|cointegrat|causality|econometric|panel data|projection|random forest|regression|quantile|gmm|fmols|dols|kuznets|simulation", re.I)
keep = [r for r in o if F.search(" ".join(r["title"]) + " " + re.sub("<[^>]+>", " ", r.get("abstract") or ""))]
json.dump(keep, open("data/screen_stage2.json", "w")); print(len(keep))
