import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import csv
class Hero:
    def __init__(self, name="None",link="None",universe="None",other_aliases="None",
                education="None",place_of_origin="None",identity="None",known_relatives="None"):
        self.name = name
        self.link = link
        self.universe = universe
        self.other_aliases = other_aliases
        self.education = education
        self.place_of_origin = place_of_origin
        self.identity = identity
        self.known_relatives = known_relatives
    def _to_dict(self):
        dic = {}
        
        dic['name'] = self.name
        dic['link'] = self.link
        dic['universe'] = self.universe
        dic['other_aliases'] = self.other_aliases
        dic['education'] = self.education
        dic['place_of_origin'] = self.place_of_origin
        dic['identity'] = self.identity
        dic['known_relatives'] = self.known_relatives
        return dic

with open("res.csv", "w", newline="") as file:
    attrs = []
    for attribute in dir(Hero()):
        if attribute[0] != '_':
            attrs.append(attribute)
    writer = csv.DictWriter(file, delimiter=',', fieldnames=attrs)
    writer.writeheader()

shortUrl = 'https://www.marvel.com'
url = 'https://www.marvel.com/characters' # url для второй страницы'

options = webdriver.ChromeOptions()
chromedriver = 'C:/data/files/chromedriver_win32/chromedriver.exe'
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver,chrome_options=options )
links =[]
browser.get(url)
k=1
while True:
    num = 0
    while k!=num:
        try:
            active = browser.find_element_by_class_name("pagination__item_active")
            active = int(active.find_element_by_tag_name("span").text)
            num = active
        except: 
            num = 0
            continue

    requiredHtml = browser.page_source
    soup = BeautifulSoup(requiredHtml)
    full = soup.find('div',{'class':'full-content'})
    elems = full.find_all('div',{'class':"mvl-card mvl-card--explore"})
    for elem in elems:
        link = elem.find('a',{'class':'explore__link'}).get('href')
        if link not in links:
            links.append(shortUrl+link)
    try:
        Button = browser.find_element_by_class_name('pagination__item-nav-next')
        Button.click()
    except:
        break
    k+=1


# for link in links:
#     print(link)
# print(k)
# print(len(links))

k = 0
for link in links:
    browser.get(link)
    requiredHtml = browser.page_source
    soup = BeautifulSoup(requiredHtml)
    properties = soup.select(".railBioInfoItem__label")
    values = soup.select(".railBioLinks li")
    hero = Hero()

    for i in range(len(properties)):
        setattr(hero, properties[i].text.lower().replace(" ","_"), values[i].text.strip())
    hero.name = soup.select(".masthead__headline")[0].text.strip()
    hero.link = link
    

    with open("res.csv", "a", encoding='utf-8',newline="") as file:
        attrs = []
        for attribute in dir(hero):
            if attribute[0] != '_':
                attrs.append(attribute)
        writer = csv.DictWriter(file, delimiter=',', fieldnames=attrs)
        writer.writerow(hero._to_dict())
    k+=1

print(len(links))

