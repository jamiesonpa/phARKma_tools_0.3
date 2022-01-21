from charset_normalizer import api
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
import Levenshtein as lev
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
    try:
        airtable.batch_delete(id_list)
        print("deleted")
    except:
        print("could not delete")
        pass

def remove_duplicate_records_force_clinical_trials(table_name):
    print(timestamp() + "Attempting to remove duplicate records from table " + table_name)
    base_id = base_key
    recordstrings = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        record_string = record["fields"]["TICKER"]+record["fields"]["URL"] + record["fields"]["ORGANIZER STUDY ID"]
        recordstrings.append((record_id, record_string))

    with alive_bar(len(recordstrings)) as bar:
        for id in recordstrings:
            current_id = id
            for check_id in recordstrings:
                fuzzratio = lev.ratio(check_id[1], current_id[1])
                if fuzzratio > 97:
                    if check_id[0] != id[0]:
                        print(timestamp() + "Duplicate record value found between " + check_id[1] + " and " + id[1] + ". Deleting...")
                        delete_record(id[0], table_name)
                        recordstrings.remove((id[0],id[1]))
            bar()
    print(timestamp() + "Duplicate records successfully removed from " + table_name)

def remove_duplicate_records_clinical_trials(table_name):
    print(timestamp() + "Attempting to remove duplicate records from table " + table_name)
    base_id = base_key
    organizer_study_ids = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        osid = record["fields"]["ORGANIZER STUDY ID"]
        organizer_study_ids.append((record_id, osid))

def remove_duplicate_records_mean_analyst_ratings(table_name):
    print(timestamp() + "Attempting to remove duplicate records from table " + table_name)
    base_id = base_key
    total_ids = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        id_string = record["fields"]["TICKER"]
        total_ids.append((record_id, id_string))

    with alive_bar(len(total_ids)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for id in total_ids:
            current_id = id
            for check_id in total_ids:
                fuzzratio = fuzz.ratio(check_id[1], current_id[1])
                if fuzzratio > 97:
                    if check_id[0] != id[0]:
                        print(timestamp() + "Duplicate record value found between " + check_id[1] + " and " + id[1] + ". Deleting...")
                        delete_record(id[0], table_name)
                        try:
                            total_ids.remove((id[0],id[1]))
                        except:
                            pass
            bar()
    print(timestamp() + "Duplicate records successfully removed from " + table_name)

def remove_duplicate_records_historical_analyst_ratings(table_name):
    print(timestamp() + "Attempting to remove duplicate records from table " + table_name)
    base_id = base_key
    total_ids = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        id_string = record["fields"]["TICKER"] + record["fields"]["DATE"] + record["fields"]["FIRM"]
        total_ids.append((record_id, id_string))

    with alive_bar(len(total_ids)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for id in total_ids:
            current_id = id
            for check_id in total_ids:
                fuzzratio = fuzz.ratio(check_id[1], current_id[1])
                if fuzzratio > 97:
                    if check_id[0] != id[0]:
                        print(timestamp() + "Duplicate record value found between " + check_id[1] + " and " + id[1] + ". Deleting...")
                        delete_record(id[0], table_name)
                        try:
                            total_ids.remove((id[0],id[1]))
                        except:
                            pass
            bar()
    print(timestamp() + "Duplicate records successfully removed from " + table_name)

def remove_duplciate_records_financial(table_name):
    print(timestamp() + "Attempting to remove duplicate records from table " + table_name)
    base_id = base_key
    total_ids = []
    for record in get_airtable_records(table_name):
        record_id = record["id"]
        id_string = record["fields"]["TICKER"] + record["fields"]["DATE"] + record["fields"]["METRIC"]
        total_ids.append((record_id, id_string))

    with alive_bar(len(total_ids)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for id in total_ids:
            current_id = id
            for check_id in total_ids:
                fuzzratio = fuzz.ratio(check_id[1], current_id[1])
                if fuzzratio > 97:
                    if check_id[0] != id[0]:
                        print(timestamp() + "Duplicate record value found between " + check_id[1] + " and " + id[1] + ". Deleting...")
                        delete_record(id[0], table_name)
                        try:
                            total_ids.remove((id[0],id[1]))
                        except:
                            pass
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

def add_record(base_id, table_name, at_api_key, record, ticker):
    airtable = Airtable(base_id,table_name, at_api_key)
    record["TICKER"] = ticker
    clean_record = {}
    for key in record.keys():
        clean_record[key] = str(record[key])
    airtable.insert(clean_record)

def get_table_fields(table_name):
    records = get_airtable_records(table_name)
    columns = []
    for key in records[0]["fields"].keys():
        columns.append(key)
    return columns

