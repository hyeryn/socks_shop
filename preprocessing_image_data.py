import cv2
from matplotlib import pyplot as plt
import re

path = 'C:\sockshopping\crawling\image'
image_sock = cv2.imread(path+"\sock9.jpg", cv2.IMREAD_COLOR)
plt.figure(figsize=[15,5])
plt.imshow(image_sock)
plt.xlabel("Original", fontsize=15)
#plt.show()
#print(image_sock.shape)

# 1) color -> grayscale 흑백화
def gray_scale(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return result

image_sock_gray = gray_scale(image_sock)

plt.figure(figsize=[20,7])
plt.subplot(1, 2, 1)
plt.imshow(image_sock)
plt.xlabel("Original", fontsize=15)
#print("Image_sock shape: ", image_sock.shape)
plt.subplot(1, 2, 2)
plt.imshow(image_sock_gray)
plt.xlabel("GrayScale", fontsize=15)
#print("Grayscale_sock shape: ", image_sock_gray.shape)
#plt.show()

# 2) grayscale -> binary 이진화
def image_threshold(image):
    result = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return result

image_sock_binary = image_threshold(image_sock_gray)

plt.figure(figsize=[20,7])
plt.subplot(1, 2, 1)
plt.imshow(image_sock_gray)
plt.xlabel("GrayScale", fontsize=15)
#print("Grayscale_sock shape: ", image_sock_gray.shape)
plt.subplot(1, 2, 2)
plt.imshow(image_sock_binary)
plt.xlabel("Binary", fontsize=15)
#print("Binary_sock shape: ", image_sock_binary.shape)
#plt.show()
#print(image_sock_binary)

# 3) remove noise
def remove_noise(image, kernel_size=5): # blur 5 / 21 / 51 (점점 뭉개짐)
    result = cv2.medianBlur(image, ksize=kernel_size)
    return result

image_sock_rm = remove_noise(image_sock)

plt.figure(figsize=[20,7])
plt.subplot(1, 2, 1)
plt.imshow(image_sock)
plt.xlabel("Original", fontsize=15)
plt.subplot(1, 2, 2)
plt.imshow(image_sock_rm)
plt.xlabel("Noise removed", fontsize=15)
# plt.show()


# tesseract 이미지 인식
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# config = ('-l kor --oem 3 --psm 4')
# image_sock_gray = cv2.imread('C:\sockshopping\crawling\image\sock9.jpg',
#                              cv2.IMREAD_GRAYSCALE)
# image_data = pytesseract.image_to_string(image_sock_gray, config=config)
image_data = pytesseract.image_to_string(image_sock_binary,
                                          lang='kor', config='-c preserve_interword_spaces=1 --psm 4')

print(image_data)
print("=================")

# 사용 데이터 추출
data_table = re.split('\n', image_data)
# 카테고리 설정
matchers = ['여성','남성', '남여공용', '01', '07', '13', '19', '사이즈', '소재', '세탁방법', '두께감', '계설감', '계절감']
data = [s for s in data_table if any(xs in s for xs in matchers)]
#data = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",data)
print(data)
print("=================")

# 데이터프레임 생성
data2 = []

for i in range(len(data)):
    data2.append(data[i].split())

print(data2) # 카테고리별 분류
print("=================")

'''
# 카테고리별 인덱스 부여
name = 0
color = 1
size = 2
textile = 3
wash = 4
thickness = 5
weather = 6
'''

# review = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",review) # 특수문자, 영어 제거

name_data = ''
color_data = ''
size_data = ''
textile_data = ''
wash_data = ''
thickness_data = ''
weather_data = ''

# 각 데이터 정제 완료 리스트
name_list = []
color_list = []
size_list = []
textile_list = []
wash_list = []
thickness_list = []
weather_list = []

'''
데이터 저장
'''

index = 0

# 1 상품명
for i in range(len(data2[index])):
    name_data += data2[index][i]
print(index, name_data)
index += 1
name_list.append(name_data)

# 2 색상명
while 1: # 맨 앞 문자가 숫자인지 판별
    if data2[index][0][:1].isdigit():
        if data2[index][0].startswith(('01.', '07.', '13.', '19.')):
            for i in range(len(data2[index])):
                color_data += data2[index][i]
            #print(index, color_data)
            index += 1
        else:
            index += 1
    else:
        break
print(index, color_data)
color_list.append(color_data)

# 3 사이즈
while 1:
    if data2[index][0].startswith(('사이즈')):
        size_data = data2[index][1]
        break
    else:
        index += 1
print(index, size_data) # 데이터 정제 필요
size_list.append(size_data)

# 4 소재
while 1:
    if data2[index][0].startswith(('소재')):
        for i in range(len(data2[index])-1):
            textile_data += data2[index][i+1]
        break
    else:
        index += 1
print(index, textile_data)
textile_list.append(textile_data)

# 5 세탁
while 1:
    if data2[index][0].startswith(('세탁')):
        for i in range(len(data2[index])-1):
            wash_data += data2[index][i+1]
        break
    else:
        index += 1
print(index, wash_data)
wash_list.append(wash_data)

# 6 두께감 -> 데이터 정제 필요
while 1:
    if data2[index][0].startswith(('두')):
        for i in range(len(data2[index])-1):
            thickness_data += data2[index][i+1]
        break
    else:
        index += 1
print(index, thickness_data)
thickness_list.append(thickness_data)

# 7 계절감 -> 데이터 정제 필요
while 1:
    if data2[index][0].startswith(('계')):
        for i in range(len(data2[index])-1):
            weather_data += data2[index][i+1]
        break
    else:
        index += 1
print(index, weather_data)
weather_list.append(weather_data)

index += 1
print(data2[index][0])
name_data = ''
color_data = ''
size_data = ''
textile_data = ''
wash_data = ''
thickness_data = ''
weather_data = ''

# 데이터 여러번 저장 필요
if data2[index][0].startswith(('여성', '남성', '남여')):

    # 1 상품명
    for i in range(len(data2[index])):
        name_data += data2[index][i]
    print(index, name_data)
    index += 1
    name_list.append(name_data)

    # 2 색상명
    while 1:  # 맨 앞 문자가 숫자인지 판별
        if data2[index][0][:1].isdigit():
            if data2[index][0].startswith(('01.', '07.', '13.', '19.')):
                for i in range(len(data2[index])):
                    color_data += data2[index][i]
                # print(index, color_data)
                index += 1
            else:
                index += 1
        else:
            break
    print(index, color_data)
    color_list.append(color_data)

    # 3 사이즈
    while 1:
        if data2[index][0].startswith(('사이즈')):
            size_data = data2[index][1]
            break
        else:
            index += 1
    print(index, size_data)  # 데이터 정제 필요
    size_list.append(size_data)

    # 4 소재
    while 1:
        if data2[index][0].startswith(('소재')):
            for i in range(len(data2[index]) - 1):
                textile_data += data2[index][i + 1]
            break
        else:
            index += 1
    print(index, textile_data)
    textile_list.append(textile_data)

    # 5 세탁
    while 1:
        if data2[index][0].startswith(('세탁')):
            for i in range(len(data2[index]) - 1):
                wash_data += data2[index][i + 1]
            break
        else:
            index += 1
    print(index, wash_data)
    wash_list.append(wash_data)

    # 6 두께감 -> 데이터 정제 필요
    while 1:
        if data2[index][0].startswith(('두')):
            for i in range(len(data2[index]) - 1):
                thickness_data += data2[index][i + 1]
            break
        else:
            index += 1
    print(index, thickness_data)
    thickness_list.append(thickness_data)

    # 7 계절감 -> 데이터 정제 필요
    while 1:
        if data2[index][0].startswith(('계')):
            for i in range(len(data2[index]) - 1):
                weather_data += data2[index][i + 1]
            break
        else:
            index += 1
    print(index, weather_data)
    weather_list.append(weather_data)

# csv 파일 변환 전 최종 점검
print(name_list, color_list, size_list, textile_list, wash_list, thickness_list, weather_list)

# csv 파일 저장
import pandas as pd
socks = pd.DataFrame({'상품명':name_list, '색상':color_list, '사이즈':size_list, '소재':textile_list,
                      '세탁방법':wash_list,'두께감':thickness_list, '계절감':weather_list})
date = str(input("저장날짜를 입력하세요: ")) # 파일이름에 들어갈 날짜 입력
while True:
    try:
        socks.to_csv("c:/sockshopping/crawling/data/양말 정보 " + date + '.csv', encoding='cp949')
        break
    except Exception as e: # 인코딩 에러 예외처리
        error_character = str(e).split(' ')[5].replace('\'', '')
        socks = socks.replace(u'{}'.format(error_character), u'', regex=True)