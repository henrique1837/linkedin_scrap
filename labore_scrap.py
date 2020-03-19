# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 01:32:59 2020

@author: henrique
"""
import sys 
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

path = "/home/henrique/Documents/scraps/labore_scrap/"
os.chdir(path)

from aux_var import *

url_base = "https://www.linkedin.com"
url = "https://www.linkedin.com/school/univeritas/people/"

profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", False)
profile.set_preference("dom.webnotifications.enabled", False)

driver = webdriver.Firefox(executable_path=SELENIUM_PATH)

login(driver,"EMAIL","SENHA")

driver.get(url)

## Scrap ##

cond = True

while cond:
    source_len1 = len(driver.page_source)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2.5)
    source_len2 = len(driver.page_source)
    if(source_len2 == source_len1):
        cond = False
    print("Scroll down")

source = driver.page_source
driver.close()

soup = BeautifulSoup(source,"lxml")
ul_people = soup.find(attrs={"class":"org-people-profiles-module__profile-list"})

a_links = ul_people.findAll("a",attrs={"class":"link-without-visited-state"})

df = pd.DataFrame({
                   "name":[],
                   "link" : []
                  })

for i in range(len(a_links)):
    a_link = a_links[i]
    df = df.append({
        "name": a_link.text,
        "link": url_base+a_link["href"]
    },
    ignore_index=True)

## Saving Sample ##

df.to_csv(path_or_buf=CSV_FILENAME)