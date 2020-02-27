import requests
import pandas as pd
import numpy as np
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

""" Horse """

URL = "http://www1.caballoyrodeo.cl/portal_rodeo/stat/port/genealogia.html?id=10939#gc"
ADD = "http://www1.caballoyrodeo.cl/portal_rodeo/stat/port/genealogia.html"

# "URL" horse generic tree

names = []
criaderos = []
edades = []
colores = []
sexos = []
registros = []

# genetic tree

genetic_tree = []
links_genetic_tree = []
criaderos_genetic_tree=[]
registros_genetic_tree=[]

def find_link_name(n,c):


    #add name and link of father to the list
    if n == 'n4':

        searcher = soup.find('div',attrs={'class':n })
        searcher = searcher.find_all('a', href= True)
        genetic_tree.append((searcher[int(c[1:])].text))
        links_genetic_tree.append((ADD+searcher[int(c[1:])]['href']))

    else:

        searcher = soup.find('div',attrs={'class':n }).find('div',attrs={'class':c}).find('a', href=True)    
        genetic_tree.append((searcher.text))
        links_genetic_tree.append((ADD+searcher['href']+'#chijos'))


try:

    page_1 = requests.get(URL)
    soup = BeautifulSoup(page_1.content, 'html.parser')
    
    #find characteristic of the horse.
    info = soup.find('div',attrs={'class':'info-caballo'}).findAll('dt')
    names.append(info[0].text[8:])
    criaderos.append(info[1].text[10:])
    colores.append(info[2].text[7:])
    edades.append(info[3].text[12:])
    sexos.append(info[5].text[6:])
    registros.append(info[7].text[20:])

#extract all the genetic tree and save it in a list.

    for n in range(4):
            for c in range(16):

                try:
                    find_link_name('n'+(str(n+1)),'c'+(str(c+1)))

                except:
                    pass

    for link in links_genetic_tree:
        try:
            #selenium webdriver : open browser and enter URL
            URL2=link
            browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
            browser.get(URL2)
            #extraction of name and ranch breeder of each horse in the genetic tree.
            soup_2 = BeautifulSoup(browser.page_source, 'html.parser')
            info = soup_2.find('div',attrs={'class':'info-caballo'}).findAll('dt')
            criaderos_genetic_tree.append(info[1].text[10:])
            registros_genetic_tree.append(info[7].text[20:])
            # counter
            button = browser.find_element_by_xpath('//*[@id="infh"]/a[1]')
            print(button)
            button.click()


        except:
  
            criaderos_genetic_tree.append(None)
            registros_genetic_tree.append(None)

        print(str(link))
        #numero de hijos

        break

    print(registros_genetic_tree)



    
except requests.exceptions.ConnectionError:

    status_code = "Connection refused"
    print(status_code)



#df = pd.DataFrame({'1':names, a}) 
#df.to_csv('prueba1.csv', index=False, encoding='utf-8')
