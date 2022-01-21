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
    try:
        filings = fullTextSearchApi.get_filings(query)
    except:
        time.sleep(2)
        filings = fullTextSearchApi.get_filings(query)
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
    filing_urls = []
    for filing in filings["filings"]:
        if filing["cik"] == str(cik):
            if filing["ticker"] == ticker:
                if filing["filingUrl"].find("ex") == -1:
                    filing_urls.append(filing["filingUrl"])
    
    filing_url = filing_urls[0]

    req = requests.get(filing_url, headers=hdr)
    html = req.text
    soup = BeautifulSoup(html,'html.parser')
    divtext = ""
    for div in soup.find_all("div"):
        current_div_text = div.text
        current_div_text = current_div_text.strip()
        divtext = divtext + "\n" + current_div_text

    
    sentences = divtext.split(".")
    sentences_split = []
    for sentence in sentences:
        sentence_frags = sentence.split("\n")
        for sentence_frag in sentence_frags:
            sentences_split.append(sentence_frag)
    sentences_to_parse = []
    for sentence in sentences_split:
        if sentence.lower().find("collaboration") != -1:
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
    with open("countries.txt") as readfile:
        countries = readfile.read().split("\n")
    # model = load_models()
    nlp = spacy.load("en_core_web_sm")
    

    entities = []
    for sent in sentences_to_parse:
        doc = nlp(sent)
        # docs = process_text(doc, ["ORG"])
        for X in doc.ents:
            if X.label_ == "ORG":
                found = False
                for entity in entities:
                    if entity == X.text:
                        found = True
                if found == False:
                    if X.text != "Inc":
                        if X.text.lower().find("phase"):
                            if X.text.lower().find("company"):
                                if X.text != "Licensing Arrangements":
                                    if X.text.find("the") == -1:
                                        if X.text.isupper() == False:
                                            if X.text.find("License") == -1:
                                                if X.text.lower().find("tumor") == -1:
                                                    if X.text.lower().find("registrant") == -1:
                                                        if X.text.lower().find(first_part_of_name.lower()) == -1:
                                                            if X.text.lower().find("collab") == -1:
                                                                if X.text.lower().find("amend") == -1:
                                                                    if X.text.lower().find("statement") == -1:
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
                                                                                            if X.text.lower().find("admin") == -1:
                                                                                                if X.text.lower().find("develop") == -1:
                                                                                                    if X.text.lower().find("expense") == -1:
                                                                                                        if X.text.lower().find("conversion") == -1:
                                                                                                            if X.text.lower().find("agree") == -1:
                                                                                                                if X.text.lower().find("revenu") == -1:
                                                                                                                    if X.text.lower().find("interest") == -1:
                                                                                                                        if X.text.lower().find("income") == -1:
                                                                                                                            if X.text.lower().find("program") == -1:
                                                                                                                                if X.text.lower().find("candidate") == -1:
                                                                                                                                    if X.text.lower().find("indication") == -1:
                                                                                                                                        if X.text.lower().find("stock") == -1:
                                                                                                                                            if X.text.lower().find("operations") == -1:
                                                                                                                                                if X.text.lower().find(" to ") == -1:
                                                                                                                                                    entities.append(removeDigits(X.text))

    trial_entities = get_trials_collaborator(ticker, True)
    trial_entities_2 = get_trials_primary(ticker, True)
    for te in trial_entities:
        entities.append(te)
    
    for te2 in trial_entities_2:
        entities.append(te2)
    
    clean_ents = []
    for ent in entities:
        if ent.find("not found") == -1:
            if ent != "":
                clean_ents.append(ent)
    return clean_ents        