"""Fetch Crossref records for the closest prior reviews (comparison set) with retries."""
import json,urllib.request,re,html,time,os
D={"Peng2014":"10.1016/j.tourman.2014.04.005","Song2019":"10.1016/j.annals.2018.12.001","Jiao2019":"10.1177/1354816618812588","Hot2018":"10.1177/1354816618810564",
"Zhang2020km":"10.1016/j.tmp.2020.100715","Li2021":"10.1016/j.tourman.2020.104245","Hotel2022":"10.1108/tr-07-2022-0367","Resort2023":"10.1016/j.heliyon.2023.e18385",
"Biblio2023":"10.1108/tr-03-2023-0169","BigData2024":"10.1177/10963480231223151","HotelAI2024":"10.18089/tms.20240304","CarbonSR2022":"10.1016/j.annals.2022.103502",
"CarbonBib2021":"10.1108/tr-07-2021-0310","CarbonBib2023":"10.1080/1528008x.2023.2266861","IndicSDG2020":"10.1080/09669582.2020.1775621","Climate2022":"10.1016/j.annals.2022.103409",
"Automation2023":"10.1080/09669582.2023.2246681","Saudi2024sdg":"10.18280/ijsdp.200333","Gulf2014":"10.1080/02508281.2014.11081329","Religion2020":"10.1016/j.annals.2020.102892","ESGSaudi2025":"10.35631/jthem.1039004"}
P="prior/closest_reviews.json"; out=json.load(open(P)) if os.path.exists(P) else {}
for k,d in D.items():
    if k in out: continue
    for i in range(5):
        try:
            out[k]=json.load(urllib.request.urlopen("https://api.crossref.org/works/"+d+"?mailto=muntakim.iot@gmail.com",timeout=40))["message"]; break
        except Exception as e: time.sleep(2*(i+1))
    json.dump(out,open(P,"w")); time.sleep(0.5)
print(len(out),"of",len(D))
