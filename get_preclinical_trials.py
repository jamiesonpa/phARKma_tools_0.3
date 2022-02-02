
import airtable_utils


def get_preclinical_trials(ticker):
    pc_records = airtable_utils.get_airtable_records("Preclinical Trials")
    pc_trial_records = []
    for record in pc_records:
        if record["fields"]["TICKER"] == ticker:
            pc_trial_records.append(record["fields"])
    
    return pc_trial_records

