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

def login():
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    input_email = driver.find_element_by_id("username")
    input_email.click()
    input_email.send_keys(email)
    
    input_pass = driver.find_element_by_id("password")
    input_pass.click()
    input_pass.send_keys(password)
    
    div_login = driver.find_element_by_class_name("login__form_action_container")
    button_login = div_login.find_element_by_tag_name("button")
    button_login.click()

SELENIUM_PATH = "/home/henrique/Documents/selenium/geckodriver"
CSV_FILENAME = "/home/henrique/Documents/scraps/linkedin_scrap/sample.csv"
CSV_FILENAME_COMPLETE = "/home/henrique/Documents/scraps/linkedin_scrap/complete.csv"

email = "iAmTheScrap@GetYourPublicData.com"
password = "Some times we need to do that by force"


url_base = "https://www.linkedin.com"
url = "https://www.linkedin.com/school/univeritas/people/"

profile = webdriver.FirefoxProfile()
profile.set_preference("javascript.enabled", False)
profile.set_preference("dom.webnotifications.enabled", False)




driver = webdriver.Firefox(executable_path=SELENIUM_PATH,firefox_profile=profile)


login()

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

## Saving Sample ##

df.to_csv(path_or_buf=CSV_FILENAME)


## Get users info 


driver = webdriver.Firefox(executable_path=SELENIUM_PATH,firefox_profile=profile)


link = []
name = []
ocupation = []
localization = []
totalConnections = []
about = []
experience = []
education = []

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


for i in range(len(df.link)):
    link.append(df.link[i])
    name.append(df.name[i])
    url_user = df.link[i]
    driver.get(url_user)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
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
    if(i%10 == 0 and i > 0):
        print("Cleaning selenium memory")
        df_final = df_final.append({
            "link": link ,
            "name": name,
            "ocupation": ocupation,
            "localization": localization,
            "totalConnections": totalConnections,
            "about": about,
            "experience": experience,
            "education": education
        },ignore_index=True)
        ocupation = []
        localization = []
        totalConnections = []
        about = []
        experience = []
        education = []
        driver.close()
        time.sleep(1)
        driver = webdriver.Firefox(executable_path=SELENIUM_PATH,firefox_profile=profile)
        login()
    
    print("Getting data from "+str(i+1)+" of "+str(len(df.link)))