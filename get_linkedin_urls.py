
import requests
import get_details
import get_arkg_tickers
from bs4 import BeautifulSoup

def get_linkedin_urls():
    tickers = get_arkg_tickers.get_arkg_tickers()
    names = []
    for ticker in tickers:
        name = get_details.get_details(ticker, False)["NAME"]
        names.append(name)
    urls = []
    for name in names:
        namestring = ""
        name = name.replace("&","")
        name = name.replace(".","")
        name = name.replace("/","")
        name = name.replace(",","")
        namesplit = name.split(" ")
        for ns in namesplit:
            namestring = namestring + ns + "-"
        
        namestring = namestring[0:(len(namestring)-1)]
        print(namestring)
        namestring = namestring + "-linkedin"

        print("https://www.google.com/search?q="+namestring)
        urls.append("https://www.google.com/search?q="+namestring)
    
    linkedin_urls = []
    for url in urls:
        try:
            req = requests.get(url)
            query = url.split("?")[1].replace("q=","query:")
            soup = BeautifulSoup(req.content, "html.parser")
            a_eles = soup.find_all("a")
            good_as = []
            for a in a_eles:
                if str(a).find("www.linkedin.com") != -1:
                    good_as.append(str(a))

            linkedin_url = (good_as[0].split("/url?q=")[1].split("&amp")[0])
            if str(linkedin_url)[-1] == "-":
                linkedin_url = str(linkedin_url)[0:len(str(linkedin_url))-1]
            linkedin_urls.append(str(linkedin_url))
        except:
            pass
    return linkedin_urls

def get_entries():
    import requests

    url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3740566_indicators.txt?1637817445?v=1637823042256"

    headers = {
        "user-agent": "Mozilla/5.0",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    def make_pretty(entry):
        from bs4 import BeautifulSoup as Soup
        return {
            "name": Soup(entry["uni"], "html.parser").select_one(".uni-link").get_text(strip=True),
            "rank": entry["overall_rank"],
            "reputation": Soup(entry["ind_76"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
        }

    yield from map(make_pretty, response.json()["data"])

def get_universities():

    from itertools import islice

    entry_list = []
    for entry in get_entries():
        entry_list.append(entry)

    return entry_list