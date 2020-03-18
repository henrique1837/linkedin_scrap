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
    for j in range(10,1,-1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/"+str(j)+");")
        time.sleep(0.4)
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
            title = items[j].find("p",attrs={"class":"pv-entity__secondary-title"})
            if(title != None):
                title = title.text
            date_range = items[j].find("h4",attrs={"class":"pv-entity__date-range"})
            if(date_range != None):
                date_range = date_range.findAll("span")[1].text
            duration = items[j].find("span",attrs={"class":"pv-entity__bullet-item-v2"})
            if(duration != None):
                duration = duration.text
            location = items[j].find("h4",attrs={"class":"pv-entity__location"})
            if(location != None):
                location = location.findAll("span")[1].text
            description = items[j].find("p",attrs={"class":"pv-entity__description"})
            if(description != None):
                description = description.text
            exp.append({
                "tittle": title ,
                "date_range": date_range,
                "duration": duration,
                "location": location,
                "description": description
            })
        experience.append(exp)
    except:
        experience.append(None)
    try:
        items = soup.find(attrs={"id":"education-section"}).findAll("li")
        edu = []
        for j in range(len(items)):
            school = items[j].find("h3",attrs={"class":"pv-entity__school-name"})
            if(school != None):
                school = school.text
            descript = items[j].find("div",attrs={"class":"pv-entity__extra-details"})
            if(descript != None):
                descript = descript.text
            course = items[j].find("p",attrs={"class":"pv-entity__fos"})
            if(course != None):
                course = course.findAll("span")[1].text
            degree = items[j].find("p",attrs={"class":"pv-entity__degree-name"})
            if(degree != None):
                degree = degree.findAll("span")[1].text
            data_range = items[j].find("p",attrs={"class":"pv-entity__dates"})
            if(data_range != None):
                data_range = data_range.findAll("span")[1].text        
            edu.append({
                    "shcool": school,
                    "course": course,
                    "degree": degree,
                    "date_range": date_range,
                    "description": descript      
            })
        education.append(edu)
    except:
        education.append(None)
    if(i%20 == 0 and i > 0):
        print("Cleaning selenium memory")
        driver.close()
        time.sleep(5)
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




import json
json_arr = []
for i in range(len(df_final.link)):
    json_arr.append({
            "link": df_final.link[i],
             "content" :{
                "name": df_final.name[i],
                "ocupation": df_final.ocupation[i],
                "localization": df_final.localization[i],
                "totalConnections": df_final.totalConnections[i],
                "about": df_final.about[i],
                "experience": df_final.experience[i],
                "education": df_final.education[i]  
            }
    })

with open('complete_arr.json', 'w') as f:
    json.dump(json_arr, f)