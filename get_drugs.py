import requests
from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import io
import os
import xlwt
import openpyxl
import config
import json
from get_details import get_details
from phARKma_utils import timestamp
import rapidfuzz
import airtable_utils
import get_arkg_tickers
import phARKma_utils
import get_condition_category

def get_drugs_dot_com():
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
    url = "https://www.drugs.com/pharmaceutical-companies.html"
    req = requests.get(url, headers = hdr)
    soup = BeautifulSoup(req.content, 'html.parser')
    links = []
    for div in soup.find_all("div", {"class": "ddc-clearfix"}):
        subdivs =[]
        for subdiv in div.find_all("div"):
            subdivs.append(subdiv)

        a_elements = []
        for subdiv in subdivs:
            for aelement in subdiv.find_all("a"):
                a_elements.append(aelement)

        for aele in a_elements:
            if str(aele).find("href") != -1:
                aele_split = str(aele).split('href="')[1].split('">')[0]
                link = "https://www.drugs.com" + aele_split
                if link.find('"') == -1:
                    links.append(link)
        
    drugs = []
    for link in links:
        print(link)
        if link.find("privacy") == -1:
            req = requests.get(link, headers = hdr)
            soup = BeautifulSoup(req.content, "html.parser")
            print("trying " + link + "!")
            try:
                headers = soup.find_all("h2", {"id":"associated-drugs"})[0]
                ompany_name = headers.text.split("with ")[1]
            except:
                company_name = link.split("manufacturer/")[1].split(".html")[0]
                company_name_split = company_name.split("-")
                company_name_split.remove(company_name_split[-1])
                new_company_name = ""
                for frag in company_name_split:
                    new_company_name = new_company_name + frag.capitalize() + " "
                
                company_name = new_company_name.strip()
                


            if len(soup.find_all("table",{"class":"data-list"})) > 1:
                dtable = soup.find_all("table",{"class":"data-list"})[0]
                trs = []
                for tbody in dtable.find_all("tbody"):
                    for tr in tbody.find_all("tr"):
                        trs.append(tr)

                for tr in trs:
                    new_drug = {}
                    if len(tr.find_all("td")) > 0:
                        td_of_interest = tr.find_all("td")[0]
                        try:
                            name = td_of_interest.find_all("a")[0].text
                        except:
                            name = "not found"
                        new_drug["COMPANY"] = company_name
                        new_drug["NAME"] = name
                        try:
                            generic_name = td_of_interest.find_all("a")[1].text
                        except:
                            generic_name = "not found"
                        new_drug["GENERIC NAME"] = generic_name
                        try:
                            drugclass = str(td_of_interest).split("class:</b>")[1].split("</td>")[0]
                        except:
                            drugclass = "not found"
                        new_drug["DRUG CLASS"] = drugclass.replace('"',"").strip()
                        drugs.append(new_drug)


    df = pd.DataFrame(drugs)
    df.to_csv("drugs_database.csv")


def get_ticker_from_name(name):
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    # print(timestamp() + "attempting to get ticker from name " + name)
    polygon_api_key = config.polygon_api_key
    request_url = "https://api.polygon.io/v3/reference/tickers?search="+name+"&active=true&sort=ticker&order=asc&limit=10&apiKey="+polygon_api_key
    req = requests.get(request_url, headers = hdr)
    reqjson = json.loads(req.content)
    result_names = []
    for result in reqjson["results"]:
        result_names.append(result["name"])
    
    best_match = ""
    highest_score = 0
    for resname in result_names:
        similarity = rapidfuzz.fuzz.WRatio(name, resname)

        if similarity > highest_score:
            best_match = resname
            highest_score = similarity
    ticker = "not found"
    if highest_score >= 85:
        for result in reqjson["results"]:
            if result["name"] == best_match:
                ticker = result["ticker"]

    return ticker


def get_all_drugs():
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    drug_db = "https://www.accessdata.fda.gov/cder/ndcxls.zip"
    r = requests.get(drug_db)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(os.getcwd())

    df = pd.read_table('product.xls',encoding='cp1252')
    drop_cols = ["PRODUCTID","PROPRIETARYNAMESUFFIX","APPLICATIONNUMBER","DEASCHEDULE","NDC_EXCLUDE_FLAG"]
    for column in drop_cols:
        del df[column]
    dates = df["STARTMARKETINGDATE"].to_list()
    new_date_list = []
    for date in dates:
        if date != "":
            year = str(date)[0:4]
            month = str(date)[4:6]
            day = str(date)[6:8]
            new_date_list.append(year + "-"+month+"-"+day)
        else:
            new_date_list.append(date)
    del df["STARTMARKETINGDATE"]
    df["STARTMARKETINGDATE"] = new_date_list


    dates = df["ENDMARKETINGDATE"].to_list()
    new_date_list = []
    for date in dates:
        if date != "":
            year = str(date)[0:4]
            month = str(date)[4:6]
            day = str(date)[6:8]
            new_date_list.append(year + "-"+month+"-"+day)
        else:
            new_date_list.append(date)
    del df["ENDMARKETINGDATE"]
    df["ENDMARKETINGDATE"] = new_date_list


    dates = df["LISTING_RECORD_CERTIFIED_THROUGH"].to_list()
    new_date_list = []
    for date in dates:
        if date != "":
            year = str(date)[0:4]
            month = str(date)[4:6]
            day = str(date)[6:8]
            new_date_list.append(year + "-"+month+"-"+day)
        else:
            new_date_list.append(date)
    del df["LISTING_RECORD_CERTIFIED_THROUGH"]
    df["LISTING_RECORD_CERTIFIED_THROUGH"] = new_date_list

    doses = df["DOSAGEFORMNAME"].to_list()
    doseformlist = []
    for dose in doses:
        dose = dose.replace('"',"")
        doseformlist.append(dose)
    del df["DOSAGEFORMNAME"]
    df["DOSAGEFORMNAME"] = doseformlist

    doses = df["DOSAGEFORMNAME"].to_list()
    doseformlist = []
    for dose in doses:
        dose = dose.replace('"',"")
        doseformlist.append(dose)
    del df["DOSAGEFORMNAME"]
    df["DOSAGEFORMNAME"] = doseformlist

    classes = df["PHARM_CLASSES"].to_list()
    classlist = []
    for cls in classes:
        cls = str(cls).replace('"',"")
        classlist.append(cls)
    del df["PHARM_CLASSES"]
    df["PHARM_CLASSES"] = classlist

    df = df.rename(columns={"LABELERNAME":"LABELER","MARKETINGCATEGORYNAME":"APPLICATION_TYPE", "PRODUCTTYPENAME": "PRODUCT_TYPE", "NONPROPRIETARYNAME": "GENERIC_NAME", "PROPRIETARYNAME": "BRAND_NAME", "DOSAGEFORMNAME": "DOSAGE_FORM", "ROUTENAME": "ROUTE", "STARTMARKETINGDATE": "START_MARKETING_DATE", "ENDMARKETINGDATE": "END_MARKETING_DATE", "SUBSTANCENAME": "SUBSTANCE_NAME", "ACTIVE_NUMERATOR_STRENGTH": "DOSE_QUANTITY","ACTIVE_INGRED_UNIT":"DOSE_UNITS","PHARM_CLASSES":"PHARMACEUTICAL_CLASS"})


    relevant_drugs = []
    dfdict = df.to_dict("records")
    tickers = get_arkg_tickers.get_arkg_tickers()
    for ticker in tickers:
        name = phARKma_utils.process_name((get_details(ticker,False)["NAME"]))
        for row in dfdict:
            labeler = row["LABELER"]
            if labeler.find("a sub") != -1:
                labeler = labeler.split("a subsidiary")[1]
            if labeler.lower().find("subsidiary") != -1:
                labeler = labeler.split("ubsidiary")[1]
            if len(labeler.split(" ")) > 5:
                labeler = labeler.split(" ")[0]
            
            if phARKma_utils.process_name(labeler).find("div") != -1:
                if phARKma_utils.process_name(labeler).find(name) != -1:
                    relevant_drugs.append((row,ticker))
                    print("found sufficient similarity between " + name +" and " + labeler)
            else:
                similarity = rapidfuzz.fuzz.WRatio(name, phARKma_utils.process_name(labeler))
                if similarity >= 95:
                    row["TICKER"] = ticker
                    relevant_drugs.append((row,ticker))
                    print("found sufficient similarity between " + name +" and " + labeler)
    

    for drug in relevant_drugs:
        drug_generic_name = drug[0]["PRODUCTNDC"]
        drug_generic_name = drug_generic_name.replace(" ","-")
        search_url = "https://api.fda.gov/drug/label.json?search=openfda.product_ndc.exact:"+drug_generic_name+"&limit=1"
        req = requests.get(search_url, headers = hdr)
        reqjson = json.loads(req.content)
        drug[0]["PRIMARY_DISEASE_CATEGORY"]= "not found"
        drug[0]["SECONDARY_DISEASE_CATEGORY"]= "not found"
        try:
            indication = reqjson["results"][0]["indications_and_usage"][0].replace("INDICATIONS AND USAGE","")
            drug[0]["INDICATION"] = indication
            
        except:
            indication = "not found"
            drug[0]["INDICATION"] = indication
        try:
            category = get_condition_category.get_condition_category(indication)
            drug[0]["PRIMARY_DISEASE_CATEGORY"]= category[0]
            drug[0]["SECONDARY_DISEASE_CATEGORY"]= category[1]
        except:
            if drug[0]["PRIMARY_DISEASE_CATEGORY"] == "not found":
                drug[0]["PRIMARY_DISEASE_CATEGORY"]= "not found"
                drug[0]["SECONDARY_DISEASE_CATEGORY"]= "not found"
            else:
                drug[0]["SECONDARY_DISEASE_CATEGORY"]= "not found"
        airtable_utils.add_record(config.at_base_key, "Drugs", config.at_api_key, drug[0],drug[1])
