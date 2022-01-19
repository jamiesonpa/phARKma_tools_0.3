from get_arkg_tickers import get_arkg_tickers
import get_trials
import requests
import pandas as pd
import json
from rapidfuzz import fuzz
from airtable import Airtable
from pprint import pprint
import config
from phARKma_utils import timestamp
import alive_progress
from alive_progress import alive_bar
import shutil
import logging
import sys
import time

base_key = config.at_base_key
api_key = config.at_api_key


def get_airtable_records(table_name):
    airtable = Airtable(base_key, table_name, api_key)
    pages = airtable.get_iter(maxRecords=100000)
    records = []
    for page in pages:
        for record in page:
            records.append(record)
    return records

def delete_record(record_id, table_name):
    id_list = [record_id]
    airtable = airtable = Airtable(base_key, table_name, api_key)
    airtable.batch_delete(id_list)

def remove_duplicate_records(table_name):
    print(timestamp() + "Attempting to remove duplicate records from airtable")
    base_id = base_key
    organizer_study_ids = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        osid = record["fields"]["ORGANIZER STUDY ID"]
        organizer_study_ids.append((record_id, osid))

    with alive_bar(len(organizer_study_ids)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for id in organizer_study_ids:
            current_id = id
            for check_id in organizer_study_ids:
                fuzzratio = fuzz.ratio(check_id[1], current_id[1])
                if fuzzratio > 97:
                    if check_id[0] != id[0]:
                        print(timestamp() + "Duplicate record value found between " + check_id[1] + " and " + id[1] + ". Deleting...")
                        delete_record(id[0], table_name)
                        organizer_study_ids.remove((id[0],id[1]))
            bar()
    print(timestamp() + "Duplicate records successfully removed from " + table_name)

def check_for_existing_record(table_name, search_term, search_field):
    airtable_records = get_airtable_records(table_name)
    found = False
    id = ""
    for record in airtable_records:
        if record["fields"][search_field] == search_term:
            print(timestamp() + "Found record in table " + base_key + " that matches search term " + search_term + " in the " + search_field + " field. Returning ID")
            found = True
            id = record["id"]
    
    if found == False:
        print(timestamp() + "Could not find any records matching the query search term in the query's indicated field.")
        id = "not found"
    
    return id

def add_clinical_trial(table_name, trial, ticker):
    trial = trial.to_dict()
    hdr = {"Authorization": "Bearer key9lRgCd32KG0vDx","Content-Type": "application/json"}
    record_url = "https://api.airtable.com/v0/appGKqhHkbjMTFvu9/Clinical%20Trials"
    record_exists = False
    record_exists = check_for_existing_record(str(trial["ID"]), "ORGANIZER STUDY ID")
    if record_exists == True:
        print(timestamp() + "Found record " + str(trial["ID"]) + " in the airtable clinical trials database already.")
    else:
        print(timestamp() + "Did not find " + str(trial["ID"]) + " in clinical trials database. Adding now...")
    if record_exists == False:
        new_data = {
            "records": [
                {
                    "fields": {
                        "TICKER": ticker,
                        "NCT ID": str(trial["ID"]),
                        "OFFICIAL TITLE": str(trial["OFFICIAL TITLE"]),
                        "ORGANIZER STUDY ID": str(trial["ORGANIZER STUDY ID"]),
                        "TITLE": str(trial["TITLE"]),
                        "INTERVENTION_TYPE": str(trial["INTERVENTION_TYPE"]),
                        "STATUS": str(trial["STATUS"]),
                        "WHY_STOP": str(trial["WHY_STOP"]),
                        "SUMMARY": str(trial["SUMMARY"]),
                        "DESCRIPTION": str(trial["DESCRIPTION"]),
                        "PHASE": str(trial["PHASE"]),
                        "ENROLLMENT": str(trial["ENROLLMENT"]),
                        "INTERVENTION_MODEL": str(trial["INTERVENTION_MODEL"]),
                        "MASKING": str(trial["MASKING"]),
                        "ALLOCATION": str(trial["ALLOCATION"]),
                        "PURPOSE": str(trial["PURPOSE"]),
                        "CONDITION": str(trial["CONDITION"]),
                        "DRUG": str(trial["DRUG"]),
                        "GENDER": str(trial["GENDER"]),
                        "MIN_AGE": str(trial["MIN_AGE"]),
                        "MAX_AGE": str(trial["MAX_AGE"]),
                        "CITY": str(trial["CITY"]),
                        "STATE": str(trial["STATE"]),
                        "COUNTRY": str(trial["COUNTRY"]),
                        "STUDY FIRST SUBMITTED": str(trial["STUDY FIRST SUBMITTED"]),
                        "STUDY FIRST POSTED": str(trial["STUDY FIRST POSTED"]),
                        "COMPLETION DATE": str(trial["COMPLETION DATE"]),
                        "PRIMARY COMPLETION DATE": str(trial["PRIMARY COMPLETION DATE"]),
                        "LAST UPDATE SUBMITTED": str(trial["LAST UPDATE SUBMITTED"]),
                        "EXPANDED_ACCESS": str(trial["EXPANDED_ACCESS"]),
                        "URL": str(trial["URL"]),
                        "AGENCY": str(trial["AGENCY"]),
                        "COLLABORATORS": str(trial["COLLABORATORS"]),
                        "AGENCY_CLASS": str(trial["AGENCY_CLASS"]),
                        "HAS RESULTS": str(trial["HAS RESULTS"])
                    }
                }
            ]
        }
        response = requests.post(record_url, headers=hdr, data = json.dumps(new_data))

def get_table_fields(table_name):
    records = get_airtable_records(table_name)
    columns = []
    for key in records[0]["fields"].keys():
        columns.append(key)
    return columns

