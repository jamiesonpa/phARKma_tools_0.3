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

    name = get_details.get_company_name(ticker)
    print(timestamp() + "Getting trials in which " + str(name) + " is the primary investigator.")
    name = name.lower()
    name = name.replace(".","")
    name = name.replace(",","")
    name = name.strip()
    name = name.replace("corporation", "corp")
    name = name.replace("corp", "corporation")
    name = name.replace("incorporated","inc")
    trials = []
    name = name.strip().lower()
    print("New name is " + name)
    df_dict = trials_database.to_dict("records")
    with alive_bar(len(df_dict)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for row in df_dict:
            agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc")
            ratio = fuzz.ratio(name, agency)
            if ratio >= 95:
                trials.append(row)
            bar()
        threshold = 95

        nullreturn = False
        while nullreturn == False:
            if threshold > 85:
                nullreturn = True
                break
            threshold = threshold - 3
            with alive_bar(len(df_dict)) as bar:
                alive_handler = logging.StreamHandler(sys.stdout)
                for row in df_dict:
                    agency = row["AGENCY"].replace('"',"").strip().lower().replace(".","").replace(",","").replace("incorporated", "inc").replace("corporation","corp")
                    ratio = fuzz.ratio(name, agency)
                    if ratio >= threshold:
                        trials.append(row)
                    bar()
            if len(trials) > 0:
                    break


        return trials


def get_trials_collaborator(ticker, trials_database):
    print(timestamp() + "Getting trials in which " + str(ticker) + " is a collaborator.")
    name = get_details.get_company_name(ticker)
    name = name.lower()
    name = name.replace(".","")
    name = name.replace("corporation", "corp")
    name = name.replace("corp", "corporation")
    name = name.replace("incorporated","inc")
    name = name.replace(".","")
    name = name.strip()
    trials = []
    name = name.strip().lower()
    print("New name is " + name)
    df_dict = trials_database.to_dict("records")
    with alive_bar(len(df_dict)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for row in df_dict:
            found = False
            collabs = row["COLLABORATORS"].split(";")
            for collab in collabs:
                ratio = fuzz.ratio(name, collab)
                if ratio >= 95:
                    found = True
                if found == True:
                    trials.append(row)
            bar()
    threshold = 95
    nullreturn = False
    while nullreturn == False:
        if threshold > 85:
            nullreturn = True
            break
        else:
            threshold = threshold - 3
            with alive_bar(len(df_dict)) as bar:
                alive_handler = logging.StreamHandler(sys.stdout)
                for row in df_dict:
                    found = False
                    collabs = row["COLLABORATORS"].split(";")
                    for collab in collabs:
                        ratio = fuzz.ratio(name, collab)
                        if ratio >= threshold:
                            found = True
                        if found == True:
                            trials.append(row)
                    bar()
            if len(trials) > 0:
                break

    return trials