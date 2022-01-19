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


def get_trials_primary(ticker, trials_database):
    print(timestamp() + "Getting trials in which " + str(ticker) + " is the primary investigator.")
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    name = name.strip().lower()
    df_dict = trials_database.to_dict("records")
    with alive_bar(len(df_dict)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for row in df_dict:
            agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc")
            ratio = fuzz.ratio(name, agency)
            if ratio >= 90:
                trials.append(row)
            bar()
        return trials


def get_trials_collaborator(ticker, trials_database):
    print(timestamp() + "Getting trials in which " + str(ticker) + " is a collaborator.")
    details = get_details.get_details(ticker)
    name = details["NAME"]
    name_split = name.split(" ")
    if len(name_split) > 2:
        name = name_split[0] + " " + name_split[1]
    name = name.replace(".","")
    name = name.strip()
    trials = []
    name = name.strip().lower()
    df_dict = trials_database.to_dict("records")
    with alive_bar(len(df_dict)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for row in df_dict:
            found = False
            collabs = row["COLLABORATORS"].split(";")
            for collab in collabs:
                ratio = fuzz.ratio(name, collab)
                if ratio >= 90:
                    found = True
                if found == True:
                    trials.append(row)
            bar()
        return trials