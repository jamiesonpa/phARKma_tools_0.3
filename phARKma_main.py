from turtle import update
import trial_updater
import get_company_data
import phARKma_utils
import get_relationships
import get_trials
import trial_updater
import airtable_utils
import get_condition_category
import get_arkg_tickers
import get_details
import get_commercialized_drugs
import config
import get_analyst_ratings
import sys
import logging
import alive_progress
from alive_progress import alive_bar

def update_mean_analyst_ratings_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    print(phARKma_utils.timestamp() + "Updating Analyst Ratings table...")
    with alive_bar(len(tickers)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for ticker in tickers:
            mean_rating = get_analyst_ratings.get_mean_analyst_rating(ticker, False)
            mean_rating_value = mean_rating[0]
            mean_rating_designation = mean_rating[1]
            mratings = {}
            mratings["TICKER"] = ticker
            mratings["MEAN RATING"] = str(mean_rating_value)
            mratings["DESIGNATION"] = str(mean_rating_designation)
            airtable_utils.add_record(config.at_base_key, "Analyst Ratings",config.at_api_key, mratings, ticker)
            bar()
    
    airtable_utils.remove_duplicate_records_mean_analyst_ratings("Analyst Ratings")

def update_ratings_history_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    print(phARKma_utils.timestamp() + "Updating Analyst Rating History table...")
    with alive_bar(len(tickers)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for ticker in tickers:
            rating_history = get_analyst_ratings.get_rating_history(ticker, False)
            for index, row in rating_history.iterrows():
                rhist = {}
                rhist["TICKER"] = row["TICKER"]
                rhist["DATE"] = row["DATE"]
                rhist["FIRM"] = row["FIRM"]
                rhist["ACTION"] = row["ACTION"]
                rhist["FROM"] = row["FROM"]
                rhist["TO"] = row["TO"]
                airtable_utils.add_record(config.at_base_key, "Analyst Rating History",config.at_api_key, rhist, ticker)
            bar()
    
    airtable_utils.remove_duplicate_records_historical_analyst_ratings("Analyst Rating History")

def update_drugs():
    pass

def update_clinical_trials_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    trials_database = phARKma_utils.get_trials_database()
    for ticker in tickers:
        trials = get_trials.get_trials_primary(ticker, trials_database)
        collab_trials = get_trials.get_trials_collaborator(ticker, trials_database)
        for trial in trials:
            airtable_utils.add_record(config.at_base_key, "Clinical Trials",config.at_api_key, trial, ticker)
        for trial in collab_trials:
            airtable_utils.add_record(config.at_base_key, "Clinical Trials",config.at_api_key, trial, ticker)
    airtable_utils.remove_duplicate_records_clinical_trials("Clinical Trials")
    airtable_utils.remove_duplicate_records_force_clinical_trials("Clinical Trials")

def update_company_financials_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    for ticker in tickers:
        financials = get_company_data.get_financials(ticker)
        for index, row in financials.iterrows():
            for column in financials.columns.to_list():
                rec = {}
                rec["DATE"] = index
                rec["METRIC"] = column
                rec["VALUE"] = row[column]
                airtable_utils.add_record(config.at_base_key, "Company Financials", config.at_api_key, rec, ticker)
        
    airtable_utils.remove_duplciate_records_financial("Company Financials")

def update_relationships_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    for ticker in tickers:
        entities = get_relationships.get_relationships(ticker)
        for entity in entities:
            print(entity)

update_relationships_table()