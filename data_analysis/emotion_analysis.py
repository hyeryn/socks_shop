from datetime import datetime
import re
import pandas as pd
import urllib.request
from keras_preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
from konlpy.tag import Twitter # 기존의 단어 품사 바꾸는건 안됨
from collections import Counter #jdk에서 제공하는 라이브러리
from keras.preprocessing.text import Tokenizer
from keras.layers import Embedding, Dense, GRU
from keras.models import Sequential
from keras.models import load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

'''
데이터 전처리
'''
okt = Okt()

df = pd.read_csv("C:\sockshopping\crawling\review\양말 리뷰 0312.csv",encoding="cp949")
print(df[:10])
df['label'] = np.select([df.평점 > 4], [1], default=0)
print(df[:10])
df.drop_duplicates(subset=['리뷰'], inplace=True) # reviews 열에서 중복인 내용이 있다면 중복 제거
print('총 샘플의 수 :',len(df))

# 한글과 공백을 제외하고 모두 제거
df['리뷰'] = df['리뷰'].str.replace('[^ㄱ-ㅣ가-힣 ]',"")
df['리뷰'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
train_data = df.dropna(how='any') # Null 값 제거
#print(df.isnull().sum())

k_stopword=pd.read_csv("c:/py_data/korean_stopword.csv")
k_stopword = list(k_stopword['불용어'])
k_stopword.append('어요')

train_data['tokenized'] = train_data['리뷰'].apply(okt.morphs)
train_data['tokenized'] = train_data['tokenized'].apply(lambda x: [item for item in x if item not in k_stopword])

negative_words = np.hstack(train_data[train_data.label == 0]['tokenized'].values)
positive_words = np.hstack(train_data[train_data.label == 1]['tokenized'].values)

negative_word_count = Counter(negative_words)
print(negative_word_count.most_common(20))

positive_word_count = Counter(positive_words)
print(positive_word_count.most_common(20))

fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
text_len = train_data[train_data['label']==1]['tokenized'].map(lambda x: len(x))
ax1.hist(text_len, color='red')
ax1.set_title('Positive Reviews')
ax1.set_xlabel('length of samples')
ax1.set_ylabel('number of samples')
print('긍정 리뷰의 평균 길이 :', np.mean(text_len))

text_len = train_data[train_data['label']==0]['tokenized'].map(lambda x: len(x))
ax2.hist(text_len, color='blue')
ax2.set_title('Negative Reviews')
fig.suptitle('Words in texts')
ax2.set_xlabel('length of samples')
ax2.set_ylabel('number of samples')
print('부정 리뷰의 평균 길이 :', np.mean(text_len))
plt.show()

X_train = train_data['tokenized'].values
y_train = train_data['label'].values

X_train[:3]

y_train[:3]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

print(tokenizer.word_index)

threshold = 2
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)

# 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
# 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
vocab_size = total_cnt - rare_cnt + 2
print('단어 집합의 크기 :',vocab_size)

tokenizer = Tokenizer(vocab_size, oov_token = 'OOV')
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)

print(tokenizer.word_index)

print(X_train[:3])

'''
패딩
'''
print('리뷰의 최대 길이 :',max(len(review) for review in X_train))
print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))
plt.hist([len(review) for review in X_train], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

def below_threshold_len(max_len, nested_list):
  count = 0
  for sentence in nested_list:
    if(len(sentence) <= max_len):
        count = count + 1
  print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (count / len(nested_list))*100))

max_len = 90
below_threshold_len(max_len, X_train)

X_train = pad_sequences(X_train, maxlen = max_len)

X_train.shape

"""# 3. GRU를 이용한 분류"""

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(GRU(128))
model.add(Dense(1, activation='sigmoid'))

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=15, callbacks=[es, mc], batch_size=60, validation_split=0.2)

loaded_model = load_model('best_model.h5')
print("\n 테스트 정확도: %.4f" % (loaded_model.evaluate(X_train, y_train)[1]))

"""# 4. 리뷰 예측해보기"""


def sentiment_predict(new_sentence):
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
    new_sentence = okt.morphs(new_sentence)  # 토큰화
    new_sentence = [word for word in new_sentence if not word in k_stopword]  # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩

    score = float(loaded_model.predict(pad_new))  # 예측
    if (score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))

sentiment_predict('양말 품질이 좋아 여기서 주문합니다 흰색이 없어 아이보리로 주문했는데 교복에 신어도 괜찮을 것 같습니다')
sentiment_predict('짱짱하고 좋아요 다만 좀 얇네요 전 겨울양말을 따로 안 신어서 상관없는데 두꺼운 양말 선호하시는 분들은 참고하시면 좋을 듯합니다 주문한 양말은 서비스로 한 켤레씩 더 주시고 따로 서비스도 더 챙겨주셨어요 감사합니다')
