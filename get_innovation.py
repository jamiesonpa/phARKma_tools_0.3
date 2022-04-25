import get_company_data
import os
import urllib3
import requests
import json
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = ('https://patents.google.com/?assignee=Pacific+Biosciences+California&country=US&language=ENGLISH&type=PATENT')
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path ="C:\\Users\\Pierce Jamieson\\Desktop\\python_projects\\phARKma_3\\phARKma_tools_0.2\\chromedriver.exe", chrome_options=options)
driver.get(url)
time.sleep(3)
page = driver.page_source
driver.quit()
soup = BeautifulSoup(page, 'html.parser')
patents_found = False
for a in soup.find_all("a"):
    if str(a).find("href") != -1:
        if str(a).find("download=true") != -1:
            if patents_found == False:
                patent_url = "https://patents.google.com/" + (str(a).split('href="')[1].split('" style=')[0])
                patents_found = True

req = requests.get(patent_url)
patent_json = json.loads(req.content)
patents = []
for key in patent_json.keys():
    print(key)
# for item in patent_json["results"]["cluster"]:
#     patents.append(item["result"])

# for p in patents:
#     for item in p:
#         print(item["patent"]["title"])


# for patent in patents:
#     print(patent["title"])
