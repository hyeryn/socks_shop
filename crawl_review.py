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

# 네이버 스마트 스토어 창 열기
url = 'https://smartstore.naver.com/sdsc/products/5033869899' # 크롤링 하고자 하는 제품 페이지
s = Service('C:\sockshopping\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get(url)
time.sleep(2)

date = str(input("저장날짜를 입력하세요: ")) # 파일이름에 들어갈 날짜 입력
stop = int(input("몇 세트 크롤링 할까요?(1-11페이지가 한 세트): "))

next_btn = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
        'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']

review_list = [] #리뷰 리스트
rating_list = [] #평점 리스트
product_option_list = [] #구매자 선택옵션 리스트

count = 0

while count < stop:
    for pagenum in next_btn: # 리뷰 페이지 넘기기
        driver.find_element(By.CSS_SELECTOR, '#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > '+str(pagenum)+'').send_keys(keys.ENTER)
        time.sleep(2)
        for i in range(0,20): # 한 페이지 속 리뷰 20개 하나하나 접근
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # 리뷰가 담긴 div 엘리먼트 모두 찾아서 텍스트 추출해 리스트에 넣기
            review = soup.find_all('div',class_="YEtwtZFLDz")
            review = review[i].text
            review = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",review) # 특수문자, 영어 제거
            review_list.append(review)

            # 평점이 담긴 em 엘리먼트 모두 찾아서 리스트에 넣기
            rating = soup.find_all('em',class_="_15NU42F3kT")
            rating = rating[i].text
            rating_list.append(rating)

            # 구매자 선택옵션이 담긴 div 엘리먼트 모두 찾아서 텍스트 추출해 리스트에 넣기(옵션 안나오는 경우는 예외처리)
            while True:
                try:
                    product_option = soup.find_all('div', class_="_38yk3GGMZq")
                    product_option = product_option[i].text
                    product_option = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]', "", product_option)
                    product_option_list.append(product_option)
                    break
                except Exception as error:
                    print("#####################################################################")
                    print(error)
                    product_option_list.append("옵션 찾을 수 없음 :: " + str(pagenum) + "페이지, " + str(i + 1) + "번째")
                    print("옵션 찾을 수 없음 :: " + str(pagenum) + "페이지, " + str(i + 1) + "번째")
                    print("#####################################################################\n")
                    break

    count = count + 1

'''
csv 파일로 저장하기
'''
socks = pd.DataFrame({'평점':rating_list, '선택옵션':product_option_list,'리뷰':review_list})
while True:
    try:
        socks.to_csv("c:/sockshopping/crawling/review/양말 리뷰 " + date + '.csv', encoding='cp949')
        break
    except Exception as e: # 인코딩 에러 예외처리
        error_character = str(e).split(' ')[5].replace('\'', '')
        socks = socks.replace(u'{}'.format(error_character), u'', regex=True)

# 확인용 print(len(review_list))