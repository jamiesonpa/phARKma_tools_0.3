
import requests
import pandas as pd 
from yahoo_fin import stock_info as si 
from pandas_datareader import DataReader
import numpy as np
import get_arkg_tickers
import datetime

recommendations = []

def get_rating_history(ticker, verbose):
    lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
    rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url =  lhs_url + ticker + rhs_url
    r = requests.get(url, headers=headers)
    if not r.ok:
        entries = []
    else:
        result = r.json()['quoteSummary']['result'][0]
        try:
            history = result['upgradeDowngradeHistory']["history"]
            entries = []
            for entry in history:
                entry_dict = {}
                entry_dict["TICKER"] = ticker.upper()
                entry_dict["DATE"] = str(datetime.datetime.fromtimestamp(int(entry["epochGradeDate"]))).split(" ")[0]
                entry_dict["FIRM"] = entry["firm"]
                if entry["action"] == "down":
                    entry_dict["ACTION"] = "DOWNGRADE"
                elif entry["action"] == "up":
                    entry_dict["ACTION"] = "UPGRADE"
                elif entry["action"] == "main":
                    entry_dict["ACTION"] = "MAINTAIN"
                elif entry["action"] == "init":
                    entry_dict["ACTION"] = "INITIATE"
                else:
                    entry_dict["ACTION"] = entry["action"]
                entry_dict["FROM"] = entry["fromGrade"]
                entry_dict["TO"] = entry["toGrade"]
                entries.append(entry_dict)
        except:
            pass
    df = pd.DataFrame(entries)
    if verbose:
        print(df)
    return df
        
def get_mean_analyst_rating(ticker, verbose):
    lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
    rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url =  lhs_url + ticker + rhs_url
    r = requests.get(url, headers=headers)
    if not r.ok:
        recommendation = "N/A"
    try:
        result = r.json()['quoteSummary']['result'][0]
        recommendation = result['financialData']['recommendationMean']['fmt']
        rec_key = result['financialData']['recommendationKey']
    except:
        recommendation = "N/A"
        rec_key = "N/A"
    retval = (str(recommendation), rec_key)
    if verbose:
        print("Mean rating: " + str(retval[0]) + "; Recommendation: " + rec_key)
    return retval
