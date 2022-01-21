import os
from time import time
import get_details
import pandas as pd
from rapidfuzz import fuzz, process
import phARKma_utils
from phARKma_utils import timestamp, process_name
import get_trials
import trial_updater
import alive_progress
from alive_progress import alive_bar
from rapidfuzz import process, utils
import shutil
import logging
import sys
import time
import Levenshtein as lev

def get_trials_primary(ticker, trials_database):
    name = get_details.get_company_name(ticker)
    name = process_name(name)
    trials = []
    print(timestamp() + "Getting trials in which '" + str(name) + "' is the primary investigator.")
    df_dict = trials_database.to_dict("records")
    nullreturn = False
    threshold = 98
    while nullreturn == False:
        threshold = threshold - 1
        if threshold < 95:
            nullreturn = True
            break
        with alive_bar(len(df_dict)) as bar:
            alive_handler = logging.StreamHandler(sys.stdout)
            for row in df_dict:
                if row["AGENCY_CLASS"] == "Industry":
                    agency = process_name(row["AGENCY"])
                    ratio = round(lev.ratio(name, agency)*100, 2)
                    if ratio >= threshold:
                        trials.append(row)
                bar()
        if len(trials) > 0:
            nullreturn = True
    return trials


def get_trials_collaborator(ticker, trials_database):
    name = get_details.get_company_name(ticker)
    name = process_name(name)
    trials = []
    print(timestamp() + "Getting trials in which '" + str(name) + "' is a collaborating investigator.")
    df_dict = trials_database.to_dict("records")
    with alive_bar(len(df_dict)) as bar:
        # alive_handler = logging.StreamHandler(sys.stdout)
        for row in df_dict:
            collabs = row["COLLABORATORS"].split(";")
            for collab in collabs:
                collab = process_name(collab)
                ratio = round(lev.ratio(name, collab)*100, 2)
                if ratio >= 95:
                    trials.append(row)
            bar()
    return trials