import os
from time import time
import get_details
import pandas as pd
from fuzzywuzzy import fuzz
import phARKma_utils
from phARKma_utils import timestamp


def get_trials_primary(ticker):
    print(timestamp() + "Getting trials from " + str(ticker))
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    trials_database = pd.read_csv("/Users/piercejamieson/Desktop/Scripts/12_9_2021/trials_database.csv")
    for index, row in trials_database.iterrows():
        agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc")
        name = name.strip().lower()
        ratio = fuzz.ratio(name, agency)
        if ratio >= 90:
            trials.append(row.astype(str))

    return trials

def get_trials_collaborator(ticker):
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    collabs = []
    trials_database = pd.read_csv("trials_database.csv")
    print("checking trials database for trials run by "+ name)
    for index, row in trials_database.iterrows():
        collabs = row["COLLABORATORS"].split(";")
        found = False
        for collab in collabs:
            name = name.strip().lower()
            ratio = fuzz.ratio(name, collab)
            if ratio >= 90:
                found = True
        if found == True:
            trials.append(row.astype(str))

    return trials
