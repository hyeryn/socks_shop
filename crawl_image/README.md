## image_data.py
#### 이미지에서 데이터 추출
- 추출 대상 이미지 : https://sockspresident.cafe24.com/product/SDSC/naver_collection/MW_Collection_list1_01.jpg
- 레퍼런스
1. https://devsmile.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%97%90%EC%84%9C-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EC%B6%94%EC%B6%9C%ED%95%98%EA%B8%B0-1-tesseract (이미지에서 텍스트 추출)
2. https://davey.tistory.com/entry/Python%EC%97%90%EC%84%9C-%EC%9D%B4%EB%AF%B8%EC%A7%80-%ED%8C%8C%EC%9D%BC%EC%9D%84-OCR%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC-%ED%85%8D%EC%8A%A4%ED%8A%B8%EB%A5%BC-%EC%B6%94%EC%B6%9C%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95-pillow-pytesseract-%ED%8C%A8%ED%82%A4%EC%A7%80 (ORC 이용해서 텍스트 추출)
3. https://m.blog.naver.com/os2dr/221814084743 (웹 페이지 대량의 이미지 크롤링)

=> pillow / pytesseract 패키지 설치

![image](https://user-images.githubusercontent.com/57982899/159191522-f87f5b1e-cbce-485f-8a50-a430953486da.png)


<br><br>

## kao_ocr_image_data.py
#### kakao에서 제공하는 광학문자인식 OCR API를 이용
- 레퍼런스
1. https://gimkuku0708.tistory.com/44 (Google Colab으로 OCR해보기)
2. https://developers.kakao.com/docs/latest/ko/vision/dev-guide#ocr (Kakao OCR API)
 
<br><br> 
 
## preprocessing_image_data.py
#### opencv 이미지 전처리 후 pytesseract 로 정보 처리
- 1. color -> grayscale -> binary 후 텍스트 정확도 상승
- 레퍼런스
1. https://turtle-dennis.tistory.com/30?category=843819 (tesseract & opencv를 이용한 OCR 전처리)

![image](https://user-images.githubusercontent.com/57982899/159191555-8e65a6da-413d-40e7-bcb7-a878b9e19a8e.png)

- 2. 색 구분 특정 영역 이미지 추출 (특수문자 추후 처리 필요)
- 문제 해결 중 ..

<br><br>

## preprocessing_image_data.py
#### opencv 특정 영역 인식 (checkbox)
- 레퍼런스
1. https://towardsdatascience.com/checkbox-table-cell-detection-using-opencv-python-332c57d25171 (체크박스 영역 인식)

![image](https://user-images.githubusercontent.com/57982899/159595901-37756fe3-edbf-46e6-a537-68f1dd09fdc0.png)

<br><br>

## draw_image.py
#### 해당 영역과 유사한 영역 찾기
- 레퍼런스
1. https://iagreebut.tistory.com/77 (이미지에서 특정 영역 찾아내기)
2. https://wjh2307.tistory.com/7 (이미지에서 특정 영역 크롭하기)

![image](https://user-images.githubusercontent.com/57982899/159595797-adf2d72d-f85d-4e1a-b7ed-836674be77f2.png)

<br><br>

## image_data_final.py
#### opencv + pytesseract 총 결합
- 1. 이미지 처리 후 글자 추출 (pytesseract + OCR)
- 2. 이미지 해당 영역 비교 후 데이터 추출 (opencv)

![image](https://user-images.githubusercontent.com/57982899/159840012-faaf9baf-715d-46ac-a5f3-aac773632dec.png)

<br><br>



