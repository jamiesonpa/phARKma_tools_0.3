import os
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import get_details
from get_details import get_details
from rapidfuzz import fuzz

def fetch_commercialized_drug_database():
    file_found = False
    for file in os.listdir():
        if str(file) == "commercialized_drug_list.txt":
            file_found = True
    if file_found == True:
        os.remove("commercialized_drug_list.txt")

    date_stamp = str(datetime.datetime.now()).split(".")[0] + "__DATE__"
    link_part1 = "https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process&rptName=2&reportSelectMonth="
    link_part2 = "&reportSelectYear="
    link_part3 = "&nav"
    current_year =int(datetime.datetime.now().year)
    next_year = current_year + 1
    year = current_year - 25
    month = 1
    links = []
    while year < next_year:
        if month < 13:
            # print("adding link for month " + str(month) + " and year " + str(year))
            newlink = link_part1 + str(month) + link_part2 + str(year) + link_part3
            links.append((newlink, year))
            month += 1
        else:
            month = 1
            year +=1
            if year < next_year:
                # print("adding link for month " + str(month) + " and year " + str(year))
                newlink = link_part1 + str(month) + link_part2 + str(year) + link_part3
                links.append((newlink, year))
                month += 1

    year = current_year - 25
    nmes = {}
    drug_dict = {}
    while year < next_year:
        nmes[year] = []
        year +=1

    for linktuple in links:
        # print(str(linktuple))
        link = linktuple[0]
        year = linktuple[1]
        req = requests.get(link)
        soup = BeautifulSoup(req.content,"html.parser")
        for table in soup.find_all("table"):
            for tbody in table.find_all("tbody"):
                for tr in tbody.find_all("tr"):
                    if tr.text.find("New Molecular Entity") != -1:
                        try:
                            text = tr.text.split("\n")
                            date = str(text[1])
                            drug = text[3]
                            priority = text[5]
                            company = text[6]
                            nmes[year].append(tr.text)
                            drug_dict[drug] = [("date", date),("company",company), ("priority",priority)]
                        except:
                            pass



    numbers = []
    for year in nmes.keys():
        numbers.append((year, str(len(nmes[year]))))

    with open("commercialized_drug_list.txt", "a") as writefile:
        writefile.write(date_stamp+"\n")

    for drug in drug_dict.keys():
        date = drug_dict[drug][0][1]
        company = drug_dict[drug][1][1]
        priority = drug_dict[drug][2][1]
        with open("commercialized_drug_list.txt", "a") as writefile:
            writefile.write(drug + "\t" + date +"\t" + company + "\t"+priority+"\n")
    


def get_commercialized_drugs(ticker):
    current_date_string = str(datetime.datetime.now()).split(".")[0]
    current_date_dtobject = datetime.datetime.strptime(current_date_string, "%Y-%m-%d %H:%M:%S")

    file_found = False
    for file in os.listdir():
        if str(file) == "commercialized_drug_list.txt":
            file_found = True
    
    if file_found == False:
        fetch_commercialized_drug_database()
    else:
        with open("commercialized_drug_list.txt") as readfile:
            cdl_file = readfile.read()
            datestamp_string = cdl_file.split("__DATE__")[0]
            datestamp_dtobject = datetime.datetime.strptime(datestamp_string, "%Y-%m-%d %H:%M:%S")
            difference = current_date_dtobject - datestamp_dtobject
            if int((difference.seconds/86400)) > 5:
                print("commercialized drugs database deprecated, updating...")
                fetch_commercialized_drug_database()
    
    name_fetched = False


    with open("commercialized_drug_list.txt") as readfile:
        cdl = readfile.read().split("__DATE__")[1]
        cdl_lines = cdl.split("\n")
        drugs = {}
        for line in cdl_lines:
            split_line = line.split("\t")
            if len(split_line) > 1:
                drugs[split_line[0]] = [split_line[2], split_line[1], split_line[3]] #company, date, status
    try:
        name = get_details(ticker)["NAME"]
        name_fetched = True
    except:
        pass

    fetched_drugs = {}
    if name_fetched == True:
        first_part_of_name = name.split(" ")[0]
        for key in drugs.keys():
            company = drugs[key][0].lower()
            ratio = fuzz.ratio(first_part_of_name.lower(), company)
            if ratio > 90:
                # print("Found drug commercialized by " +first_part_of_name + ": " + key + " -- " + str(drugs[key][1]) +", " + str(drugs[key][2]) + ". (ratio = " + str(ratio) + ")")
                fetched_drugs[key] = [str(drugs[key][1]), str(drugs[key][2])]
    
    df = pd.DataFrame.from_dict(fetched_drugs, orient='index')
    return df