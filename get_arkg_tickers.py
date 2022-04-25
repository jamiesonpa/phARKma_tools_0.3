import requests
import alive_progress
from alive_progress import alive_bar
import shutil
import sys, logging
# import airtable_utils

def get_arkg_tickers():
    #this is the link that downloads the csv of the current ARKG holdings
    print("Retrieving ARKG ticker list...")
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
    arkg_holdings_csv = "https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv"
    arkg_holdings = str(requests.get(arkg_holdings_csv, headers=hdr).content).split("ARKG")
    arkg_holdings = arkg_holdings[1:len(arkg_holdings)-1]
    arkg_tickers = []
    with alive_bar(len(arkg_holdings)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for line in arkg_holdings:
            ticker = line.split(",")[2].replace('"',"")
            if ticker.find(" ") != -1:
                ticker = ticker.split(" ")[0]
            if ticker != "":
                arkg_tickers.append(ticker)
            bar()
        # print("retrieved...")
    
    # tickers_of_interest = airtable_utils.get_airtable_records("Tickers of Interest")
    # for toi in tickers_of_interest:
    #     ticker = toi["fields"]["TICKER"]
    #     if len(ticker) > 1:
    #         arkg_tickers.append(ticker)
    
    arkg_tickers = list(set(arkg_tickers))

    return arkg_tickers

def get_arkk_tickers():
    #this is the link that downloads the csv of the current ARKG holdings
    print("Retrieving ARKG ticker list...")
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
    arkg_holdings_csv = "https://ark-funds.com/wp-content/uploads/funds-etf-csv/ARK_GENOMIC_REVOLUTION_ETF_ARKG_HOLDINGS.csv"
    arkg_holdings = str(requests.get(arkg_holdings_csv, headers=hdr).content).split("ARKG")
    arkg_holdings = arkg_holdings[1:len(arkg_holdings)-1]
    arkg_tickers = []
    with alive_bar(len(arkg_holdings)) as bar:
        alive_handler = logging.StreamHandler(sys.stdout)
        for line in arkg_holdings:
            ticker = line.split(",")[2].replace('"',"")
            if ticker.find(" ") != -1:
                ticker = ticker.split(" ")[0]
            if ticker != "":
                arkg_tickers.append(ticker)
            bar()
        # print("retrieved...")
    
    # tickers_of_interest = airtable_utils.get_airtable_records("Tickers of Interest")
    # for toi in tickers_of_interest:
    #     ticker = toi["fields"]["TICKER"]
    #     if len(ticker) > 1:
    #         arkg_tickers.append(ticker)
    
    arkg_tickers = list(set(arkk_tickers))

    return arkk_tickers

