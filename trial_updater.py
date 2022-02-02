from bs4 import BeautifulSoup
import datetime
import os
import re
import csv
import urllib
from tqdm import tqdm
import requests
import zipfile
import os
import alive_progress
from alive_progress import alive_bar
import shutil
import pandas as pd
import threading
import phARKma_utils


#abstracted methods

def download_trial_data():
    #check to see if a database of trials currently exists in the local directory, and if so, delete it.
    trial_database_link = "https://clinicaltrials.gov/AllPublicXML.zip" #download from this file and extract it using python
    print(phARKma_utils.timestamp() + "Retrieving clinical trials raw data...")
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}
    
    url = trial_database_link#big file test
    # Streaming, so we can iterate over the response.
    r = requests.get(url, headers = hdr, stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open('AllPublicXML.zip', 'wb') as file:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(phARKma_utils.timestamp() + "ERROR, something went wrong")
    print ("Clinical trials raw data retrieved...")
    print ("Unzipping clinical trials archive. This may take five minutes or so...")
    with zipfile.ZipFile("AllPublicXML.zip") as zip_ref:
        zip_ref.extractall(os.path.abspath(os.getcwd())+"/AllPublicXML")

def delete_clinical_trials_data():
    dir_path = "/Users/piercejamieson/Desktop/Scripts/12_9_2021/AllPublicXML2"
    print(phARKma_utils.timestamp() + "deleting" + dir_path)
    print(phARKma_utils.timestamp() + "this should take about 30s...")
    shutil.rmtree(dir_path)

def record_time():
    with open("auxillary_data/trial_data_fetch_time.txt","w+") as writefile:
        writefile.write(str(datetime.datetime.now().isoformat(timespec='minutes')))

def check_last_fetch_time():
    right_now = str(datetime.datetime.now().isoformat(timespec='minutes'))
    current_year = right_now.split("-")[0]
    current_month = right_now.split("-")[1]
    current_day = right_now.split("-")[2].split("T")[0]

    
    with open("auxillary_data/trial_data_fetch_time.txt") as readfile:
        last_fetch = readfile.read()
        lf_year = last_fetch.split("-")[0]
        lf_month = last_fetch.split("-")[1]
        lf_day = last_fetch.split("-")[2].split("T")[0]
        lf_date = datetime.datetime(year=int(lf_year), month = int(lf_month), day = int(lf_day))
        current_date = datetime.datetime(year=int(current_year), month = int(current_month), day = int(current_day))

    time_between = current_date - lf_date
    print(phARKma_utils.timestamp() + "It has been " + str(time_between) + " since last fetched clinical trials data...")
    if str(time_between).find(" ") != -1:
        retval = int(str(time_between).split(" ")[0])
    else:
        retval = 0
    return retval

def process_trial(file, study_data, trials):
    # print(phARKma_utils.timestamp() + "Fetching file " + str(file) + "/" + str(len(files)))
    with open(file, 'r', encoding="utf8") as readfile:
        data = readfile.read()
    soup = BeautifulSoup(data, "xml")
    study_type = soup.find("study_type").text
    if study_type == "Interventional":
        try:
            intervention_type = soup.find("intervention_type").text
        except:
            intervention_type = "not found"
        if intervention_type != "":
            agency_class = soup.find("agency_class").text
            if agency_class != "":
                nct_id = file.split("/")[-1].split(".")[0]
                title = soup.find('brief_title').text
                try:
                    official_title = soup.find("official_title").text
                    study_data["OFFICIAL_TITLE"] = official_title
                except:
                    study_data["OFFICIAL_TITLE"] = title

                try:
                    org_study_id = soup.find("org_study_id").text
                    study_data["ORGANIZER_STUDY_ID"] = org_study_id
                except:
                    study_data["ORGANIZER_STUDY_ID"] = "not found"


                study_data["id"] = nct_id
                study_data["title"] = title
                study_data["intervention_type"] = intervention_type

                try:
                    overall_status = soup.find("overall_status").text
                    study_data["status"] = overall_status
                except:
                    study_data["status"] = "not found"

                if overall_status.find("Terminate") != -1:
                    try:
                        stoppage = soup.find("why_stopped").text.strip("\r").strip('\n').replace(",","").replace("\n","").replace("\r","").strip()
                        study_data["why_stop"] = stoppage
                    except:
                        study_data["why_stop"] = "not found"
                elif overall_status.find("Withdraw") != -1:
                    try:
                        stoppage = soup.find("why_stopped").text.strip("\r").strip('\n').replace(",","").replace("\n","").replace("\r","").strip()
                        study_data["why_stop"] = stoppage
                    except:
                        study_data["why_stop"] = "not found"
                else:
                    study_data["why_stop"] = "not_found"

                summary_container = soup.find("brief_summary")
                try:
                    summary_text = summary_container.find("textblock").text
                    study_data["summary"] = summary_text.replace("\r","").replace("&#xA;","").replace("&#xD;","").replace(","," ").replace("\n","").strip().replace("\t","").strip().replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")

                except:
                    study_data["summary"] = "not found"

                description_container = soup.find("detailed_description")
                try:
                    description_text = description_container.find("textblock").text
                    study_data["description"] = description_text.replace("\r","").replace("&#xA;","").replace("&#xD;","").replace(","," ").replace("\n","").strip().replace("\t","").strip().replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
                    
                except:
                    study_data["description"] = "not found"
                
                phasetag = soup.find("phase")
                try:
                    phase = phasetag.text
                    if phase == "N/A":
                        study_data["phase"] = "not found"
                    else:
                        study_data["phase"] = phase
                except:
                    study_data["phase"] = "not found"

                try:
                    enrollment = soup.find("enrollment").text
                except:
                    enrollment = "not found"
                
                study_data["enrollment"] = enrollment
                    
                ivmodel = soup.find("intervention_model")
                try:
                    intervention_model = ivmodel.text
                    study_data["intervention_model"] = str(intervention_model)
                except:
                    study_data["intervention_model"] = "not found"

                masking_tag = soup.find("masking")
                try:
                    masking = masking_tag.text
                    study_data["masking"] = masking
                except:
                    study_data["masking"] = "not found"

                try:
                    allocation = soup.find("allocation").text
                    study_data["allocation"] = allocation
                except:
                    study_data["allocation"] = "not found"
                
                purpose_tag = soup.find("primary_purpose")
                try:
                    purpose = purpose_tag.text
                    study_data["purpose"] = purpose
                except:
                    study_data["purpose"] = "not found"
                
                condition_tag = soup.find("condition")
                try:
                    condition = condition_tag.text
                    study_data["condition"] = condition.strip("\n").strip("\r").replace(",", "")
                except:
                    study_data["condition"] = "not found"

                try:
                    drug = soup.find("intervention_name").text
                    study_data["drug"] = drug
                except:
                    study_data["drug"] = "not found"

                try:
                    gender = soup.find("gender").text
                    if gender == "All":
                        study_data["gender"] = "not found"
                    else:
                        if gender == "N/A":
                            study_data["gender"] = "not found"
                        else:
                            study_data["gender"] = gender
                except:
                    study_data["gender"] = "not found"

                try:
                    min_age = soup.find("minimum_age").text
                    if min_age == "N/A":
                        min_age = "0"
                    else:
                        min_age = min_age.split(" ")[0]

                    if min_age.find("Years") != -1:
                        min_age = min_age.split(" ")[0]
                    elif min_age.find("Month") != -1:
                        min_age = str(float(min_age.split(" ")[0]/12))

                    study_data["min_age"] = min_age
                except:
                    study_data["min_age"] = "not found"

                try:
                    max_age = soup.find("maximum_age").text
                    if max_age == "N/A":
                        max_age = "120"
                    else:
                        max_age = max_age.split(" ")[0]
                    
                    if max_age.find("Years") != -1:
                        max_age = max_age.split(" ")[0]
                    elif max_age.find("Month") != -1:
                        max_age = str(float(max_age.split(" ")[0]/12))
                    study_data["max_age"] = max_age
                except:
                    study_data["min_age"] = "not found"

                try:
                    city = soup.find("city").text
                    study_data["city"] = city
                except:
                    study_data["city"] = "not found"

                try:
                    state = soup.find("state").text
                    study_data["state"] = state
                except:
                    study_data["state"] = "not found"

                try:
                    country = soup.find("country").text
                    study_data["country"] = country
                except:
                    study_data["country"] = "not found"

                #NEW TIMEDATA CLEANING
                months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

                try:
                    study_first_submitted = soup.find("study_first_submitted").text
                except:
                    study_first_submitted = None
                try:
                    study_first_posted = soup.find("study_first_posted").text
                except:
                    study_first_posted = None
                try:
                    completion_date = soup.find("completion_date").text
                except:
                    completion_date = None
                try:
                    primary_completion_date = soup.find("primary_completion_date").text
                except:
                    primary_completion_date = None
                try:
                    last_sub_date = soup.find("last_update_submitted").text
                except:
                    last_sub_date = None
                
                dates = [(study_first_submitted, "STUDY FIRST SUBMITTED"), (study_first_posted, "STUDY FIRST POSTED"), (completion_date,"COMPLETION DATE"), (primary_completion_date, "PRIMARY COMPLETION DATE"), (last_sub_date, "LAST UPDATE SUBMITTED")]

                clean_dates = []
                for date in dates:
                    mcounter = 1
                    #first check to see if the date is a none value
                    if date[0] != None:
                        #if it isnt, check to see if it has a comma or not
                        comma_found = False
                        month_found = False
                        if date[0].find(",") != -1:
                            comma_found = True

                        #now check to see if it has a month in it or not
                        mcounter = 1
                        for month in months:
                            if date[0].find(month) != -1:
                                month_found = True
                                month_num = str(mcounter)
                            mcounter += 1
                        #if it doesn't have a month in it, just pretend its in January
                        if month_found == False:
                            month_num = "1"
                        
                        #if it has a comma in it
                        if comma_found == True:
                            #grab the day and the year
                            day = date[0].split(",")[0].split(" ")[1]
                            year = date[0].split(",")[1].strip()
                        #if there is no comma in it
                        else:
                            #check to see if it is a M D Y rather than a M D, Y format
                            if date[0].find(" ") == 2:
                                day = date[0].split(" ")[1]
                                year = date[0].split(" ")[2]
                            #if its not M D Y it should be just M Y format, so assign it 1 for the first day of the month
                            else:
                                day = "1"
                                year = date[0].split(" ")[1]
                        #now add it to the clean dates list with the key value for it
                        clean_dates.append((date[1], [int(day.strip()),int(month_num.strip()),int(year.strip())]))
                    else:
                        clean_dates.append((date[1], [None,None,None]))
                
                for date in clean_dates:
                    if date[1] != [None, None, None]:
                        clean_datetime = str(datetime.datetime(int(date[1][2]), int(date[1][1]), int(date[1][0])))
                        study_data[date[0]] = clean_datetime
                    else:
                        study_data[date[0]] = str(None)
                #END TIMEDATA CLEANING

                try:
                    exp_access = soup.find("has_expanded_access").text
                    study_data["expanded_access"] = exp_access
                except:
                    study_data["expanded_access"] = "not found"        

                try:
                    link = soup.find("url").text
                    study_data["url"] = link
                except:
                    study_data["url"] = "not found"             
                
                try:
                    agency = soup.find("agency").text
                    study_data["agency"] = agency
                except:
                    study_data["agency"] = "not found"

                try:
                    sponsor_container = soup.find("sponsors")
                    collaborators =  sponsor_container.find_all("collaborator")
                    collabors = []
                    for collab in collaborators:
                        try:
                            collab_agency = collab.find("agency").text
                            collabors.append(collab_agency)
                        except:
                            pass

                    if len(collabors) == 0:
                        collaborator_string = "not found"
                    else:
                        collaborator_string = ""
                        for cb in collabors:
                            collaborator_string = collaborator_string + cb + ";"
                    study_data["collaborators"] = collaborator_string
                except:
                    study_data["collaborators"] = "not found"


                try:
                    agency_class = soup.find("agency_class").text
                    study_data["agency_class"] = agency_class
                except:
                    study_data["agency_class"] = "not found"    

                #check to see whether this trial has results.
                try:
                    clinical_results = soup.find("clinical_results")
                except:
                    clinical_results = None
                
                #create an entry in the dict indicating that this trial has results.
                if clinical_results != None:
                    study_data["has results"] = True
                    # get_clinical_results(soup, study_data)
                else:
                    study_data["has results"] = False
                    # study_data["participant_flow"] = "not found"
                    # study_data["reported_events"] = "not found"
                    # study_data["baseline"] = "not found"
                    # study_data["outcome_list"] = "not found"

                # for key in study_data.keys():
                #     if key == "description":
                #         print(phARKma_utils.timestamp() + key + ": " + study_data[key][0:50].strip("\n") + "...")
                #     elif key == "summary":
                #         print(phARKma_utils.timestamp() + key + ": " + study_data[key][0:50].strip("\n") + "...")
                #     else:
                #         print(phARKma_utils.timestamp() + key + ": " + str(study_data[key]))
                trials.append(study_data)
    
def get_clinical_results(soup, study_data): #not currently implemented
    try:
        p_flow = soup.find("participant_flow")
        study_data["participant_flow"] = str(p_flow).replace("\n","").replace(",","")
    except:
        study_data["participant_flow"] = "not found"
    try:
        baseline = soup.find("baseline")
        study_data["baseline"] = str(baseline).replace("\n","").replace(",","")
    except:
        study_data["baseline"] = "not found"
    try:
        outcomes = soup.find("outcome_list")
        study_data["outcome_list"] = str(outcomes).replace("\n","").replace(",","")
    except:
        study_data["outcome_list"] = "not found"
    try:
        events = soup.find("reported_events")
        study_data["reported_events"] = str(events).replace("\n","").replace(",","")
    except:
        study_data["reported_events"] = "not found"

def check_trial_deprecation_status(download):
    #this is where execution begins
    print(phARKma_utils.timestamp() + "Initializing clinical trial data parse protocol...")
    trials = []
    directories = []
    files = []
    trial_ids = []
    trial_data_recent = False
    trial_data_present = False
    new_data_downloaded = False
    last_fetch = 0

    #first check to see if there is a clinical trial data directory in current directory
    if str(os.listdir()).find("AllPublicXML") != -1:
        trial_data_present = True
        print(phARKma_utils.timestamp() + "found existing clinical trials xml archive data in local directory")


    #if it is there, then check to see how long ago it was fetched
    if trial_data_present == True:
        if str(os.listdir()).find("trial_data_fetch_time") == -1:
            print(phARKma_utils.timestamp() + "Fetch time record not found, proceeding on the assumption that trial database is deprecated.")
            last_fetch = 9999
        else:
            last_fetch = check_last_fetch_time()
            print(phARKma_utils.timestamp() + "Trial data archive is not deprecated. Last fetch was " + str(last_fetch) + " days ago.")

    #if it isnt there, then download it and record the time
    else:
        if download == True:
            print(phARKma_utils.timestamp() + "No clinical trials raw data directory found. Downloading data now...")
            download_trial_data()
            new_data_downloaded = True
            record_time()
        else:
            print(phARKma_utils.timestamp() + "No clinical trials raw data found.")


    #if it was found and the date at which it was downloaded was found to be longer than 2 days ago,
    #this will cause it to delete it and download a new copy.
    if last_fetch > 2:
        if download == True:
            print(phARKma_utils.timestamp() + "Clinical trials data is deprecated. Wiping clinical trials data...")
            delete_clinical_trials_data()
            print(phARKma_utils.timestamp() + "Downloading new clinical trials data archive...")
            download_trial_data()
            new_data_downloaded = True
            record_time()
    else:
        if download == True:
            print(phARKma_utils.timestamp() + "Clinical trials data is not deprecated, proceeding...")

    if download == True:
        #if we have updated the clinical trials database, we need to update the corresponding csv file.
        if new_data_downloaded == False:
            try:
                os.remove("auxillary_data/trials_database.csv")
            except:
                pass
            #now get the directories containing all the clinical trials data
            all_path = str(os.getcwd())+ "\AllPublicXML"
            for dir in os.listdir(all_path):
                if dir.find("NCT") != -1:
                    directories.append((all_path+ "/" + str(dir)))

            for directory in directories:
                for file in os.listdir(directory):
                    files.append(directory +"/" + str(file))
                    trial_ids.append((str(file).split(".")[0]))

            print(phARKma_utils.timestamp() + "Trial data retrieved...")
            print(phARKma_utils.timestamp() + "Assembling data structures...")

            #now iterate through those data
            study_data = {}

            with alive_bar(len(files)) as bar:
                for file in files:
                    study_data = {}
                    process_trial(file, study_data, trials)
                    bar()

            #now create a csv using the data we pull here
            print(phARKma_utils.timestamp() + "Constructing pandas dataframe...")
            df = pd.DataFrame(trials)
            df.columns = map(str.upper, df.columns)
            df.drop_duplicates
            df.to_csv("auxillary_data/trials_database.csv")


