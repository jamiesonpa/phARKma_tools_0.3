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
    print(timestamp() + "Adding new entry " + trial["ID"] + " for company " + ticker + " to "+ table_name + " table.")
    hdr = {"Authorization": "Bearer key9lRgCd32KG0vDx","Content-Type": "application/json"}
    record_url = "https://api.airtable.com/v0/"+config.at_base_key+"/Clinical%20Trials"
    processed_trial = {}
    for key in trial.keys():
        processed_trial[key] = str(trial[key])
    new_data = {
        "records": [
            {
                "fields": processed_trial
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

