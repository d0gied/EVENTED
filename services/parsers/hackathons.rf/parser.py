import requests

import time
import schedule
from bs4 import BeautifulSoup
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


from fake_useragent import UserAgent
# from random_user_agent.user_agent import UserAgent

LINK = 'https://www.xn--80aa3anexr8c.xn--p1ai/'

class Hackathon(BaseModel):
    title: str
    image: str
    date_time: str
    stack: str
    place: str
    registration: str
    link: str

def parse_hackathons():
    agent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    browser = webdriver.Chrome(options=options)
    browser.get(LINK)

    time.sleep(5)

    soup = BeautifulSoup(browser.page_source, "html.parser")

    allHacks = soup.find_all('a', class_='js-product-link')
    for hack in allHacks:
        hackLink = hack['href']
        if hack.find('div', class_='t776__bgimg t-bgimg js-product-img') is None:
            break
        hackImage = hack.find('div', class_='t776__bgimg t-bgimg js-product-img').get('data-original')
        
        hackTitleCol = hack.find('div', class_='t776__title t-name t-name_xl js-product-name')
        hackTitleBig = hack.find('div', class_='t776__title t-name t-name_md js-product-name')
        if hackTitleCol is None and hackTitleBig is None:
            break
        
        hackTitle = (hackTitleCol if hackTitleCol is not None else hackTitleBig)
        if hackTitle.find('div') is None:
            break
        hackTitle = hackTitle.find('div').text
        
        if hack.find('div', class_='t776__descr t-descr t-descr_xxs') is None:
            break
        hackText = hack.find('div', class_='t776__descr t-descr t-descr_xxs').text
        hackPlace = hackText.split('Хакатон')[0]
        hackDate = hackText.split('Хакатон: ')[1].split('Регистрация')[0]
        hackReg = hackText.split('Регистрация: ')[1].split('Организатор')[0]
        hackStack = hackText.split('Технологический фокус: ')[1].split('Призовой фонд')[0]
        
        print(hack)
        
    browser.quit()

schedule.every().day.at("09:00").do(parse_hackathons)
        
while True:
    schedule.run_pending()