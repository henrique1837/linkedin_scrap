# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 03:30:29 2020

@author: henrique
"""

import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def getProxies():
    url = 'https://free-proxy-list.net/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    table = soup.find("table")
    proxies = []
    tr = table.findAll("tr")
    for i in range(1,len(tr)-1):
        ip = tr[i].findAll("td")[0].text
        port = tr[i].findAll("td")[1].text
        proxies.append(ip+":"+port)
    return proxies

def login(driver):
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


## Inicio ##

proxies = getProxies()


SELENIUM_PATH = "/home/henrique/Documents/selenium/geckodriver"
CSV_FILENAME = "/home/henrique/Documents/scraps/labore_scrap/sample.csv"
CSV_FILENAME_COMPLETE = "/home/henrique/Documents/labore_scrap/complete.json"


#webdriver.DesiredCapabilities.FIREFOX['proxy']={
#            "httpProxy":proxies[0],
#            "sslProxy":proxies[0],
#            "proxyType":"MANUAL"
#}



email = "LOGIN DA CONTA"
password = "SENHA DA CONTA"
