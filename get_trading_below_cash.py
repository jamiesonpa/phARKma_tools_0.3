

import get_model
import get_company_data
import get_arkg_tickers


# tickers = get_arkg_tickers.get_arkg_tickers()
tickers = ["NTLA","EXAS","CRSP","VRTX","TDOC","IONS","BNR","FATE","BEAM","REGN","NVTA","CDNA","NVS","TWST","PFE","VCYT","SHE: 000710","SGFY","PSNL","VEEV","INCY","PATH","PACB","MASS","IOVA","CTVA","SLGC","CDXS","CERS","ONEM","ACCD","MCRB","QSI","SDGR","ARCT","ONT","EDIT","TXG","RXRX","DNA","BLI","CGEN","VERV","ONVO","CLLS","PLTR"]

cash_dict = {}
for ticker in tickers:
    try:
        financials = get_company_data.get_financials(ticker)
        cash = financials['cashAndCashEquivalentsAtCarryingValue'].to_list()
        cash_dict[ticker] = cash[0]
        print("ticker = " + ticker + ": cash = " + str(cash[0]))
    except:
        pass

price_dict = {}
for ticker in tickers:
    price = get_model.get_price(ticker)[ticker]
    price_dict[ticker] = price
    print(ticker + " has a price of " + str(price))

shares_dict = {}
for ticker in price_dict.keys():

    financials = get_company_data.get_financials(ticker)
    shares = financials['commonStockSharesOutstanding'].to_list()
    shares_dict[ticker] = shares[0]
    print("ticker = " + ticker + ": shares = " + str(shares[0]))


market_cap_dict = {}

for tick in shares_dict.keys():
    shares = shares_dict[tick]
    price = price_dict[tick]
    market_cap = shares * price
    market_cap_dict[tick] = market_cap
    print(tick + " has a market cap of " + str(market_cap))


for ticker in tickers:
    try:
        if float(market_cap_dict[ticker]) < float(cash_dict[ticker]):
            print(ticker + " is trading at less than cash.")
        else:
            print(ticker + " is not trading at less than cash")
    except:
        pass







