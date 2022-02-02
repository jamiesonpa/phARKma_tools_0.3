
import requests
import sec_api
from sec_api import QueryApi
import config
import json
from datetime import datetime



def get_details(ticker, verbose):
    try:
        print("Fetching company details for " + ticker)
        polygon_api_key = config.polygon_api_key
        url ="https://api.polygon.io/v3/reference/tickers/"+ticker+"?apiKey=" + polygon_api_key
        response = requests.get(url)
        response_dict = json.loads(response.content)
        mappings = [("TICKER","ticker"), ("NAME","name"),("LOCALE","locale"),("EXCHANGE","primary_exchange"),("CIK","cik"),("MARKET CAP","market_cap"),("PHONE NUMBER","phone_number"),("DESCRIPTION","description"),("SIC DESCRIPTION","sic_description"),("URL","homepage_url"),("EMPLOYEES","total_employees"),("LIST DATE","list_date")]
        detail_dict = {}
        for key in response_dict["results"].keys():
            for mapping in mappings:
                if mapping[1] == key:
                    if key == "name":
                        name = response_dict["results"][key]
                        if name.find("Class") != -1:
                            newname = name.split("Class")[0].strip()
                            detail_dict["NAME"] = newname
                        elif name.find("Common") != -1:
                            newname = name.split("Common")[0].strip()
                            detail_dict["NAME"] = newname                  
                        else:
                            detail_dict["NAME"] = name
                    else:
                        detail_dict[mapping[0]] = response_dict["results"][key]
        
        return detail_dict
    except:
        print("Couldn't fetch details for " + ticker + " from polygon API")
        return None