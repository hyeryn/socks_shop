# socks_shop
### 네이버 스마트 스토어 제품 크롤링
<br>

-----

## crawl_review_all.py
#### 전체 데이터 크롤링
=> selenium / 크롬 드라이버 설치 (https://chancoding.tistory.com/136)
<br> <br>

## crawl_review.py
#### 특정 데이터 태그 크롤링
- 레퍼런스
1. https://blog.naver.com/yk02061/222228280467 (네이버 스토어팜 리뷰 크롤링)
2. https://github.com/heemang2/PycharmProjects/blob/42de0b3b6b1c67fe08ada498cbfe8393462d9290/pythonProject/getreivewtest456.py (네이버 스마트스토어 리뷰 가져오기)
3. https://blog.naver.com/angela_id/222608584687 (BeautifulSoup 데이터 크롤링)
<br><br>

## wordcloud.py
#### csv 파일 리뷰 데이터 전처리 후 워드클라우드로 데이터 시각화
- 1. 명사만 추출해 만든 워드 클라우드
- 2. 형태소 단위로 추출해 만든 워드 클라우드
- 레퍼런스
1. https://blog.naver.com/yk02061/222262810714 (크롤링 후 전처리와 워드 클라우드)
<br><br>

## emotion_analysis.py
- 레퍼런스
1. https://wikidocs.net/94600 (네이버 쇼핑 리뷰 감성 분류하기)
<br><br>

## image_data.py
#### 이미지에서 데이터 추출
- 추출 대상 이미지 : https://sockspresident.cafe24.com/product/SDSC/naver_collection/MW_Collection_list1_01.jpg
- 레퍼런스
1. https://devsmile.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%97%90%EC%84%9C-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0-1-tesseract (이미지에서 텍스트 추출)
2. https://davey.tistory.com/entry/Python%EC%97%90%EC%84%9C-%EC%9D%B4%EB%AF%B8%EC%A7%80-%ED%8C%8C%EC%9D%BC%EC%9D%84-OCR%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-%ED%85%8D%EC%8A%A4%ED%8A%B8%EB%A5%BC-%EC%B6%94%EC%B6%9C%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-pillow-pytesseract-%ED%8C%A8%ED%82%A4%EC%A7%80 (ORC 이용해서 텍스트 추출)
3. https://m.blog.naver.com/os2dr/221814084743 (웹 페이지 대량의 이미지 크롤링)
<br>
=> pillow / pytesseract 패키지 설치
<br>

