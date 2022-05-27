import pandas as pd
from bs4 import BeautifulSoup
import re 
import requests

#---------------------------------------Fonction pour scrapper les formations en fonction du Rome------------------------------

def handle_rome(rome):

  headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

  url = (f"https://candidat.pole-emploi.fr/formations/recherche?quoi={rome}&range=0-9&tri=0")
  req = requests.get(url, headers)

  soup = BeautifulSoup(req.content, 'html.parser')

  link = []
  link_ref = []
  link_title = []

  for a in soup.find_all('a', href=True, title=True):
   if (re.match(r'^[\/]formations\/detail.*[\d]$', a['href'])):
     link_ref.append('https://candidat.pole-emploi.fr' + a['href'])
     link_title.append(a['title'])

  link = dict(zip(link_title, link_ref))

  return link

#---------------------------------------Fonction pour scrapper les infos utiles sur les formations-----------------------------

def scrapper_formation(url):

  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  result = soup.find( class_='icon-group')
  info = []
  for row in result:
   info.append(row.get_text())

  organisme = info[1].split('\n')
  adresse = info[3].split('\n')
  lien_organisme = result.a.get_text()

  result2 = soup.find(class_='description col-sm-8 col-md-7')
  objectif = result2.get_text().split('\n')
  objectif = objectif[2:]

  result3 = soup.find(class_='t4 title-complementary')
  duree = result3.get_text()

  result4 = soup.find_all('li')
  info3 = []
  for row in result4:
    info3.append(row.get_text())
  prerequis = info3[79].split('\n')

  result5 = soup.find_all('p')
  info4 = []
  for row in result5:
    info4.append(row.get_text())
  financement = info4[12:14]

  adresse_map = adresse[-1].split(' ')


  return organisme[1], lien_organisme, adresse, objectif, duree, prerequis, financement[0], financement[1], adresse_map



