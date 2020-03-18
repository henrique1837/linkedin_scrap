# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:54:04 2020

@author: henrique
"""

import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

SELENIUM_PATH = "/home/henrique/Documents/selenium/geckodriver"
CSV_FILENAME = "/home/henrique/Documents/scraps/linkedin_scrap/sample.csv"

url_base = "https://www.linkedin.com"
url = "https://www.linkedin.com/school/univeritas/people/"

profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", False)
profile.set_preference("dom.webnotifications.enabled", False)




driver = webdriver.Firefox(executable_path=SELENIUM_PATH,firefox_profile=profile)
driver.get(url)


## Funcao de login aqui ##

## Scrap ##

cond = True

while cond:
    source_len1 = len(driver.page_source)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
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

df.to_csv(path_or_buf=CSV_FILENAME)


## Get users info 


driver = webdriver.Firefox(executable_path=SELENIUM_PATH,firefox_profile=profile)

ocupation = []
localization = []
totalConnections = []
about = []
experience = []
education = []
for i in range(len(df.link)):
    url_user = df.link[i]
    driver.get(url_user)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.8)
    source = driver.page_source
    soup = BeautifulSoup(source,"lxml")
    user_resume = soup.find(attrs={"class":"pv-top-card"})
    try:
        ocupation.append(user_resume.find("h2",attrs={"class":"mt1"}).text)
    except:
        ocupation.append(None)
    try:
        localization.append(user_resume.find("ul",attrs={"class":"pv-top-card--list-bullet"}).findAll("li")[0].text)
    except:
        localization.append(None)
    try:
        totalConnections.append(user_resume.find("ul",attrs={"class":"pv-top-card--list-bullet"}).findAll("li")[1].text)
    except:
        totalConnections.append(None)
    try:
        about.append(soup.find("section",attrs={"class":"pv-about-section"}).p.text)
    except:
        about.append(None)
    try:
        experience.append(soup.find(attrs={"id":"experience-section"}).text)
    except:
        experience.append(None)
    try:
        education.append(soup.find(attrs={"id":"education-section"}).text)
    except:
        education.append(None)
    
    print("Getting data from "+str(i+1)+" of "+str(len(df.link)))