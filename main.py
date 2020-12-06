from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import credentials
username, password = credentials.login['username'], credentials.login['password']

#start driver
driver = webdriver.Chrome(ChromeDriverManager().install())
delay = 30
timeerror = "Loading time exceded"

def go_login():
    connection_url = 'https://www.atrium-sud.fr/connexion/login?service=https:%2F%2F0061642C.index-education.net%2Fpronote%2F'
    driver.get(connection_url)

    #input credentials
    form_username = driver.find_element_by_name('username').send_keys(username)
    form_psw = driver.find_element_by_name('password').send_keys(password)
    form_submit = driver.find_element_by_css_selector('[type=submit]').click()

def prepare_extract():
    #wait for load
    voirplus_btn = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//header[@title="Notes des 14 derniers jours"]//div'))) 

    #click on voir plus de notes
    driver.execute_script("GInterface.Instances[2]._surToutVoir(10)", voirplus_btn)

    #wait for load
    check = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//tr'))) 

    #clique sur les notes pour toutes les faire apparaitre
    redfn = lambda : driver.find_elements_by_xpath('//tbody//tr[@valign="top"]//td[starts-with(@id, "GInterface.Instances[2].Instances[1]_0")]') 
    
    i = 0
    prev = 0
    print(len(redfn()))
    while prev != len(redfn()):
        if prev != len(redfn()):
            prev = len(redfn())
        reduce = redfn()
        
        print(len(reduce))
        try:
            reduce[i].click() 
        except:
            pass

        i+=1

def extract_val():
    listedata = driver.find_elements_by_xpath('//div[@class="Gras Espace"]//div')
    nom= [] 
    note = []

    for i in range(0,len(listedata),2):
        nom.append(listedata[i+1].text)
        note.append(listedata[i].text)

    for i in range(len(note)):
        note[i] = float(note[i].replace(',','.'))
    
    return nom,note

def main():

    go_login()
    prepare_extract()
    nom, note = extract_val()

    for i in range(len(note)):
        print(f"{nom[i]} | {note[i]}")

main()