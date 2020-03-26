import requests
import pandas as pd
import numpy as np
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
""" Horse """
# "URL" horse generic tree

def dict_zip(*dicts):

    all_keys = {k for d in dicts for k in d.keys()}
    return {k: [d[k] for d in dicts if k in d] for k in all_keys}

def find_link_name(n,c,soup):
    #add name and link of father to the list

    try:
        searcher = soup.find('div',attrs={'class':n })

        if n == 'n4':

            
            searcher = searcher.find_all('a', href= True)
            genetic_tree.append((searcher[int(c[1:])-1].text))
            links_genetic_tree.append((ADD+searcher[int(c[1:])-1]['href']))

        else:

            searcher = searcher.find('div',attrs={'class':c}).find('a', href=True) 
            genetic_tree.append((searcher.text))
            links_genetic_tree.append((ADD+searcher['href']))

    except:
        
        pass

def extract_tree(link,pos):

        #selenium webdriver : open browser and enter URL
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        URL2=link
        browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",options=options)
        browser.get(URL2)

        
        try:

            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Ver listado de hijos completo"))
            )
            time.sleep(4)
            browser.find_element_by_link_text('Ver listado de hijos completo').send_keys("\n")
            soup_2 = BeautifulSoup(browser.page_source, 'html.parser')
            info_2 = soup_2.find('div',attrs={'class':'info-caballo'}).findAll('dt')
            criaderos_genetic_tree[pos] = info_2[1].text[10:]
            registros_genetic_tree[pos] = info_2[7].text[20:]

            listado = soup_2.find('tbody',attrs={'id':'hi'}).findAll('a')


            while len(listado) == 0:

                browser.find_element_by_link_text('Ver listado de hijos completo').send_keys("\n")
                browser.implicitly_wait(50)
                soup_2 = BeautifulSoup(browser.page_source, 'html.parser')
                info_2 = soup_2.find('div',attrs={'class':'info-caballo'}).findAll('dt')
                listado = soup_2.find('tbody',attrs={'id':'hi'}).findAll('a')

            else:

                n_hijos[pos] = (len(listado)/2)
                browser.close()
            #extraction of name and ranch breeder of each horse in the genetic tree.

        finally:

            browser.quit()

def add_dic(soup):

    caballos = dict_zip(criaderos_genetic_tree,registros_genetic_tree,n_hijos)
    info = soup.find('div',attrs={'class':'info-caballo'}).findAll('dt')
   # horses[info[7].text[20:]]={(pos+1):gen,'Criadero1':info_2[1].text[10:],'Registro'+(pos+1):info_2[7].text[20:]}
    horses[info[7].text[20:]]={'Nombre':info[0].text[8:],'Criadero':info[1].text[10:],'Sexo':info[5].text[6:],'Color':info[2].text[7:],'Fecha Nacimiento':info[3].text[12:]}
    
    for a in range(30):

        try:

            horses[info[7].text[20:]]['Name{}'.format(str(a+1))] = genetic_tree[a]
            
            horses[info[7].text[20:]]['Criadero{}'.format(str(a+1))]=caballos[a+1][0]
            
            horses[info[7].text[20:]]['Registro{}'.format(str(a+1))]=caballos[a+1][1]
            
            horses[info[7].text[20:]]['N_Hijos{}'.format(str(a+1))]=caballos[a+1][2]

        except:

            horses[info[7].text[20:]]['Name{}'.format(str(a+1))] = '0'
            
            horses[info[7].text[20:]]['Criadero{}'.format(str(a+1))]= '0'
            
            horses[info[7].text[20:]]['Registro{}'.format(str(a+1))]= '0'
            
            horses[info[7].text[20:]]['N_Hijos{}'.format(str(a+1))]= '0'

def url_search(url):

    try:

        page_1 = requests.get(url)
        soup = BeautifulSoup(page_1.content, 'html.parser')
        #find characteristic of the horse.
        #extract all the genetic tree and save it in a list.

        [find_link_name('n'.format(str(n+1)),'c'.format(str(c+1)),soup) for n in range(4) for c in range(17)]
        print(genetic_tree)
        threadlist = []

        for pos,link in enumerate(links_genetic_tree):

            t = Thread(target=extract_tree,args=(link,(pos+1)))
            t.start()
            threadlist.append(t)

        [b.join() for b in threadlist]

        add_dic(soup)

        del genetic_tree[:]
        del links_genetic_tree[:]
        criaderos_genetic_tree={}
        registros_genetic_tree={}
        n_hijos={}

    except requests.exceptions.ConnectionError:

        status_code = "Connection refused"
        print(status_code)


if __name__ == "__main__":

    genetic_tree = []
    links_genetic_tree = []
    criaderos_genetic_tree={}
    registros_genetic_tree={}
    n_hijos = {}
    horses = {}

    csv_columns = ['Nombre', 'Criadero', 'Sexo', 'Color', 'Fecha Nacimiento', 'Name1', 'Criadero1', 'Registro1', 'N_Hijos1', 'Name2', 'Criadero2', 'Registro2', 'N_Hijos2', 'Name3', 'Criadero3', 'Registro3', 'N_Hijos3', 'Name4', 'Criadero4', 'Registro4', 'N_Hijos4', 'Name5', 'Criadero5', 'Registro5', 'N_Hijos5', 'Name6', 'Criadero6', 'Registro6', 'N_Hijos6', 'Name7', 'Criadero7', 'Registro7', 'N_Hijos7', 'Name8', 'Criadero8', 'Registro8', 'N_Hijos8', 'Name9', 'Criadero9', 'Registro9', 'N_Hijos9', 'Name10', 'Criadero10', 'Registro10', 'N_Hijos10', 'Name11', 'Criadero11', 'Registro11', 'N_Hijos11', 'Name12', 'Criadero12', 'Registro12', 'N_Hijos12', 'Name13', 'Criadero13', 'Registro13', 'N_Hijos13', 'Name14', 'Criadero14', 'Registro14', 'N_Hijos14', 'Name15', 'Criadero15', 'Registro15', 'N_Hijos15', 'Name16', 'Criadero16', 'Registro16', 'N_Hijos16', 'Name17', 'Criadero17', 'Registro17', 'N_Hijos17', 'Name18', 'Criadero18', 'Registro18', 'N_Hijos18', 'Name19', 'Criadero19', 'Registro19', 'N_Hijos19', 'Name20', 'Criadero20', 'Registro20', 'N_Hijos20', 'Name21', 'Criadero21', 'Registro21', 'N_Hijos21', 'Name22', 'Criadero22', 'Registro22', 'N_Hijos22', 'Name23', 'Criadero23', 'Registro23', 'N_Hijos23', 'Name24', 'Criadero24', 'Registro24', 'N_Hijos24', 'Name25', 'Criadero25', 'Registro25', 'N_Hijos25', 'Name26', 'Criadero26', 'Registro26', 'N_Hijos26', 'Name27', 'Criadero27', 'Registro27', 'N_Hijos27', 'Name28', 'Criadero28', 'Registro28', 'N_Hijos28', 'Name29', 'Criadero29', 'Registro29', 'N_Hijos29', 'Name30', 'Criadero30', 'Registro30', 'N_Hijos30']

    ADD = "http://www1.caballoyrodeo.cl/portal_rodeo/stat/port/genealogia.html"

    count=0

    with open('links_caballos_completos_2020.csv', 'r') as file:

        reader = csv.reader(file)

        for row in reader:

            start = time.time()
            #t = Thread(target= url_search, args=(row[0],))
            url_search(row[0])
            #t.start()
            #threadlist.append(t)
            end = time.time()
            count+=1
            print('N:',count,'time:',(end - start))


    dict_data = horses
    csv_file = "caballos.csv"


    try:

        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for key in dict_data:
                writer.writerow(dict_data[key])

    except IOError:

        print("I/O error")
