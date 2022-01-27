from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import random
import datetime
import csv
from datetime import date
import config

class LinkedinEmployeesSchoolinfoDataScraper():
    def __init__(self):
        DEFAULT_PATH = os.path.join(os.path.dirname(__file__))
        driverPath = DEFAULT_PATH+"\chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-setuid-sandbox')
        self.options.add_argument("--proxy-server='direct://")
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-accelerated-2d-canvas')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("start-maximized")
        self.options.add_argument("-incognito")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=self.options, executable_path=os.getcwd()+"/chromedriver.exe")
        self.url = 'https://www.linkedin.com/login'
        email = config.linkedin_email
        password = config.linkedin_password
        self.start()

    def find_element(self, css, attrib, element):
        try:
            return element.find_element_by_css_selector(css).get_attribute(attrib)
        except:
            return ''

    def get_element_text(self, css, element):
        try:
            return element.find_element_by_css_selector(css).text
        except:
            return ''

    def captcha(self):
        while(True):
            if "Let's do a quick security check" in self.driver.page_source:
                choice = input('please solve captcha then press Y:   ')
                if choice.lower() != 'y':
                    continue
            break

    def sleep(self, min, max):
        ranum = 0
        ranum = random.randint(min, max)
        time.sleep(ranum)

    def internetconnection(self):
        while(True):
            if "No internet" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "This site can’t be reached" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "Your connection was interrupted" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            if "This page isn’t working" in self.driver.page_source:
                self.sleep(3, 5)
                self.driver.refresh
                continue
            break

    def login(self):
        try:
            self.driver.get(self.url)
        except:
            pass
        self.internetconnection()
        self.captcha()
        self.sleep(3, 6)
        email = config.linkedin_email
        password = config.linkedin_password
        try:
            self.driver.find_element_by_css_selector(
                "input[id='username']").clear()
            self.sleep(1, 2)
            self.driver.find_element_by_css_selector(
                "input[id='username']").send_keys(email)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element_by_css_selector(
                "input[id='password']").clear()
            self.sleep(1, 2)
            self.driver.find_element_by_css_selector(
                "input[id='password']").send_keys(password)
            self.sleep(1, 2)
        except:
            pass
        try:
            self.driver.find_element_by_css_selector(
                "button[type='submit']").click()
            self.sleep(5, 6)
            self.internetconnection()
            self.captcha()
        except:
            pass

    def phase3_Scraping(self):
        FIELD_NAMES = ['Company Name', 'Location',
                       '# Employees', 'Company Url']
        with open('employee_data.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
            writer.writeheader()
        file_object = open("linkedin_urls.txt", "r")
        if file_object.mode == 'r':
            urls = file_object.readlines()
        for url in urls:
            companyname = ""
            Schoolname = ""
            hiredemployees = ""
            url = url.strip()
            if "/people" not in url:
                try:
                    self.driver.get(url+"/people/")
                except:
                    pass
            else:
                try:
                    self.driver.get(url)
                except:
                    pass
            self.internetconnection()
            self.captcha()
            self.sleep(3, 4)
            if "Sign" in self.driver.current_url:
                self.login()
            if "login" in self.driver.current_url:
                self.login()
            if "Sign Up | LinkedIn" in self.driver.title:
                self.sleep(60, 100)
                self.login()
            companyname = self.get_element_text(
                "div[class='block mt2']>div>h1", self.driver)
            try:
                self.driver.find_element_by_xpath(
                    "//*[@class='org-people__show-more-button t-16 t-16--open t-black--light t-bold']").click()
                self.sleep(2, 3)
            except:
                pass
            try:
                nodes = self.driver.find_elements_by_xpath(
                    "//*[@class='artdeco-card p4 m2 org-people-bar-graph-module__geo-region']//button[not(contains(@aria-label, 'Add any location'))]")
                for row in nodes:
                    try:
                        temp = row.text
                    except:
                        pass
                    try:
                        hiredemployees = temp.split(' ')[0]
                    except:
                        pass
                    try:
                        location = temp.split(None, 1)[1]
                    except:
                        pass
                    try:
                        with open('employee_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(
                                csvfile, fieldnames=FIELD_NAMES)
                            rowData = {'Company Name': companyname, 'Location': location,
                                       '# Employees': hiredemployees, 'Company Url': url}
                            writer.writerow(rowData)
                    except:
                        pass
                #self.sleep(10, 15)
            except:
                pass
            csvfile.close()

    def phase2_Scraping(self):
        FIELD_NAMES = ['Company Name', 'School Name',
                       '# Hired Employees', 'Company Url']
        with open('employee_education.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
            writer.writeheader()
        file_object = open("linkedin_urls.txt", "r")
        if file_object.mode == 'r':
            urls = file_object.readlines()
        for url in urls:
            companyname = ""
            Schoolname = ""
            hiredemployees = ""
            url = url.strip()
            if "/people" not in url:
                try:
                    self.driver.get(url+"/people/")
                except:
                    pass
            else:
                try:
                    self.driver.get(url)
                except:
                    pass
            self.internetconnection()
            self.captcha()
            self.sleep(3, 4)
            if "Sign" in self.driver.current_url:
                self.login()
            if "login" in self.driver.current_url:
                self.login()
            if "Sign Up | LinkedIn" in self.driver.title:
                self.sleep(60, 100)
                self.login()
            companyname = self.get_element_text(
                "div[class='block mt2']>div>h1", self.driver)
            try:
                self.driver.find_element_by_xpath(
                    "//*[@class='org-people__show-more-button t-16 t-16--open t-black--light t-bold']").click()
                self.sleep(2, 3)
            except:
                pass
            try:
                nodes = self.driver.find_elements_by_xpath(
                    "//*[@class='artdeco-card p4 m2 org-people-bar-graph-module__organization']//button[not(contains(@aria-label, 'Add any school'))]")
                for row in nodes:
                    try:
                        temp = row.text
                    except:
                        pass
                    try:
                        hiredemployees = temp.split(' ')[0]
                    except:
                        pass
                    try:
                        Schoolname = temp.split(None, 1)[1]
                    except:
                        pass
                    try:
                        with open('employee_education.csv', 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(
                                csvfile, fieldnames=FIELD_NAMES)
                            rowData = {'Company Name': companyname, 'School Name': Schoolname,
                                       '# Hired Employees': hiredemployees, 'Company Url': url}
                            writer.writerow(rowData)
                    except:
                        pass
                #self.sleep(10, 15)
            except:
                pass

    def start(self):
        self.login()
        self.phase3_Scraping()
        self.phase2_Scraping()
        self.phase3_Scraping()
