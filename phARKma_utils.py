import datetime
from datetime import datetime
import pandas as pd
import trial_updater
def removeDigits(s):
    answer = []
    for char in s:
        if not char.isdigit():
            answer.append(char)
    return ''.join(answer)


def timestamp():
    dateTimeObj = datetime.now()
    timestampStr = "[" + (dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")) + "]: "
    return timestampStr

def get_trials_database():
    print(timestamp() + "Fetching clinical trials csv database...")
    trial_database_found = False
    try:
        trials_database = pd.read_csv("trials_database.csv")
        trial_database_found = True
    except:
        trial_database_found = False
    if trial_database_found == True:
        return trials_database
    else:
        trial_updater.check_trial_deprecation_status(True)
        trials_database = pd.read_csv("trials_database.csv")
        return trials_database
