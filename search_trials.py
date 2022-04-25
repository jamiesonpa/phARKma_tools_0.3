import pandas as pd


def pull_trial(id):
    trials_db = pd.read_csv("phARKma_tools_0.2/auxillary_data/trials_database.csv")

    results = []
    for index, row in trials_db.iterrows():
        if row["ID"].find(id) != -1:
            results.append(row)
    for res in results:
        print("ID: "+ res["ID"])
        print("SUMMARY: " + res["SUMMARY"])
        print("DESCRIPTION: " +res["DESCRIPTION"])
        print("AGENCY: " + res["AGENCY"])


def search_trials(term):
    trials_db = pd.read_csv("phARKma_tools_0.2/auxillary_data/trials_database.csv")
    keep_cols = ["ORGANIZER STUDY ID", "SUMMARY", "DESCRIPTION","TITLE","OFFICIAL TITLE"]
    for column in trials_db.columns:
        kcol_found = False
        for kcol in keep_cols:
            if column == kcol:
                kcol_found = True
        if kcol_found == False:
            if column == "ID":
                pass
            else:

                trials_db = trials_db.drop(columns= [column])

    results = []
    columns = trials_db.columns
    for index, row in trials_db.iterrows():
        string = ""
        for col in columns:
            string = string + " " + row[col]
        
        if string.find(term) != -1:
            results.append(row["ID"])
    
    for res in results:
        print(res)



modality = input("To search trials for a search term type 's', to pull a specific trial's data, type 'id': ")
if modality == "s":
    search_term = input("specify search term: ")
    search_trials(search_term)

if modality == "id":
    id = input("specify trial id: ")
    pull_trial(id)
