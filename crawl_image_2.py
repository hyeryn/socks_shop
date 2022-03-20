import urllib.request
from bs4 import BeautifulSoup

# 접근할 페이지 번호
pageNum = 1

# 저장할 이미지 경로 및 이름
imageNum = 0
imageStr = "./crawling/image/sock"

url = "https://smartstore.naver.com/sdsc/products/5033869899"

fp = urllib.request.urlopen(url)
source = fp.read();
fp.close()

soup = BeautifulSoup(source, 'html.parser')
#print(soup)
soup_intro = soup.findAll("div", class_="z7cS6-TO7X")
print(soup_intro)

# 이미지 경로를 받아 로컬에 저장한다.
for i in soup_intro:
    imageNum += 1
    imgURL = i.find("img")["src"]
    urllib.request.urlretrieve(imgURL, imageStr + str(imageNum) + ".jpg")
    print(imgURL)
    print(imageNum)

# while pageNum < 3:
#     url = "https://www.kr.playblackdesert.com/BeautyAlbum?searchType=0&searchText=&categoryCode=0&classType=0,4,8,12,16,20,21,24,25,26,28,31,27,19,23,11,29,17,5&Page="
#     url = url + str(pageNum)
#
#     fp = urllib.request.urlopen(url)
#     source = fp.read();
#     fp.close()
#
#     soup = BeautifulSoup(source, 'html.parser')
#     soup = soup.findAll("p", class_="img_area")
#
#     # 이미지 경로를 받아 로컬에 저장한다.
#     for i in soup:
#         imageNum += 1
#         imgURL = i.find("img")["src"]
#         urllib.request.urlretrieve(imgURL, imageStr + str(imageNum) + ".jpg")
#         print(imgURL)
#         print(imageNum)
#
#     pageNum += 1
