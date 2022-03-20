from datetime import datetime
import pandas as pd
import re
from konlpy.tag import Okt
from konlpy.tag import Twitter # 기존의 단어 품사 바꾸는건 안됨
from collections import Counter #jdk에서 제공하는 라이브러리
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

'''
데이터 전처리
'''

df = pd.read_csv("c:/py_data/양말 리뷰0309.csv",encoding="cp949") # csv 파일 불러오기

content_all= ''
for i in range(len(df['리뷰'])): # 리뷰 갯수만큼 반복해서 content_all 변수에 리뷰 넣기
    content_all = content_all + ' ' + df['리뷰'].loc[i]

content_all = re.sub('[^ㄱ-ㅣ가-힣 ]',"",content_all) #형태소 추출을 위해 한글 이외의 것 제거
content_all = str(content_all)

okt = Okt() #형태소 분석 툴 Konlpy의 Okt 모듈을 이용
nouns_txt = okt.nouns(content_all) #명사 단위로 쪼개서 nouns_txt에 담기
#morphs_txt = okt.morphs(content_all) # 형태소 단위로 쪼개서 nouns_txt에 담기

count = Counter(nouns_txt) #nouns_txt에서 nouns 개수를 세서 몇개인지 넣어라
#count = Counter(morphs_txt)
rank_text = count.most_common() #내림차순 정렬

rank_text = dict(rank_text)
count_len = 10
temp_dic={}
#items를 안쓰면 키,벨류 값 모두 나오지 않는다.
for key, value in rank_text.items():
    if value > count_len: #10번 미만으로 언급된 단어 제외
        temp_dic[key] = value
rank_text = temp_dic

#불용어 제거하기
k_stopword=pd.read_csv("c:/py_data/korean_stopword.csv")
k_stopword = list(k_stopword['불용어'])
k_stopword.append('어요')

temp_dic = {}
for key, value in rank_text.items():
    if key not in k_stopword: #stopword가 아닌(not in) 키값만 다시 모아서
        temp_dic[key] = value

[temp_dic.pop(key) for key in ['양말', '켤레']] # 자주 나오는데 분석에 필요없는 단어 지우기
temp_dic_sort_by_the_key = dict(sorted(temp_dic.items(), key=lambda x: x[0], reverse=True))
print(temp_dic_sort_by_the_key) # 자주 나오는 순으로 단어 출력하라고 한건데 뭔가 이상하네요;;



'''
워드클라우드 이미지 만들고 저장하기
'''

img_path = 'c:/py_data/sock.png'
flower_mask = np.array(Image.open(img_path))
wordcloud = WordCloud(font_path="c:/Windows/Fonts/malgun.ttf",
                     colormap= 'Dark2',
                      background_color="white", mask=flower_mask)

date = datetime.now()
time = date.strftime('%Y-%m-%d_%H.%M.%S')

wc = wordcloud.generate_from_frequencies(temp_dic)
plt.figure(figsize=(8,15))
plt.imshow(wc)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('C:/py_data/wordcloud/워드클라우드' + time + ".png")
plt.show()