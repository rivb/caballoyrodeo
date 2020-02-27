import requests
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from bs4 import BeautifulSoup

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
    #find name of the horse
    info = soup.find('div',attrs={'class':'info-caballo'}).findAll('dt')
    names.append(info[0].text[8:])
    criaderos.append(info[1].text[10:])
    colores.append(info[2].text[7:])
    edades.append(info[3].text[12:])
    sexos.append(info[5].text[6:])
    registros.append(info[7].text[20:])




    #find father in the html .
    #_1 = soup.find('div',attrs={'class':'n1'}).find('div',attrs={'class':'c1'}).find('a', href=True)

    for n in range(4):
       
            for c in range(16):

                try:

                    find_link_name('n'+(str(n+1)),'c'+(str(c+1)))

                except:

                    pass

    for link in links_genetic_tree:

        try:


            page_2 = requests.get(link)
            soup_2 = BeautifulSoup(page_2.content, 'html.parser')
            info = soup_2.find('div',attrs={'class':'info-caballo'}).findAll('dt')
            criaderos_genetic_tree.append(info[1].text[10:])
            registros_genetic_tree.append(info[7].text[20:])

            # sons count
            break

    
        except:
            print('hi')
            criaderos_genetic_tree.append(None)
            registros_genetic_tree.append(None)



    #request web page entrance of the father genetic tree
    #page_2 = requests.get(ADD+_1['href'])
    print(registros_genetic_tree)



    
except requests.exceptions.ConnectionError:
    status_code = "Connection refused"
    print(status_code)



#df = pd.DataFrame({'1':names, a}) 
#df.to_csv('prueba1.csv', index=False, encoding='utf-8')
