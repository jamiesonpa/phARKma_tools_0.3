
import requests

def get_details(ticker):
    polygon_api_key = "p1YTyzago_r14PExlGUNQY8X463myELr"
    url ="https://api.polygon.io/v1/meta/symbols/"+ticker+"/company?apiKey=" + polygon_api_key
    response = requests.get(url)
    details_cats = [("NAME", "name"), ("SYMBOL", "symbol"), ("LOGO","logo"), ("IPO DATE", "listdate"), ("INDUSTRY", "industry"), ("DESCRIPTION","description"),("COMPETITORS","similar"),("TAGS","tags"),("WEBSITE","url"),("EMPLOYEES","employees"),("HQ","hq_country"),("CIK ID","cik"),("BLOOMBERG ID","bloomberg"),("SIC ID","sic")]
    details = {}
    for cat in details_cats:
        try:
            details[cat[0]] = str(response.json()[cat[1]])
        except:
            pass
    return details