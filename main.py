from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
from os import system, name 
import sys
from rich.console import Console
from rich.table import Column, Table
console = Console()

try:
    import credentials
    username, password = credentials.login['username'], credentials.login['password']
except:
    username = input("identifiant Atrium : ")
    password = input("mot de pass Atrium : ")
    with open("credentials.py", "w") as file:
        file.write('login = {')
        file.write(f'"username" : "{username}",')
        file.write(f'"password" : "{password}"')
        file.write('}')


#start driver
driver = webdriver.Chrome(ChromeDriverManager().install())
delay = 30
timeerror = "Loading time exceded"

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')     

def printConsole(nom,note,listcoef):
    clear()
    table = Table(show_header=True, header_style="bold magenta")
    
    table.add_column("Matières", justify="center")
    table.add_column("Notes")

    for i in range(len(note)):
        try:
            table.add_row(nom[i], str(note[i]))
        except:
            pass
    table.add_row()
    withoutnull = []
    withoutnullcoef = []
    for i in range(len(note)):
        if type(note[i]) == float:
            withoutnull.append(note[i])
    for i in range(len(listcoef)):
        if type(listcoef[i]) == float:
            withoutnullcoef.append(listcoef[i])
    table.add_row(f'[bold magenta]MOYENNE[/bold magenta]', str((sum(withoutnull)//len(withoutnull))))
    table.add_row(f'[bold yellow]MOYENNE COEF[/bold yellow]', str((sum(withoutnullcoef)//len(withoutnullcoef))))
    console.print(table)

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
    check = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//td'))) 

    #clique sur les notes pour toutes les faire apparaitre
    redfn = lambda : driver.find_elements_by_xpath('//tbody//tr[@valign="top"]//td[starts-with(@id, "GInterface.Instances[2].Instances[1]_0")]') 
    
    print(len(redfn()))
    assert len(redfn()) != 0

    i = 0
    prev = 0
    while prev != len(redfn()):
        if prev != len(redfn()):
            prev = len(redfn())
        reduce = redfn()
        

        try:
            reduce[i].click() 
        except:
            pass

        i+=1

def extract_val():
    listedata = driver.find_elements_by_xpath('//div[@class="Gras Espace"]//div')
    print(len(listedata))
    nom= [] 
    note = []

    for i in range(0,len(listedata),2):
        nom.append(listedata[i+1].text)
        note.append(listedata[i].text)

    for i in range(len(note)):
        try:
            note[i] = float(note[i].replace(',','.'))
        except:
            continue
    return nom,note

def get_coef(note):
    res = note[:]
    res.pop(0)
    res[1] = round((res[0]+res[1])/2,2)
    res.pop(0)
    res[-2] = round((res[-1]+res[-2])/2,2)
    res.pop(-1)
    return res

def main():
    clear()
    go_login()
    prepare_extract()
    nom, note = extract_val()
    listcoef = get_coef(note)


    printConsole(nom,note,listcoef)

main()