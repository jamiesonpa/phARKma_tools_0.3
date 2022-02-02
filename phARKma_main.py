from os import name
from turtle import update
from anyio import current_effective_deadline
import rapidfuzz
from rapidfuzz import fuzz
import requests
import get_company_data
import get_linkedin_urls
import phARKma_utils
import get_relationships
import get_trials
import trial_updater
import airtable_utils
import get_clinical_collaborators
import get_arkg_tickers
import get_details
import config
import get_analyst_ratings
import sys
import logging
import alive_progress
from alive_progress import alive_bar
from itertools import groupby
from itertools import combinations
import get_drugs
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import linkedin_scraper
from unirank import Ranking
import get_model

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
        
    airtable_utils.remove_duplicate_records_financial("Company Financials")

def update_clinical_relationships_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    for ticker in tickers:
        print("getting clinical relationships for " + ticker)
        ctcollabs = get_clinical_collaborators.get_clinical_collaborators(ticker)
        print(ctcollabs)
        for dict in ctcollabs:
            print("adding clinical relationships for " + dict["NAME"])
            if rapidfuzz.fuzz.WRatio(dict["NAME"],dict["TARGET"]) < 90:
                airtable_utils.add_record(config.at_base_key, "Clinical Relationships", config.at_api_key, dict, ticker)

def get_total_database():
    db = pd.read_csv("trials_database.csv")
    records = []
    with open("all_biotech_tickers.txt") as readfile:
        tickers = readfile.read().split("\n")
    for ticker in tickers[22:]:
        try:
            name = get_details.get_details(ticker, False)["NAME"]
        except:
            name = ticker
        trials = get_trials.get_trials_primary(ticker,db)
        for trial in trials:
            new_record = {}
            if trial["COLLABORATORS"] != "not found":
                if trial["COLLABORATORS"].find(";") != -1:
                    collabs = trial["COLLABORATORS"].split(";")
                    for collab in collabs:
                        if len(collab) > 2:
                            new_record["TICKER"] = ticker
                            new_record["NAME"] = name
                            new_record["TARGET"] = collab
                else:
                    new_record["TICKER"] = ticker
                    new_record["NAME"] = name
                    new_record["TARGET"] = trial["COLLABORATORS"]
            
            if new_record != {}:
                with open("records.txt","a") as writefile:
                    print("adding record: " + str(new_record))
                    writefile.write(str(new_record) + "\n")

def update_relationships_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    for ticker in tickers:
        relationship_dicts = []
        entities = get_relationships.get_relationships(ticker)
        ctcollabs = get_clinical_collaborators.get_clinical_collaborators(ticker)
        for ctc in ctcollabs:
            entities.append(ctc["TARGET"])

        entities.sort()
        treshold = 85
        minGroupSize = 1
        paired = { c:{c} for c in entities }
        for a,b in combinations(entities,2):
            if fuzz.WRatio(a,b) < treshold: continue
            paired[a].add(b)
            paired[b].add(a)
        groups = []
        ungrouped = set(entities)
        while ungrouped:
            bestGroup = {}
            for city in ungrouped:
                g = paired[city] & ungrouped
                for c in g.copy():
                    g &= paired[c] 
                if len(g) > len(bestGroup):
                    bestGroup = g
            if len(bestGroup) < minGroupSize : break  # to terminate grouping early change minGroupSize to 3
            ungrouped -= bestGroup
            groups.append(bestGroup)


        for group in groups:
            smallest = "arkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkarkark"
            for item in group:
                if len(item) < len(smallest):
                    smallest = item
            
            relationship_dict = {}
            relationship_dict["TICKER"] = ticker
            relationship_dict["TARGET"] = smallest
            relationship_dict["TARGET GROUP"] = group
            relationship_dicts.append(relationship_dict)
        
        for dict in relationship_dicts:
            airtable_utils.add_record(config.at_base_key, "Relationships", config.at_api_key, dict, ticker)

def update_details_table():
    tickers = get_arkg_tickers.get_arkg_tickers()
    detail_list = []
    for ticker in tickers:
        details = get_details.get_details(ticker,False)
        detail_list.append((ticker,details))
    for detail in detail_list:
        airtable_utils.add_record(config.at_base_key, "Company Details",config.at_api_key, detail[1], detail[0])
    airtable_utils.remove_duplicate_records_details("Company Details")

def update_employees_table():
    linkedin_urls = get_linkedin_urls.get_linkedin_urls()
    with open("linkedin_urls.txt", "w+") as writefile:
        for url in linkedin_urls:
            print(url)
            writefile.write(url+"\n")

    scraper = linkedin_scraper.LinkedinEmployeesSchoolinfoDataScraper()

    unis = get_linkedin_urls.get_universities()
    education = pd.read_csv("employee_education.csv")
    companies = []
    lowest_rank = 0
    for uni in unis:
        if int(uni["rank"]) > lowest_rank:
            lowest_rank = int(uni["rank"])
    middle_rank = round((lowest_rank/2),0)
    print("lowest rank is " + str(lowest_rank))
    print("middle rank is " + str(middle_rank))

    for index,row in education.iterrows():
        companies.append(row["Company Name"])
    companies = list(set(companies))
    company_scores = []
    for company in companies:
        company_score = {}
        for index,row in education.iterrows():
            if row["Company Name"] == company:
                current_university = row["School Name"]
                current_employees = row["# Hired Employees"]
                uni_found = False
                rank = 0
                for uni in unis:
                    if uni["name"] == current_university:
                        rank = uni["rank"]
                        uni_found = True
                
                if uni_found == False:
                    for uni in unis:
                        if rapidfuzz.fuzz.WRatio(uni["name"],current_university) > 95:
                            rank = uni["rank"]
                            uni_found = True
                
                if uni_found == True:
                    company_score[rank] = current_employees
        company_scores.append((company, company_score))

    company_dicts = []
    for company in company_scores:
        company_name = company[0]
        company_scores = company[1]
        total_score = 0
        total_employees = 0
        for company_score in company_scores.keys():
            total_employees = int(company_score) + int(total_employees)
            total_score = total_score + (int(company_score) * int(company_scores[company_score]))
        company_dict = {}
        company_dict["name"] = company_name
        company_dict["total_employees"] = total_employees
        company_dict["total_score"] = total_score
        company_dicts.append(company_dict)

    for company_dict in company_dicts:
        company_dict["baseline_score"] = company_dict["total_employees"] * lowest_rank
        company_dict["difference_from_baseline"] = company_dict["baseline_score"] - company_dict["total_score"]
        company_dict["average_employee_educational_rank"] = lowest_rank - (company_dict["difference_from_baseline"]/company_dict["total_employees"])
        company_dict["normalized_average_employee_rank"] =round((1-(company_dict["average_employee_educational_rank"]/lowest_rank)) *100,2)
        name = company_dict["name"]
        cdeets = airtable_utils.get_airtable_records("Company Details")
        ticker = None
        name_found = False
        for entry in cdeets:
            if name_found == False:
                ename = entry["fields"]["NAME"]
                ticker = entry["fields"]["TICKER"]
                if rapidfuzz.fuzz.WRatio(name, ename) > 95:
                    print("found name similar to " + name + " in company details table which was " + ename + " and associated ticker was " + ticker)
                    name_found = True
            else:
                pass
        if ticker != None:
            edurecord = {}
            edurecord["TICKER"] = ticker
            edurecord["EDUCATION_SCORE"] = str(company_dict["normalized_average_employee_rank"])
            airtable_utils.add_record(config.at_base_key, "Employee Education Score", config.at_api_key, edurecord, ticker)
            
def update_models():
    tickers = get_arkg_tickers.get_arkg_tickers()
    data_dicts = {}
    for ticker in tickers:
        try:
            print("updating model for " + ticker)
            data_dict = {}
            price = get_model.get_price(ticker)[ticker]
            data_dict["CURRENT_PRICE"] = str(price)
            print("price = " + str(price))

            shares_outstanding = get_model.get_shares_outstanding(ticker)
            data_dict["CURRENT_ABSO"] = str(round(shares_outstanding[1],2))
            data_dict["AVERAGE_ABSO_DILUTION"] = str(round(shares_outstanding[0],2))
            print("current shares outstanding = " + str(shares_outstanding[1]))
            print("average shares outstanding annual dilution = " + str(shares_outstanding[0]))

            cash = get_model.get_cash(ticker)
            data_dict["CURRENT_CASH"] = cash
            print("cash = " + str(cash))

            average_opex = get_model.get_average_opex(ticker)
            data_dict["AVERAGE_OPEX"] = str(average_opex)
            print("average opex = " + str(average_opex))

            implied_runway = round((float(cash)/float(average_opex)),2)
            data_dict["IMPLIED_RUNWAY"] = str(implied_runway)
            print("implied cash runway = " + str(implied_runway) + " years")

            market_cap = float(price) * float(shares_outstanding[1])
            data_dict["MARKET_CAP"] = str(round(market_cap,2))
            print("market cap " + str(market_cap))

            total_debt = get_model.get_total_debt(ticker)
            data_dict["TOTAL_LIABILITIES"] = str(total_debt)
            print("total debt = " + str(total_debt))

            enterprise_value = float(market_cap) + float(total_debt) - float(cash)
            data_dict["ENTERPRISE_VALUE"] = str(round(enterprise_value,2))
            print("enterprise value = " + str(enterprise_value))

            airtable_utils.add_record(config.at_base_key,"Financial Model Statistics",config.at_api_key, data_dict, ticker)
        except:
            print("couldn't calculate model data for " + ticker)


update_employees_table()
update_models()