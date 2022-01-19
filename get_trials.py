import os
from time import time
import get_details
import pandas as pd
from rapidfuzz import fuzz
import phARKma_utils
from phARKma_utils import timestamp
import get_trials
import trial_updater
import alive_progress
from alive_progress import alive_bar
from rapidfuzz import process, utils
import shutil
import logging
import sys
import time


def get_trials_primary(ticker):
    print(timestamp() + "Getting trials in which " + str(ticker) + " is the primary investigator.")
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    trial_database_found = False
    try:
        trials_database = pd.read_csv("trials_database.csv")
        trial_database_found = True
    except:
        trial_database_found = False
    
    if trial_database_found == True:
        with alive_bar(len(trials_database)) as bar:
            alive_handler = logging.StreamHandler(sys.stdout)
            for index, row in trials_database.iterrows():
                agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc")
                name = name.strip().lower()
                ratio = fuzz.ratio(name, agency)
                if ratio >= 90:
                    trials.append(row.astype(str))
                bar()

        return trials
    else:
        trial_updater.check_trial_deprecation_status(True)
        trials_database = pd.read_csv("trials_database.csv")
        with alive_bar(len(trials_database)) as bar:
            alive_handler = logging.StreamHandler(sys.stdout)
            for index, row in trials_database.iterrows():
                agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc")
                name = name.strip().lower()
                ratio = fuzz.ratio(name, agency)
                if ratio >= 90:
                    trials.append(row.astype(str))
                bar()

def get_trials_collaborator(ticker):
    print(timestamp() + "Getting trials in which " + str(ticker) + " is a collaborator.")
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    collabs = []
    trial_database_found = False
    try:
        trials_database = pd.read_csv("trials_database.csv")
        trial_database_found = True
    except:
        trial_database_found = False

    if trial_database_found == True:
        with alive_bar(len(trials_database)) as bar:
            alive_handler = logging.StreamHandler(sys.stdout)
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
                bar()

        return trials
    else:
        trial_updater.check_trial_deprecation_status(True)
        trials_database = pd.read_csv("trials_database.csv")
        with alive_bar(len(trials_database)) as bar:
            alive_handler = logging.StreamHandler(sys.stdout)
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
                bar()

        return trials
