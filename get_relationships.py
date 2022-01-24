from platform import release
from anyio import current_effective_deadline
from bleach import clean
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



def clean_string(string):
    print(string)

def get_relationships(ticker):
    details = get_details(ticker, False)
    try:
        name = details["NAME"]
        print("name found: " + name)
    except:
        print("couldn't find name")
    try:
        first_part_of_name = name.split(" ")[0]
    except:
        pass
    try:
        cik = details["CIK ID"]
    except:
        print("couldn't fetch CIK ID")
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
    "query": name,
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
                print("couldnt find filings for " + ticker)

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
                try:
                    filings = fullTextSearchApi.get_filings(query)
                except:
                    print("couldnt find filings for " + ticker)



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


        divtext_list =[]
        for filing_url in filing_urls:
            # req = requests.get(filing_url, headers=hdr)
            response = requests.get(filing_url, headers=hdr)
            soup = BeautifulSoup(response.content, "html.parser")
            divs = soup.find_all("div")
            for div in divs:
                divtext = div.get_text(" ")
                divtext = divtext.replace("/s/", "")
                divtext = divtext.replace("s/", "")
                divtext_list.append(divtext)
    
        chopped = []
        for divtext in divtext_list:
            split_div = divtext.split(". ")
            for sentence in split_div:
                if sentence.find("\n") != -1:
                    newline_split = sentence.split("\n")
                    for frag in newline_split:
                        chopped.append(frag)
                else:
                    chopped.append(sentence)

        long_strings = []
        for fragment in chopped:
            if len(fragment) > 25:
                if fragment.isupper() == False:
                    if fragment.find("Table of Content") == -1:
                        if fragment.find("$") < 2:
                            if fragment.find("__") == -1:
                                if fragment.find("(In ") == -1:
                                    if fragment.find(" - ") == -1:
                                        if fragment.lower().find("year ended") == -1:
                                            if fragment.find("%") < 3:
                                                if fragment[-1] == " ":
                                                    fragment = fragment.strip()
                                                if fragment[-1] != ".":
                                                    if fragment[-1] != ":":
                                                        fragment = fragment + "."
                                                long_strings.append(fragment.strip().replace("  ", " ").replace("  "," ").replace("  "," ").replace("  "," ").replace('("',"").replace('")',""))

        
        #define countries
        with open("countries.txt") as readfile:
            countries = readfile.read().split("\n")
        #define states
        with open("states.txt") as readfile:
            states = readfile.read().split("\n")

        #define months
        with open("months.txt") as readfile:
            months = readfile.read().split("\n")
        
        #define spacy model
        model_loaded = False
        try:
            nlp = spacy.load("en_core_web_lg")
            model_loaded = True
            print("model loaded")
        except:
            print("Error: you may not have the correct spacy python model installed on your system, try running 'python -m spacy download en_core_web_lg'")

        #if everything is good, proceed
        if model_loaded == True:
            print("proceeding with text processing")

            #append all of the sentences together into one string.
            doc = ""
            for sentence in long_strings:
                doc = doc + sentence + " "

            #use that string as the input for the model.
            try:
                mod = nlp(doc)
                print("training on unexpanded")
            except:
                mod = nlp(doc[0:1000000])

            print("extracing organization named entities")
            #extract all the named organization entities from the sentences.
            ents = []
            for X in mod.ents:
                if X.label_ == "ORG":
                    ents.append(X.text)
                    
            #deduplicate
            deduplicated_ents = list(set(ents))

            #remove all states
            decountrified_ents = []
            for ddent in deduplicated_ents:
                country_found = False
                for country in countries:
                    if ddent.lower().find(country.lower()) != -1:
                        country_found = True
                
                if country_found == False:
                    decountrified_ents.append(ddent)
            



            #remove all states
            destatified_ents = []
            for dcount in decountrified_ents:
                state_found = False
                for state in states:
                    if dcount.lower().find(state.lower()) != -1:
                        state_found = True
                
                if state_found == False:
                    destatified_ents.append(dcount)


            #remove all months
            demonthified_ents = []
            for dstat in destatified_ents:
                month_found = False
                for month in months:
                    if dstat.lower().find(month.lower()) != -1:
                        month_found = True
                
                if month_found == False:
                    demonthified_ents.append(dstat)

            #remove all entities starting with "the"
            detheified_ents = []
            for ent in demonthified_ents:
                if ent.split(" ")[0].lower() != "the":
                    detheified_ents.append(ent)
                else:
                    detheified_ents.append(ent.replace("the ", "").replace("The ", ""))


            #remove all entities ending in "of"
            deofified_ents = []
            for ent in detheified_ents:
                if ent.split(" ")[-1] != "of":
                    deofified_ents.append(ent)


            #remove all plurals
            depluralized_ents = []
            for ent in deofified_ents:
                if ent.find("'s") != -1:
                    ent = ent.replace("'s","")
                    depluralized_ents.append(ent)
                elif ent.find("s'") != -1:
                    ent = ent.replace("s'", "")
                    depluralized_ents.append(ent)
                else:
                    depluralized_ents.append(ent)

            #deduplicate again
            depluralized_ents = list(set(depluralized_ents))

            #remove any incorporateds or limiteds or things like that
            deincified_ents = []
            for ent in depluralized_ents:
                ent = ent.replace(", Incorporated", "").replace(", incorporated","").replace("Incorporated","").replace("incorporated","").replace(", Inc.","").replace(" Inc.","").replace(", Inc","").replace(", inc.","").replace(", inc", "").replace(" inc.","").replace("Corporation","").replace("corporation","").replace("Corp.","").replace("Corp","").replace("corp.","").replace("corp","")
                deincified_ents.append(ent.strip())

            
            #split slashes
            deslashified_ents = []
            for ent in deincified_ents:
                if ent.find("/") != -1:
                    slashsplit = ent.split("/")
                    for slsh in slashsplit:
                        deslashified_ents.append(slsh)
                else:
                    deslashified_ents.append(ent)

    
            #remove if they contain other things we aren't interested in
            keywords = ["initial","payments","payment","exclusiv","cohort","“","exchange commission",".gov",".com",".org",".edu","equity", "qui tam","filer","executive order","operating", "expense","obligation", "protocol","exchange comission","review","safe harb","=","an ", "guidelines","competition","response","fair","strategic", " – ", "preclinical","immuno-oncology","endpoint","observable"," to ","designation","ethics","orders"," or ","commercial","utr","viral","application","test","patented","competition","new","designation","xbrl","policy","drug discovery","revolving","intangible","asset","charge","controller","rebate","medicare","medicaid","equity invest","human capital","development","audit","human services","date","  ","scheme","regulatory","goodwill",'"ass',"diversity","learning","channel","herewith","digital self","issuer","+","rounds","telehealth","board","expenses","standards","fraud","d2c","b2b","ii","client","identify","rule","the company","short","compil","program","marketing","expenses","advertis","monte carlo","expanded","risk","qualitati","et.","al.","compile",".com","amendment","certficate","assets","member","strategy", "code","state","controls","procedures", "tax", " dx"," tx"," rx","product","civil","address","euro","treasury","h.r.", "relief","economic","location","function","lease","acquisition","u.s","e.u.","framework","congress","revenue","court","federal","national", "offering", "loan","equipment","plan","agreement","method","protection","interest","journal","stock","merger","®","property","panel", "programs","liquidity","litigation", "registrant","report","score","regulation", "data","operations","gaap", "act", first_part_of_name.lower(), "signature", "statement", "financial", "statute","compensation",ticker.lower(),"intellectual","law","statement","account","improvement","collab","supplemental","entit","trustee","balance","certification","accredit","section","research and", "item"]
            single_words = ["institutions","council","internal control","series","combination","cancer","bladder","kidney","esophagus","stomach","vaginal","cervical","ovarian","reproductive","cancers","commission","trademark","injection","finance","breast","lung","liver","colon","brain","heart","committee","trademarks","time","ltd.","facility","supply","review","","medicines","medicine","clinical","digital","advanced","biologics","policy","research","oncology","cybersecurity""building","buildings","schedule","chemistry","customer","m.d","sun","recognition","reliance","endocrine","company's",'“association',"food","access","contingencies","contingency","vp","institute","development","administration","legal","sciences","science","form","drug","guarantor","board","agency","analytics","ltd","llp","inc.","property","healthcare","company","securities","fair","state","health"]
            cleaned_ents = []
            for ent in deslashified_ents:
                kw_found = False
                for kw in keywords:
                    if ent.lower().find(kw) != -1:
                        kw_found = True
                if kw_found == False:
                    cleaned_ents.append(ent.replace('"',"").replace('"',""))

            
            #now split by ", " and add to new thing
            recleaned_ents = []
            for ent in cleaned_ents:
                if ent.find(", ") != -1:
                    sents = ent.split(", ")
                    for sent in sents:
                        recleaned_ents.append(sent)
                else:
                    recleaned_ents.append(ent)
            
            recleaned_ents = list(set(recleaned_ents))

            rerecleaned_ents = []
            for ent in recleaned_ents:
                if ent.find(" and ") != -1:
                    sents = ent.split(" and ")
                    for sent in sents:
                        rerecleaned_ents.append(sent)
                else:
                    rerecleaned_ents.append(ent)
            
            cleaned_ents = []
            for ent in rerecleaned_ents:
                kw_found = False
                for kw in keywords:
                    if ent.lower().find(kw) != -1:
                        kw_found = True
                if kw_found == False:
                    cleaned_ents.append(ent)

            cleaned_ents = list(set(cleaned_ents))

            #now check to see if the items are themselves equal to the single word no nos.
            sword_cleaned_ents = []
            for ent in cleaned_ents:
                swordfound = False
                for sword in single_words:
                    if ent.lower() == sword:
                        swordfound = True
                
                if swordfound == False:
                    if ent.isupper() == False:
                        sword_cleaned_ents.append((ent.replace("'s","").replace("s'","")))

            #remove all entities that are less than 3 characters long or if it contains more than 2 parentheses or start with "a" or "an"
            cleaned_ents = []
            for ent in sword_cleaned_ents:
                if len(ent) > 3:
                    if ent.find(")") < 2:
                        if ent.find("(") < 2:
                            if ent[0:1] != "a ":
                                if ent[0:2] != "an ":
                                    if ent[0] != '"':
                                        cleaned_ents.append(ent.replace(",","").strip())

            cleaned_ents = list(set(cleaned_ents))

            recleaned_ents = []
            for ent in cleaned_ents:
                kw_found = False
                for kw in keywords:
                    if ent.lower().find(kw) != -1:
                        kw_found = True
                if kw_found == False:
                    recleaned_ents.append(ent)


            #now check to see if the items are themselves equal to the single word no nos.
            sword_cleaned_ents = []
            for ent in recleaned_ents:
                swordfound = False
                for sword in single_words:
                    if ent.lower() == sword:
                        swordfound = True
                
                if swordfound == False:
                    if ent.isupper() == False:
                        sword_cleaned_ents.append((ent.replace("’s","").replace("s’","")))


            cleaned_ents = []
            for ent in sword_cleaned_ents:
                if ent[0].isupper() == True:
                    if ent[0].isnumeric() == False:
                        cleaned_ents.append(ent)
            
            recleaned_ents = []
            for ent in cleaned_ents:
                capital_letters = 0
                lowercase_letters = 0
                for i in len(ent):
                    if str(ent)[i].isupper():
                        capital_letters += 1
                    elif str(ent)[i].islower():
                        lowercase_letters += 1
                    elif str(ent)[i].isnumeric():
                        pass
                    else:
                        pass
                if lowercase_letters >= capital_letters:
                    recleaned_ents.append(str(ent))


            cleaned_ents = list(set(recleaned_ents))

            for ent in cleaned_ents:
                print(ent)
            


get_relationships("EDIT")
