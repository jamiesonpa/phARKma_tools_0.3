import get_arkg_tickers
import airtable_utils
import datetime
import pandas as pd
import config
import requests
import json

#get the price of a ticker
def get_price(ticker):   
    #get the current market price of the company
    current_price = {}
    date = str(datetime.datetime.today()-datetime.timedelta(5)).split(" ")[0]
    # print(date)
    url = "https://api.polygon.io/v1/open-close/"+ticker+"/"+date+"?adjusted=true&apiKey="+config.polygon_api_key
    req = requests.get(url)
    reqjson = json.loads(req.content)
    current_price[ticker] = reqjson["close"]
    return current_price
#make a list of dicts that contain the shares outstanding for each company in a tuple with the
#ticker as the first entry
def get_shares_outstanding(ticker):
    ret_dict = {}
    shares_outstanding = {}
    financial_records = airtable_utils.get_airtable_records("Company Financials")
    for rec in financial_records:
        if (rec["fields"]["TICKER"]) == ticker:
            if rec["fields"]["METRIC"] == "commonStockSharesOutstanding":
                date_string = rec["fields"]["DATE"]
                year_string = date_string.split("-")[0]
                month_string = date_string.split("-")[1]
                day_string = date_string.split("-")[2]
                date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                shares_outstanding[date] = rec["fields"]["VALUE"]
                # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])

    shares_outstanding_keys_sorted = sorted(shares_outstanding)
    if len(shares_outstanding_keys_sorted) > 1:
        current_shares_outstanding = shares_outstanding[(shares_outstanding_keys_sorted)[-1]]
    else:
        current_shares_outstanding = shares_outstanding[(shares_outstanding_keys_sorted)[0]]
    
    shares_outstanding_change_sum = 0
    last_shares_outstanding = 0
    for key in shares_outstanding_keys_sorted:
        if last_shares_outstanding == 0:
            last_shares_outstanding = shares_outstanding[key]
        else:
            change = float(shares_outstanding[key]) - float(last_shares_outstanding)
            shares_outstanding_change_sum = float(shares_outstanding_change_sum) + float(change)
            last_shares_outstanding = shares_outstanding[key]

    shares_outstanding_change_average = shares_outstanding_change_sum/(len(shares_outstanding_keys_sorted))
    retval = (shares_outstanding_change_average, current_shares_outstanding)
    return retval

#make a list of dicts that contain the cash for each company in a tuple with the
#ticker as the first entry
def get_cash(ticker):
    ret_dict = {}
    cash_and_equivalents = {}
    financial_records = airtable_utils.get_airtable_records("Company Financials")
    for rec in financial_records:
        if (rec["fields"]["TICKER"]) == ticker:
            if rec["fields"]["METRIC"] == "cashAndCashEquivalentsAtCarryingValue":
                date_string = rec["fields"]["DATE"]
                year_string = date_string.split("-")[0]
                month_string = date_string.split("-")[1]
                day_string = date_string.split("-")[2]
                date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                cash_and_equivalents[date] = rec["fields"]["VALUE"]
                # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])
    
    cash_keys_sorted = sorted(cash_and_equivalents)
    try:
        current_cash = cash_and_equivalents[cash_keys_sorted[-1]]
        return current_cash
    except:
        return ("not found")

#make a list of dicts that contain the cash for each company in a tuple with the
#ticker as the first entry
def get_average_opex(ticker):
    try:
        opex_dict = {}
        financial_records = airtable_utils.get_airtable_records("Company Financials")
        for rec in financial_records:
            if (rec["fields"]["TICKER"]) == ticker:
                if rec["fields"]["METRIC"] == "operatingExpenses":
                    date_string = rec["fields"]["DATE"]
                    year_string = date_string.split("-")[0]
                    month_string = date_string.split("-")[1]
                    day_string = date_string.split("-")[2]
                    date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                    opex_dict[date] = rec["fields"]["VALUE"]
                    # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])


        #get average company opex
        opexs = []
        for entry in opex_dict.keys():
            opexs.append(opex_dict[entry])
        
        opex_sum = 0
        for opex in opexs:
            opex_sum = float(opex_sum) + float(opex)
        
        entry_number = len(opexs)
        opex_average = round(opex_sum/entry_number,2)
        return opex_average
    except:
        return ("not found")

def get_revenue(ticker):
    try:
        revenue_dict = {}
        financial_records = airtable_utils.get_airtable_records("Company Financials")
        for rec in financial_records:
            if (rec["fields"]["TICKER"]) == ticker:
                if rec["fields"]["METRIC"] == "totalRevenue":
                    date_string = rec["fields"]["DATE"]
                    year_string = date_string.split("-")[0]
                    month_string = date_string.split("-")[1]
                    day_string = date_string.split("-")[2]
                    date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                    revenue_dict[date] = rec["fields"]["VALUE"]
                    # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])


        #get average company opex
        revs = []
        for entry in revenue_dict.keys():
            revs.append(revenue_dict[entry])
        
        revenue_sum = 0
        for rev in revs:
            revenue_sum = float(revenue_sum) + float(rev)
        
        entry_number = len(revs)
        revenue_average = round(revenue_sum/entry_number,2)
        return revenue_average
    except:
        return ("not found")

def get_total_debt(ticker):
    debt_dict = {}
    financial_records = airtable_utils.get_airtable_records("Company Financials")
    for rec in financial_records:
        if (rec["fields"]["TICKER"]) == ticker:
            if rec["fields"]["METRIC"] == "totalLiabilities":
                date_string = rec["fields"]["DATE"]
                year_string = date_string.split("-")[0]
                month_string = date_string.split("-")[1]
                day_string = date_string.split("-")[2]
                date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                debt_dict[date] = rec["fields"]["VALUE"]
                # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])
    
    sorted_debt_dict_keys = sorted(debt_dict.keys())
    if len(sorted_debt_dict_keys) > 1:
        last_date = sorted_debt_dict_keys[-1]
    else:
        last_date = sorted_debt_dict_keys[0]
    
    current_total_debt = debt_dict[last_date]

    return current_total_debt

def get_net_income(ticker):
    try:
        revenue_dict = {}
        financial_records = airtable_utils.get_airtable_records("Company Financials")
        for rec in financial_records:
            if (rec["fields"]["TICKER"]) == ticker:
                if rec["fields"]["METRIC"] == "netIncome":
                    date_string = rec["fields"]["DATE"]
                    year_string = date_string.split("-")[0]
                    month_string = date_string.split("-")[1]
                    day_string = date_string.split("-")[2]
                    date = datetime.datetime(int(year_string),int(month_string),int(day_string))
                    revenue_dict[date] = rec["fields"]["VALUE"]
                    # print(ticker + " " + str(date) + ": " + rec["fields"]["VALUE"])


        #get average company opex
        revs = []
        for entry in revenue_dict.keys():
            revs.append(revenue_dict[entry])
        
        revenue_sum = 0
        for rev in revs:
            revenue_sum = float(revenue_sum) + float(rev)
        
        entry_number = len(revs)
        revenue_average = round(revenue_sum/entry_number,2)
        return revenue_average
    except:
        return ("not found")
    


with open("C:\\Users\\Pierce Jamieson\\Desktop\\python_projects\\phARKma_3\\phARKma_tools_0.2\\arkg_tickers.txt") as readfile:
    ticker_list = readfile.read().split("\n")

for ticker in ticker_list:
    cash = get_net_income(ticker)
    print(ticker + ", " + str(cash))