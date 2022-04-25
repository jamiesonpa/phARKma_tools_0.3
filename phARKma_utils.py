import datetime
from datetime import datetime
import pandas as pd
import trial_updater
import get_details
import requests
import bs4
from bs4 import BeautifulSoup
from collections import Counter

stripJunk = str.maketrans("","","- ")

def removeDigits(s):
    answer = []
    for char in s:
        if not char.isdigit():
            answer.append(char)
    return ''.join(answer)


def getRatio(a,b):
    a = a.lower().translate(stripJunk)
    b = b.lower().translate(stripJunk)
    total  = len(a)+len(b)
    counts = (Counter(a)-Counter(b))+(Counter(b)-Counter(a))
    return 100 - 100 * sum(counts.values()) / total


def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = "[" + (dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")) + "]: "
    return timestampStr

def get_trials_database():
    print(timestamp() + "Fetching clinical trials csv database...")
    trial_database_found = False
    try:
        trials_database = pd.read_csv("auxillary_data/trials_database.csv")
        trial_database_found = True
    except:
        trial_database_found = False
    if trial_database_found == True:
        return trials_database
    else:
        trial_updater.check_trial_deprecation_status(True)
        trials_database = pd.read_csv("auxillary_data/trials_database.csv")
        return trials_database

def process_name(name):
    name = name.lower()
    name = name.replace(".","")
    name = name.replace(",","")
    name = name.replace('"',"")
    name = name.replace(";","")
    if name.find(" /") != -1:
        name = name = name.split(" /")[0]
    if name.find("a/s"):
        name = name.replace("a/s","")
    if name.find(" north america") != -1:
        name = name.replace(" north america", "")
    if name.find(" development center americas") != -1:
        name = name.replace(" development center americas", "")
    if name.find("corporation") != -1:
        name = name.replace("corporation", "")
    if name.find("incorporated") != -1:
        name = name.replace("incorporated", "")
    if name.find(" corp") != -1:
        name = name.replace(" corp", "")
    if name.find(" coltd") != -1:
        name = name.replace(" coltd", "")
    if name.find(" limited") != -1:
        name = name.replace(" limited", "")
    if name.find(" group") != -1:
        name = name.replace(" group", "")
    if name.find(" lifesciences") != -1:
        name = name.replace(" lifesciences", "")
    if name.find(" biomedical") != -1:
        name = name.replace(" biomedical", "")
    if name.find(" medical") != -1:
        name = name.replace(" medical", "")
    if name.find(" biosciences") != -1:
        name = name.replace(" biosciences", "")
    if name.find(" biotherapeutics") != -1:
        name = name.replace(" biotherapeutics", "")
    if name.find(" biotechnologies") != -1:
        name = name.replace(" biotechnologies", "")
    if name.find(" technologies") != -1:
        name = name.replace(" technologies", "")
    if name.find(" biotechnology") != -1:
        name = name.replace(" biotechnology", "")
    if name.find(" technology") != -1:
        name = name.replace(" technology", "")
    if name.find(" biologics") != -1:
        name = name.replace(" biologics", "")
    if name.find(" biopharmaceuticals") != -1:
        name = name.replace(" biopharmaceuticals", "")
    if name.find(" biopharmaceutical") != -1:
        name = name.replace(" biopharmaceutical", "")
    if name.find(" biopharma") != -1:
        name = name.replace(" biopharma", "")
    if name.find(" biopharm") != -1:
        name = name.replace(" biopharm", "")
    if name.find(" biomedical") != -1:
        name = name.replace(" biomedical", "")
    if name.find(" bioscience") != -1:
        name = name.replace(" bioscience", "")
    if name.find(" health") != -1:
        name = name.replace(" health", "")
    if name.find(" medicine") != -1:
        name = name.replace(" medicine", "")
    if name.find(" labs") != -1:
        name = name.replace(" labs", "")
    if name.find(" a ") != -1:
        name = name.split(" a ")[0]
    if name.find(" biotech") != -1:
        name = name.replace(" biotech", "")
    if name.find(" biotech") != -1:
        name = name.replace(" biotech", "")
    if name.find(" pvt") != -1:
        name = name.replace(" pvt", "")
    if name.find(" inc") != -1:
        name = name.replace(" inc", "")
    if name.find(" ltd") != -1:
        name = name.replace(" ltd", "")
    if name.find(" llc") != -1:
        name = name.replace(" llc", "")
    if name.find(" llc") != -1:
        name = name.replace(" llc", "")
    if name.find(" pharmaceuticals") != -1:
        name = name.replace(" pharmaceuticals","")
    if name.find(" pharmaceutical") != -1:
        name = name.replace(" pharmaceutical","")
    if name.find("therapeutics") != -1:
        name = name.replace("therapeutics", "")
    if name.find(" pharma") != -1:
        name = name.replace(" pharma","")
    if name.find(" pharm") != -1:
        name = name.replace(" pharm","")
    if name.find(" sciences") != -1:
        name = name.replace(" sciences", "")
    if name.find(" therapy") != -1:
        name = name.replace(" therapy", "")
    if name.find(" holdings") != -1:
        name = name.replace(" holdings", "")
    if name.find(" co") != -1:
        name = name.replace(" co", "")
    if name.find("  ") != -1:
        name = name.replace("  "," ")
    if name.find("american depositary shares") != -1:
        name = name.replace("american depositary shares","")
    name = name.strip()
    return name