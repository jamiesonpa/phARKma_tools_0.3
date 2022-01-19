from get_arkg_tickers import get_arkg_tickers
import get_trials
import requests
import pandas as pd
import json
from fuzzywuzzy import fuzz
from airtable import Airtable
from pprint import pprint
import config

base_key = config.at_base_key
table_name = "Clinical Trials"
api_key = config.at_api_key
airtable = Airtable(base_key, table_name, api_key)


def get_airtable_records(at):
    pages = airtable.get_iter(maxRecords=100000)
    records = []
    for page in pages:
        for record in page:
            records.append(record)
    return records

def delete_record(record_id):
    pass

def remove_duplicate_records(base_id):
    record_strings = []
    for record in get_airtable_records(base_id):
        recordstring = ""
        for key in record["fields"].keys():
            recordstring = recordstring + ";" + record["fields"][key]
        record_id = record["id"]
        record_strings.append((record_id, recordstring))

    for rs in record_strings:
        current_rs = rs[1]
        for check_rs in record_strings:
            fuzzratio = fuzz.ratio(check_rs[1], current_rs)
            if fuzzratio > 97:
                if check_rs[0] != rs[0]:
                    print("found duplicate value in table between ID " + check_rs[0] + " and " + rs[0] + " with a ratio of " + str(fuzzratio))

def check_for_existing_record(base_key, search_term, search_field):
    airtable_records = get_airtable_records(base_key)
    found = False
    id = ""
    for record in airtable_records:
        if record["fields"][search_field] == search_term:
            print("found record in table " + base_key + " that matches search term " + search_term + " in the " + search_field + " field. Returning ID")
            found = True
            id = record["id"]
    
    if found == False:
        print("Could not find any records matching the query search term in the query's indicated field.")
        id = "not found"
    
    return id

def add_clinical_trial(trial, ticker):
    trial = trial.to_dict()
    hdr = {"Authorization": "Bearer key9lRgCd32KG0vDx","Content-Type": "application/json"}
    record_url = "https://api.airtable.com/v0/appGKqhHkbjMTFvu9/Clinical%20Trials"
    record_exists = False
    record_exists = check_for_existing_record(str(trial["ID"]), "NCT ID")
    if record_exists == True:
        print("Found record " + str(trial["ID"]) + " in the airtable clinical trials database already.")
    else:
        print("Did not find " + str(trial["ID"]) + " in clinical trials database. Adding now...")
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

