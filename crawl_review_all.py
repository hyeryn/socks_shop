from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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

date = str(input("저장날짜를 입력하세요: "))
stop = int(input("몇 세트 크롤링 할까요?(1-11페이지가 한 세트): "))

next_btn = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
        'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']
review_list = []

count = 0

while count < stop:
    for pagenum in next_btn:
        driver.find_element(By.CSS_SELECTOR, '#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > '+str(pagenum)+'').send_keys(keys.ENTER)
        time.sleep(2)
        for i in range(0,20):
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            review = soup.find_all('div',class_='_1-CNpGwOcC')
            review = review[i].text
            review = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",review)
            review_list.append(review)
    count = count + 1

socks = pd.DataFrame({'리뷰':review_list})
socks.to_csv("c:/sockshopping/crawling/review/양말 리뷰 전체 " + date + '.csv', encoding='cp949')

print(len(review_list))