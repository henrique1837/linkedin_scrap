# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:49:50 2020

@author: henrique
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

path = "./"
os.chdir(path)

from aux_var import *

## Htmls already extracted 

html_files = os.listdir("./htmls")

## Links 

df = pd.read_csv(CSV_PATHNAME+"publicas/rural/adm_rural.csv")

## Get users HTML


driver = webdriver.Firefox(executable_path=SELENIUM_PATH)

login(driver,email,senha)
input("Press Enter to continue...")
# time.sleep(60)


n = len(html_files)-1
if (n < 1):
    n = 0
total_per_time = 1

for i in range(n,n+total_per_time):
    ## Change to df.link[i] if link does not ends with '/'
    url_user = df.link[n+i][:-1]
    driver.get(url_user)

    cond = True

    while cond:
        source_len1 = len(driver.page_source)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        source_len2 = len(driver.page_source)
        
        
        # Mostrar que está dando scroll
        if(source_len2 == source_len1):
            cond = False
        print("Scroll down")
    
    # Clicar no botão "Ver mais"
    try:
        a_show = driver.find_elements_by_class_name(
            "pv-profile-section__see-more-inline")
        # driver.execute_script("window.scrollTo(0, "+str(a_show.location['y']-300)+");")
        a_show[1].click()
        input("Estou aqui")
        time.sleep(0.5)
    except:
        input("Deu erro")
        a_show = None

    # Clicar no botão "ver mais" Skills
    try:
        a_show = driver.find_element_by_class_name(
            "pv-skills-section__additional-skills")
        # driver.execute_script("window.scrollTo(0, "+str(a_show.location['y']-300)+");")
        a_show.click()
        time.sleep(0.5)
    except:
        a_show = None

    # for j in range(10,1,-1):
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight/"+str(j)+");")
    #     time.sleep(0.4)
        
    
        
    # show_more = driver.find_elements_by_class_name("pv-profile-section__see-more-inline")
    # for button in show_more:
    #     driver.execute_script("window.scrollTo(0, "+str(button.location['y']-300)+");")
    #     button.click()
    #     time.sleep(0.5)
    source = driver.page_source
    ## Save
    with open("./htmls/"+str(n+i)+"_"+url_user.split("/")[-1]+".html", "w", encoding="utf-8") as text_file:
        text_file.write(source)
    
print("Execução finalizada")
    



# driver.close()
