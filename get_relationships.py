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
        if len(filing_urls) > 0:

            for filing_url in filing_urls:
                req = requests.get(filing_url, headers=hdr)
                html = req.text
                soup = BeautifulSoup(html,'html.parser')
                divtext = ""
                for div in soup.find_all("div"):
                    current_div_text = div.text
                    current_div_text = str(repr(current_div_text))
                    for match in re.match("\u...b"):
                        
                    print(repr(current_div_text))
                    divtext = divtext + "\n" + current_div_text
                sentences = []

                sentences_split = []
                for sentence in sentences:
                    sentence_frags = sentence.split("\n")
                    for sentence_frag in sentence_frags:
                        sentence_frag = sentence_frag.replace("\n ", " ").rstrip("\r\n").replace("  "," ").replace("  "," ").replace("  "," ").replace("\r","").replace("\t","")
                        sentences_split.append(sentence_frag)

                sentences_to_parse = []
                for sentence in sentences_split:
                    goodsentence = False
                    sentence_checkwords = ["partnership", "collab","agreement","guarantor","underwriter", "partner","strategic", "lawsuit"]
                    for word in sentence_checkwords:
                        if sentence.lower().find(word) != -1:
                            goodsentence = True
                    if goodsentence == True:
                        words = sentence.split(" ")
                        capitalized_words = 0
                        for word in words[1:]:
                            if word.find("Company") == -1:
                                if len(word) > 1:
                                    if str(word[0]).isupper() == True:
                                        if str(word[1:]).isupper() == False:
                                            capitalized_words+=1
                        if capitalized_words > 1:
                            sentences_to_parse.append(sentence)

                #define countries
                with open("countries.txt") as readfile:
                    countries = readfile.read().split("\n")
                #define spacy model
                nlp = spacy.load("en_core_web_sm")
                
                #is uppper
                #is country
                # digits = re.findall(r'\d+', X.text)
                # keywords_exclude_upper = ["Inc", "Licensing Arrangements", "License"]
                keywords_exclude_lower = ["phase","company","the","tumor","registrant","collab",first_part_of_name.lower(), "collab","amend","statement", ";",":","admin", "develop","expense","conversion","agree","revenu","interest","income","program","candidate","indication","stock"," to ", "code","'s","s'","guarantor","convertible","the","month","ended","letter","education","fellows","cost","customer","balance","consolidated"," and ","balance","complaint","improvement","contract","milestones"]
                entities = []
                for sent in sentences_to_parse:
                    doc = nlp(sent)
                    for X in doc.ents:
                        if X.label_ == "ORG":
                            found = False
                            for entity in entities:
                                if entity == X.text:
                                    found = True
                            if found == False:
                                bad = False
                                for kel in keywords_exclude_lower:
                                    if X.text.lower().find(kel) != -1:
                                        bad = True 
                                if not bad:
                                    print("found not bad sentence")
                                    if X.text != "Inc":
                                        if X.text != "Licensing Arrangements":
                                            if X.text.find("the") == -1:
                                                if X.text.isupper() == False:
                                                    if X.text.find("License") == -1:
                                                        iscountry = False
                                                        for country in countries:
                                                            if X.text.find(country) != -1:
                                                                iscountry = True
                                                        if iscountry == False:
                                                            if X.text.find("10-K") == -1:
                                                                if X.text.find(";") == -1:
                                                                    if X.text.find(":") == -1:
                                                                        digits = re.findall(r'\d+', X.text)
                                                                        if len(digits) <= 1:
                                                                            if X.text.find("'s") == -1:
                                                                                if len(X.text.split(" ")) < 4:
                                                                                    entities.append(removeDigits(X.text))
                for ent in entities:                                                                                                                                                                                                
                    if ent.find("not found") == -1:
                        if ent != "":
                            entlist.append(ent)
            return entlist
        else:
            return entlist
    else:
        return []