
import requests
import phARKma_utils
import sec_api
from sec_api import QueryApi
import config
import json
from datetime import datetime
import phARKma_utils



def get_details(ticker, verbose):
    print("Fetching company details for " + ticker)
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
    if str(details) == "{}":
        hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
        hdr["Authorization"] = config.sec_api_key
        response = requests.get("https://api.sec-api.io/mapping/ticker/" + ticker, headers = hdr)
        response_dict = response.json()[0]
        last_year = int(datetime.now().year) -1
        this_year = int(datetime.now().year)
        queryApi = QueryApi(api_key=config.sec_api_key)
        query = {
        "query": { "query_string": { 
            "query": "ticker:"+ticker+" AND filedAt:{"+str(last_year)+"-01-01 TO "+str(this_year)+"-12-31} AND formType:\"10-K\"" 
            } },
        "from": "0",
        "size": "10",
        "sort": [{ "filedAt": { "order": "desc" } }]
        }
        filings = queryApi.get_filings(query)
        if (len(filings["filings"])) == 1:
            if filings["filings"][0]["formType"] == "10-K":
                filing = filings["filings"][0]
                details["NAME"] = filing["companyName"]

    return details


def get_company_name(ticker):
    print(phARKma_utils.timestamp()+"Fetching company name for " + ticker)
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    hdr["Authorization"] = config.sec_api_key
    response = requests.get("https://api.sec-api.io/mapping/ticker/" + ticker, headers = hdr)
    response_dict = response.json()[0]
    last_year = int(datetime.now().year) -10
    this_year = int(datetime.now().year)
    queryApi = QueryApi(api_key=config.sec_api_key)
    query = {
    "query": { "query_string": { 
        "query": "ticker:"+ticker+" AND filedAt:{"+str(last_year)+"-01-01 TO "+str(this_year)+"-12-31}" 
        } },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
    }
    filings = queryApi.get_filings(query)
    filing = filings["filings"][0]
    if filing["ticker"] == ticker:
        name = filing["companyName"]
    return name

