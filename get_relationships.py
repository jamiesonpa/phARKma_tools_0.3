from platform import release
from anyio import current_effective_deadline
from bleach import clean
from get_details import get_details
from phARKma_utils import timestamp
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

alphavantage_api_key = config.alphavantage_api_key
polygon_api_key = config.polygon_api_key
edgar_api_key = config.edgar_api_key


def get_filings(name, year, ticker, cik, form):
    query = {
    "query": name,
    "formTypes": [form],
    "startDate": str(year)+"-01-01",
    "endDate": str(year)+"-12-31",
    }
    fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
    counter = 0
    found = False
    filings = None
    while counter < 5:
        try:
            filings = fullTextSearchApi.get_filings(query)
            counter = 5
        except:
            time.sleep(1)
            counter +=1
    
    if filings != None:
        for filing in filings["filings"]:
            
            if str(filing["ticker"]) == ticker:
                found = True

    
    if found == False:
        query = {
        "query": name,
        "formTypes": [form],
        "startDate": str(year-1)+"-01-01",
        "endDate": str(year-1)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True
    
    if found == False:
        query = {
        "query": ticker,
        "formTypes": [form],
        "startDate": str(year)+"-01-01",
        "endDate": str(year)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True
    
    if found == False:
        query = {
        "query": ticker,
        "formTypes": [form],
        "startDate": str(year-1)+"-01-01",
        "endDate": str(year-1)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    if found == False:
        query = {
        "query": name.upper(),
        "formTypes": [form],
        "startDate": str(year)+"-01-01",
        "endDate": str(year)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    if found == False:
        query = {
        "query": name.upper(),
        "formTypes": [form],
        "startDate": str(year-1)+"-01-01",
        "endDate": str(year-1)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    if found == False:
        query = {
        "query": name.upper(),
        "formTypes": [form],
        "startDate": str(year-1)+"-01-01",
        "endDate": str(year-1)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True


    if found == False:
        if cik != "not found":
            query = {
            "query": name.upper(),
            "formTypes": [form],
            "startDate": str(year)+"-01-01",
            "endDate": str(year)+"-12-31",
            }
            fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
            counter = 0
            while counter < 5:
                try:
                    filings = fullTextSearchApi.get_filings(query)
                    break
                except:
                    time.sleep(1)
                    counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    if found == False:
        if cik != "not found":
            query = {
            "query": name.upper(),
            "formTypes": [form],
            "startDate": str(year-1)+"-01-01",
            "endDate": str(year-1)+"-12-31",
            }
            fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
            counter = 0
            while counter < 5:
                try:
                    filings = fullTextSearchApi.get_filings(query)
                    break
                except:
                    time.sleep(1)
                    counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    first_part_of_name = name.split(" ")[0]
    if found == False:
        query = {
        "query": first_part_of_name,
        "formTypes": [form],
        "startDate": str(year-1)+"-01-01",
        "endDate": str(year-1)+"-12-31",
        }
        fullTextSearchApi = FullTextSearchApi(api_key=edgar_api_key)
        counter = 0
        while counter < 5:
            try:
                filings = fullTextSearchApi.get_filings(query)
                break
            except:
                time.sleep(1)
                counter +=1

        if filings != None:
            for filing in filings["filings"]:
                
                if str(filing["ticker"]) == ticker:
                    found = True

    if found == False:
        print(timestamp() + "couldnt find " + form + " filings for " + name + " or " + ticker)
        return None
    else:
        return filings

def get_matches(filings, ticker, form):
    tickermatches = []
    for filing in filings["filings"]:
        if str(filing["ticker"]) == ticker:
            tickermatches.append(filing)
    
    filing_urls = []
    print(timestamp() + "found the following correct filings:")
    for match in tickermatches:
        if match["formType"] == form:
            if match["type"].find("EX") == -1:
                print(timestamp() + str(match))
                filing_urls.append(match["filingUrl"])  

    if len(filing_urls) == 0:
        print(timestamp() + "No filings were found with matching ticker to " + ticker)
        return None
    else:
        return filing_urls

def parse_sentences(matches):
    print(timestamp() + "parsing sentences")
    if matches != None:
        divtext_list =[]
        for filing_url in matches:
            hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
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
        doc = ""
        for sentence in long_strings:
            doc = doc + sentence + " "
        return doc
    else:
        return None

def process_entities(name, ticker, ents, model):

    first_part_of_name = name.split(" ")[0]

    #define countries
    with open("countries.txt") as readfile:
        countries = readfile.read().split("\n")
    #define states
    with open("states.txt") as readfile:
        states = readfile.read().split("\n")

    #define months
    with open("months.txt") as readfile:
        months = readfile.read().split("\n")

    #remove all countries
    decountrified_ents = []
    for ddent in ents:
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
    keywords = ["discovery","demonstr", "form","registr","beneficial", " in ", "parameter", "licens","known"," of ","occupational","fortune","star ratings","combinations","business ","screen","certificate","requirements","™","conservancy","monte-carlo","carlo","patent","rights","initial","complexes","exemption","exempt","payments","payment","exclusiv","cohort","“","exchange commission",".gov",".com",".org",".edu","equity", "qui tam","filer","executive order","operating", "expense","obligation", "protocol","exchange comission","review","safe harb","=","an ", "guidelines","competition","response","fair","strategic", " – ", "preclinical","immuno-oncology","endpoint","observable"," to ","designation","ethics","orders"," or ","commercial","utr","viral","application","test","patented","competition","new","designation","xbrl","policy","drug discovery","revolving","intangible","asset","charge","controller","rebate","medicare","medicaid","equity invest","human capital","development","audit","human services","date","  ","scheme","regulatory","goodwill",'"ass',"diversity","learning","channel","herewith","digital self","issuer","+","rounds","telehealth","board","expenses","standards","fraud","d2c","b2b","ii","client","identify","rule","the company","short","compil","program","marketing","expenses","advertis","monte carlo","expanded","risk","qualitati","et.","al.","compile",".com","amendment","certficate","assets","member","strategy", "code","state","controls","procedures", "tax", " dx"," tx"," rx","product","civil","address","euro","treasury","h.r.", "relief","economic","location","function","lease","acquisition","u.s","e.u.","framework","congress","revenue","court","federal","national", "offering", "loan","equipment","plan","agreement","method","protection","interest","journal","stock","merger","®","property","panel", "programs","liquidity","litigation", "registrant","report","score","regulation", "data","operations","gaap", "act", first_part_of_name.lower(), "signature", "statement", "financial", "statute","compensation",ticker.lower(),"intellectual","law","statement","account","improvement","collab","supplemental","entit","trustee","balance","certification","accredit","section","research and", "item"]
    single_words = ["capital markets","type","primer","prospectus","distribution","prevention","control","change","metabolism","foundation", "authority","consolidation","translational", "library","research services","inc.","inc","incorporated","ltd","ltd.","llc","llc.","limited","corp.","corp","corporation","company","capital","therapeutics","technology","institutions","council","order","cellular","cell","success","internal control","series","combination","cancer","bladder","kidney","esophagus","stomach","vaginal","cervical","ovarian","reproductive","cancers","commission","trademark","injection","finance","breast","lung","liver","colon","brain","heart","committee","trademarks","time","ltd.","facility","supply","review","","medicines","medicine","clinical","digital","advanced","biologics","policy","research","oncology","cybersecurity""building","buildings","schedule","chemistry","customer","m.d","sun","recognition","reliance","endocrine","company's",'“association',"food","access","contingencies","contingency","vp","institute","development","administration","legal","sciences","science","form","drug","guarantor","board","agency","analytics","ltd","llp","inc.","property","healthcare","company","securities","fair","state","health"]
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
        for i in range(0,len(ent)):
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

    cleaned_ents = []
    for ent in recleaned_ents:
        if ent.find(" ") == -1:
            if ent.find("ology") == -1:
                cleaned_ents.append(ent)
        else:
            cleaned_ents.append(ent)

    recleaned_ents = []
    for ent in cleaned_ents:
        if ent.lower().find("drug admin") != -1:
            recleaned_ents.append("Food and Drug Administration")
        else:
            recleaned_ents.append(ent)


    cleaned_ents = list(set(recleaned_ents))
    return cleaned_ents

def process_text(name, ticker, doc):
    model_loaded = False
    try:
        nlp = spacy.load("en_core_web_lg")
        model_loaded = True
        print(timestamp() + "model loaded")
    except:
        print(timestamp() + "Error: you may not have the correct spacy python model installed on your system, try running 'python -m spacy download en_core_web_lg'")

    if model_loaded == True:
        print(timestamp() + "proceeding with text processing")

        try:
            mod = nlp(doc)
            print(timestamp() + "training on unexpanded")
        except:
            mod = nlp(doc[0:1000000])
            print(timestamp() + "training on truncated")

        ents = []
        for X in mod.ents:
            if X.label_ == "ORG":
                ents.append(X.text)

        deduplicated_ents = list(set(ents))
        print(timestamp() + "processing " + str(len(deduplicated_ents)) + " entities")
        processed_ents = process_entities(name, ticker, deduplicated_ents, mod)

        final_clean = []
        for ent in processed_ents:
            final_clean.append(ent.replace(".",""))
        return final_clean

    else:
        return None
        print(timestamp() + "couldnt load NLP model")

def get_relationships(ticker):
    name_found = False
    cik = "not found"
    details = get_details(ticker, False)
    name = details["NAME"]
    print(timestamp() + "name found: " + name)
    name_found = True
    try:
        first_part_of_name = name.split(" ")[0]
    except:
        pass
    try:
        cik = details["CIK"]
    except:
        print(timestamp() + "couldn't fetch CIK ID")

    if name_found == True:
        current_year = int(datetime.datetime.now().year)
        session = requests.Session()
        session.params["apiKey"] = polygon_api_key
        print(timestamp() + "getting filings for " + name + ", "+ ticker + ", " + str(cik))
        filings = get_filings(name, current_year, ticker, str(cik), "10-K")
        s1 = False
        if filings == None:
            filings = get_filings(name, current_year, ticker, str(cik), "S-1")
            s1 = True
        if filings != None:
            if s1:
                matches = get_matches(filings, ticker, "S-1")
            else:
                matches = get_matches(filings, ticker, "10-K")
            doc = parse_sentences(matches)
            entities = process_text(name, ticker, doc)
        return entities
    
    else:
        return None


    
