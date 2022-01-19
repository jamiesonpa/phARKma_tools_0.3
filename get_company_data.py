import requests
import pandas as pd
from rapidfuzz import fuzz
from sec_api import FullTextSearchApi, XbrlApi
import datetime
import urllib
import nltk
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import time
import re
import os
import spacy
import get_details
import get_trials
from get_trials import get_trials_primary, get_trials_collaborator
import config

alphavantage_api_key = config.alphavantage_api_key
polygon_api_key = config.polygon_api_key
edgar_api_key = config.edgar_api_key


def get_fundamental_dataframe(json):
    df = pd.DataFrame(json['annualReports'])
    df.set_index('fiscalDateEnding', inplace=True)
    return df

def query_fundamental_data(func, symbol, outputsize='full', datatype='json', apikey=alphavantage_api_key):
    data = {
        "function": func,
        "symbol": symbol,
        "outputsize": outputsize, # (full) and (compact) are accepted
        "datatype": datatype,
        "apikey": apikey
    }
    return requests.get("https://www.alphavantage.co/query", data).json()

def query_timeseries_data(func, symbol, outputsize='full', datatype='json', apikey=alphavantage_api_key):
    data = {
        "function": func,
        "symbol": symbol,
        "outputsize": outputsize, # (full) and (compact) are accepted
        "datatype": datatype,
        "apikey": apikey
    }
    return requests.get("https://www.alphavantage.co/query", data).json()

def get_timeseries_dataframe(json, type):
    df = pd.DataFrame.from_dict(json[type], orient= 'index')
    df.index =  pd.to_datetime(df.index, format='%Y-%m-%d')
    
    df = df.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
    df = df.astype({'Open': 'float64', 'High': 'float64', 'Low': 'float64','Close': 'float64','Volume': 'float64',})
    df = df[[ 'Open', 'High', 'Low', 'Close', 'Volume']]
    return df

def get_price(ticker):
    response_json = query_timeseries_data("TIME_SERIES_DAILY", ticker)
    STOCKPRICE_DATA = get_timeseries_dataframe(response_json, "Time Series (Daily)")
    price = STOCKPRICE_DATA["Close"].to_list()[0]
    yesterdays_price = STOCKPRICE_DATA["Close"].to_list()[1]
    return (float(price), float(yesterdays_price))

def get_financials(ticker):
    df_columns = []
    response_json = query_fundamental_data("INCOME_STATEMENT", ticker)
    try:
        INCOME_DATA = get_fundamental_dataframe(response_json)
    except:
        pass
    cols = ["totalRevenue","costOfRevenue","costofGoodsAndServicesSold","ebitda","netIncome","researchAndDevelopment","operatingExpenses","sellingGeneralAndAdministrative","grossProfit"]
    for col in cols:
        try:
            df_columns.append(INCOME_DATA[col].astype(float))
        except:
            pass

    response_json = query_fundamental_data("BALANCE_SHEET", ticker)
    try:
        BALANCE_DATA = get_fundamental_dataframe(response_json)
    except:
        pass
    bd_cols = ["totalAssets","cashAndCashEquivalentsAtCarryingValue", "totalLiabilities","commonStockSharesOutstanding"]
    for col in bd_cols:
        try:
            df_columns.append(BALANCE_DATA[col].astype(float))
        except:
            pass
        
    response_json = query_fundamental_data("CASH_FLOW", ticker)
    CASHFLOW_DATA = get_fundamental_dataframe(response_json)
    try:
        df_columns.append(CASHFLOW_DATA["changeInCashAndCashEquivalents"].astype(float))
    except:
        pass

    financials_df = pd.DataFrame()
    counter = 0
    for column in df_columns:
        if counter == 0:
            financials_df = column
        else:
            financials_df = pd.merge(financials_df, column, right_index=True, left_index=True)
        counter +=1
    
    return financials_df


        

