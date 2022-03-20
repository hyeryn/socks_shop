from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import urllib.request

import pandas as pd
from tqdm.notebook import tqdm
import time
import re
import sys
from selenium.webdriver.common.keys import Keys #키보드 키를 제어하는 라이브러리

keys = Keys() #키보드 키를 제어

url = 'https://smartstore.naver.com/sdsc/products/5033869899' # 크롤링 하고자 하는 제품 페이지
s = Service('C:\sockshopping\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get(url)
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, '#INTRODUCE')
time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
image = soup.find_all('div',class_='se-component se-image se-l-default')
print(image)

# 저장할 이미지 경로 및 이름
imageNum = 0
imageStr = "./crawling/image/sock"

# 이미지 경로를 받아 로컬에 저장한다.
for i in image:
    imageNum += 1
    imgURL = i.find("img")["data-src"]
    urllib.request.urlretrieve(imgURL, imageStr + str(imageNum) + ".jpg")
    print(imgURL)
    print(imageNum)