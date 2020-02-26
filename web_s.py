import requests
import pandas as pd
from bs4 import BeautifulSoup

URL = "http://www1.caballoyrodeo.cl/portal_rodeo/stat/port/genealogia.html?id=10939#gc"
ADD = "http://www1.caballoyrodeo.cl/portal_rodeo/stat/port/genealogia.html"

names = []
criaderos = []
edades = []
colores = []
sexos = []
genetic_tree = []
links_genetic_tree = []

def find_link_name(n,c):

    searcher = soup.find('div',attrs={'class':n }).find('div',attrs={'class':c}).find('a', href=True)
    print(searcher.text)
    #add name and link of father to the list

    if n == 'n4':

        
        searcher = soup.find('div',attrs={'class':n }).find('div',attrs={'class':c}).find('a', href=True)
        print(searcher.text)    
        genetic_tree.append([searcher.text])
        links_genetic_tree.append([ADD+searcher['href']])

    else:

        searcher = soup.find('div',attrs={'class':n }).find('a', attrs={'class':c}).find('a', href=True)
        print(searcher.text)
        genetic_tree.append([searcher.text])
        links_genetic_tree.append([ADD+searcher['href']])


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


    #find father in the html .
    #_1 = soup.find('div',attrs={'class':'n1'}).find('div',attrs={'class':'c1'}).find('a', href=True)
    for n in range(4):
       
            for c in range(16):

                try:

                    find_link_name('n'+(str(n+1)),'c'+(str(c+1)))

                except:

                    pass

    searcher = soup.find('div',attrs={'class':'n4'}).find('div',attrs={'class':'c1'}).find('a', href=True)
    print(searcher.text)

    #request web page entrance of the father genetic tree
    #page_2 = requests.get(ADD+_1['href'])

    
except requests.exceptions.ConnectionError:

    status_code = "Connection refused"
    print(status_code)

#df = pd.DataFrame({'1':name_1 , 'link_1': link_1}) 
#df.to_csv('prueba1.csv', index=False, encoding='utf-8')
