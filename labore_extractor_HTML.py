# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:49:50 2020

@author: henrique
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

path = "/home/henrique/Documents/scraps/labore_scrap/"
os.chdir(path)

from aux_var import *

## Htmls already extracted 

html_files = os.listdir("./htmls")

## Links 

df = pd.read_csv(CSV_FILENAME)

## Get users HTML


driver = webdriver.Firefox(executable_path=SELENIUM_PATH)

login(driver,"EMAIL","SENHA")


n = len(html_files)
total_per_time = 20

for i in range(n,n+total_per_time):
    ## Change to df.link[i] if link does not ends with '/'
    url_user = df.link[n][:-1]
    driver.get(url_user)
    
    for j in range(10,1,-1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/"+str(j)+");")
        time.sleep(0.4)
        
    try:
        a_show = driver.find_element_by_id("line-clamp-show-more-button")
        driver.execute_script("window.scrollTo(0, "+str(a_show.location['y']-300)+");")
        a_show.click()
        time.sleep(0.5)
    except:
        a_show = None
        
    show_more = driver.find_elements_by_class_name("pv-profile-section__see-more-inline")
    for button in show_more:
        driver.execute_script("window.scrollTo(0, "+str(button.location['y']-300)+");")
        button.click()
        time.sleep(0.5)
    source = driver.page_source
    ## Save
    with open("./htmls/"+str(n+i)+"_"+url_user.split("/")[-1]+".html", "w") as text_file:
        text_file.write(source)
    
    



driver.close()