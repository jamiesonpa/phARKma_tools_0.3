from anyio import current_effective_deadline
from get_details import get_details
import requests
import pandas as pd
from rapidfuzz import fuzz
from sec_api import FullTextSearchApi, XbrlApi
import datetime
import time
import spacy
from get_trials import get_trials_primary, get_trials_collaborator
from bs4 import BeautifulSoup
import config
from phARKma_utils import removeDigits
import re

alphavantage_api_key = config.alphavantage_api_key
polygon_api_key = config.polygon_api_key
edgar_api_key = config.edgar_api_key

def get_relationships(ticker):
    details = get_details(ticker, False)
    try:
        name = details["NAME"]
    except:
        pass
    try:
        first_part_of_name = name.split(" ")[0]
    except:
        pass
    try:
        cik = details["CIK ID"]
    except:
        pass
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    xbrlApi = XbrlApi(edgar_api_key)
    fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
    DEFAULT_HOST = "api.polygon.io"
    url = "https://" + DEFAULT_HOST
    current_year = int(datetime.datetime.now().year)
    session = requests.Session()
    session.params["apiKey"] = polygon_api_key
    annual_endpoint = "/vX/reference/financials?ticker="+ticker+"&filing_date.gte="+str(current_year)+"-01-01&timeframe=annual&include_sources=false&order=asc&sort=filing_date&apiKey=p1YTyzago_r14PExlGUNQY8X463myELr"
    last_year_annual_endpoint = "/vX/reference/financials?ticker="+ticker+"&filing_date.gte="+str(current_year-1)+"-01-01&timeframe=annual&include_sources=false&order=asc&sort=filing_date&apiKey=p1YTyzago_r14PExlGUNQY8X463myELr"
    query = {
    "query": ticker,
    "formTypes": ['10-K'],
    "startDate": str(current_year)+"-01-01",
    "endDate": str(current_year)+"-12-31",
    }
    unable_to_find_filings = False
    try:
        filings = fullTextSearchApi.get_filings(query)
    except:
        time.sleep(2)
        try:
            time.sleep(2)
            filings = fullTextSearchApi.get_filings(query)
        except:
            time.sleep(2)
            try:
                filings = fullTextSearchApi.get_filings(query)
            except:
                unable_to_find_filings = True

    if unable_to_find_filings == False:
        search_year = current_year
        if len(filings["filings"]) == 0:
            query = {
            "query": ticker,
            "formTypes": ['10-K'],
            "startDate": str(current_year-1)+"-01-01",
            "endDate": str(current_year-1)+"-12-31",
            }
            try:
                filings = fullTextSearchApi.get_filings(query)
            except:
                time.sleep(2)
                filings = fullTextSearchApi.get_filings(query)

            search_year = current_year-1
        tickermatches = []
        for filing in filings["filings"]:
            if str(filing["ticker"]).lower().strip() == ticker.lower().strip():
                tickermatches.append(filing["filingUrl"])

        filing_urls = []
        for match in tickermatches:
            if str(match).find("-") != -1:
                if str(match).split("-")[1].find("ex") == -1:
                    filing_urls.append(match)
                else:
                    if str(match).find("ex") == -1:
                        filing_urls.append(match)
        entlist = []

        strings = []
        for filingurl in filing_urls:
            for filing_url in filing_urls:
                req = requests.get(filing_url, headers=hdr)
                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                divtext = ""
                for div in soup.find_all("div"):
                    current_div_text = div.text
                    current_div_text = str(repr(current_div_text))
                    string_encode = current_div_text.encode("ascii", "ignore")
                    string_decode = string_encode.decode("unicode-escape")
                    string_decode = string_decode.replace("'","").replace('"',"")
                    if len(string_decode.split(" ")) > 10:
                        strings.append(string_decode)
            
        for string in strings:
            print(string)



get_relationships("EXAS")
