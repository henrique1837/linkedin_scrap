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

path = "/home/henrique/Documents/scraps/labore_scrap/"
os.chdir(path)

from aux_var import *




df = pd.read_csv(CSV_FILENAME)


## Get users info 


driver = webdriver.Firefox(executable_path=SELENIUM_PATH)

login(driver)

link = []
name = []
ocupation = []
localization = []
totalConnections = []
about = []
experience = []
education = []


for i in range(len(df.link)):

    url_user = df.link[i]
    driver.get(url_user)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    source = driver.page_source
    soup = BeautifulSoup(source,"lxml")
    user_resume = soup.find(attrs={"class":"pv-top-card"})
    if(user_resume == None):
        df_final = pd.DataFrame({
            "link": link ,
            "name": name,
            "ocupation": ocupation,
            "localization": localization,
            "totalConnections": totalConnections,
            "about": about,
            "experience": experience,
            "education": education
            })
        df_final.to_json(CSV_FILENAME_COMPLETE)
        i = len(df.link)+1
    link.append(df.link[i])
    name.append(df.name[i])
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
        items = soup.find(attrs={"id":"experience-section"}).findAll("li")
        exp = []
        for j in range(len(items)):
            exp.append({
                "tittle": items[j].find("div",attrs={"class":"pv-entity__summary-info-v2"}).findAll("span")[1].text,
                "date_range": items[j].find("h4",attrs={"class":"pv-entity__date-range"}).findAll("span")[1].text,
                "duration": items[j].find("span",attrs={"class":"pv-entity__bullet-item-v2"}).text,
                "location": items[j].find("h4",attrs={"class":"pv-entity__location"}).findAll("span")[1].text,
                "description": items[j].find("p",attrs={"class":"pv-entity__description"}).text
            })
        experience.append(exp)
    except:
        experience.append(None)
    try:
        items = soup.find(attrs={"id":"education-section"}).findAll("li")
        edu = []
        descript = items[j].find("div",attrs={"class":"pv-entity__extra-details"})
        if(descript == None):
            descript = None
        else:
            descript = descript.text
        for j in range(len(items)):
            edu.append({
                "shcool": items[j].find("h3",attrs={"class":"pv-entity__school-name"}).text,
                "course": items[j].find("p",attrs={"class":"pv-entity__secondary-title"}).findAll("span")[1].text,
                "date_range": items[j].find("p",attrs={"class":"pv-entity__dates"}).findAll("span")[1].text,
                "description": descript      
            })
        education.append(edu)
    except:
        education.append(None)
    if(i%20 == 0 and i > 0):
        print("Cleaning selenium memory")
        driver.close()
        time.sleep(5)
        #webdriver.DesiredCapabilities.FIREFOX['proxy']={
        #    "httpProxy":proxies[j],
        #    "sslProxy":proxies[j],
        #    "proxyType":"MANUAL"
        #}
        j = j + 1
        if(j >= len(proxies)):
            j = 0
        driver = webdriver.Firefox(executable_path=SELENIUM_PATH)
        login(driver)
    
    print("Getting data from "+str(i+1)+" of "+str(len(df.link)))
    
    
df_final = pd.DataFrame({
            "link": link ,
            "name": name,
            "ocupation": ocupation,
            "localization": localization,
            "totalConnections": totalConnections,
            "about": about,
            "experience": experience,
            "education": education
            })
            
            
df_final.to_json(CSV_FILENAME_COMPLETE)