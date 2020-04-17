# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 17:49:50 2020

@author: henrique
"""

from login_string import *
from links.links_UNIRIO import *
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

path = "./"
os.chdir(path)

from aux_var import *

from login_string import *



## Links 

df = pd.read_csv(CSV_PATHNAME+"publicas/rural/adm_rural.csv")

## Get users HTML


driver = webdriver.Firefox(executable_path=SELENIUM_PATH)

# login(driver,email,senha)
# input("Press Enter to continue...")
# time.sleep(60)

for login_string in emailLogin:
    time.sleep(3)
    print("\n\nExecutando usando: "+login_string+"")

    login(driver, login_string, senha)
    time.sleep(3)

    ## Htmls already extracted
    html_files = os.listdir("./htmls")

    n = len(html_files)
    total_per_time = 1

    for i in range(n,n+total_per_time):
        ## Change to df.link[i] if link does not ends with '/'
        url_user = df.link[i][:-1]
        driver.get(url_user)
        # driver.get("https://www.linkedin.com/in/grace-costa-adm/")

        cond = True

        while cond:
            source_len1 = len(driver.page_source)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            print("Scroll down")
            time.sleep(5)

            # Clicar no botão "Ver mais"
            try:
                a_show = driver.find_elements_by_class_name("pv-profile-section__see-more-inline")
                # driver.execute_script("window.scrollTo(0, "+str(a_show.location['y']-300)+");")
                # for show_more in a_show:
                for element in a_show:
                    if not ("Visualizar" in element.text):
                        driver.execute_script(
                            "window.scrollTo(0, "+str(element.location['y']-52-64)+");")
                        time.sleep(0.5)
                        element.click()
                time.sleep(0.5)
            except Exception as e:
                print ("Error: \n"+str(e))
                a_show = None
            
            source_len2 = len(driver.page_source)
            
            # Mostrar que está dando scroll
            if(source_len2 == source_len1):
                cond = False
                print("Stopping Scroll")
           
        time.sleep(5)
        
        # Clicar no botão "ver mais" Skills
        try:
            a_show = driver.find_element_by_class_name("pv-skills-section__additional-skills")
            print("Abrindo a página de Skills")
            # driver.execute_script("window.scrollTo(0, "+str(a_show.location['y']-300)+");")
            driver.execute_script(
                "window.scrollTo(0, "+str(a_show.location['y']-52-64)+");")
            time.sleep(0.5)
            a_show.click()
        except Exception as e:
            print("Error: \n"+str(e))
            a_show = None

        #Carregar a página toda até o final antes de salvar, após abrir todos os links
        cond = True
        print("Carregando até o fim da página")
        while cond:
            source_len1 = len(driver.page_source)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            source_len2 = len(driver.page_source)
            print("Scroll down")
            # Mostrar que está dando scroll
            if(source_len2 == source_len1):
                cond = False
                print("Stopping Scroll")
            
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
        with open("./htmls/"+str(i)+"_"+url_user.split("/")[-1]+".html", "w", encoding="utf-8") as text_file:
            text_file.write(source)
        
        print("Página de número "+str(i)+" salva com sucesso\n")
        # time.sleep(10)
    
print("Execução finalizada")
    



driver.close()
