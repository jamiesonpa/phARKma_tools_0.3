import airtable_utils
from get_details import get_details
from get_trials import get_trials_primary


def get_clinical_collaborators_offline(ticker, db):
    name = get_details(ticker, False)["NAME"]
    get_trials_primary(ticker, db)

def get_clinical_collaborators(ticker):
    name = get_details(ticker, False)["NAME"]
    clinical_trials = airtable_utils.get_airtable_records("Clinical Trials")
    ct_collabs = []
    for trial in clinical_trials:
        if trial["fields"]["TICKER"] == ticker:
            if trial["fields"]["COLLABORATORS"] != "not found":
                if trial["fields"]["COLLABORATORS"].find(";") != -1:
                    collaborators = trial["fields"]["COLLABORATORS"].split(";")
                    for collab in collaborators:
                        if len(collab) > 2:
                            ct_collabs.append(collab)
                else:
                    collaborators = trial["fields"]["COLLABORATORS"]
                    collaborators = collaborators.replace(";","")
                    if len(collaborators) > 2:
                        ct_collabs.append(collaborators)
    
    relationship_dicts = []
    for collab in ct_collabs:
        relationship_dict = {}
        relationship_dict["TICKER"] = ticker
        relationship_dict["TARGET"] = collab
        relationship_dict["NAME"] = name
        relationship_dicts.append(relationship_dict)

    return relationship_dicts
