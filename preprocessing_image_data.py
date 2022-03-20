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
matchers = ['사이즈', '소재', '세탁방법', '두께감', '계설감', '계절감']
data = [s for s in data_table if any(xs in s for xs in matchers)]
print(data)
print("=================")

# 데이터프레임 생성
data2 = []

for i in range(len(data)):
    data2.append(data[i].split())

print(data2) # 카테고리별 분류
print("=================")

size = 0
textile = 1
wash = 2
thickness = 3
weather = 4
size2 = 5
textile2 = 6
wash2 = 7
thickness2 = 8
weather2 = 9

# review = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",review) # 특수문자, 영어 제거

size_list = []
textile_list = []
wash_list = []
thickness_list = []
weather_list = []

size_list.append(data2[size][1])
for i in range(len(data2[textile])-1):
    textile_list.append(data2[textile][i+1])
for i in range(len(data2[wash])-1):
    wash_list.append(data2[wash][i+1])
for i in range(len(data2[thickness])-1):
    thickness_list.append(data2[thickness][i+1])
for i in range(len(data2[weather])-1):
    weather_list.append(data2[weather][i+1])
size_list.append(data2[size2][1])
for i in range(len(data2[textile2]) - 1):
    textile_list.append(data2[textile2][i + 1])
for i in range(len(data2[wash2]) - 1):
    wash_list.append(data2[wash2][i + 1])
for i in range(len(data2[thickness2]) - 1):
    thickness_list.append(data2[thickness2][i + 1])
for i in range(len(data2[weather2]) - 1):
    weather_list.append(data2[weather2][i + 1])

print(size_list, textile_list, wash_list, thickness_list, weather_list)

import pandas as pd
# socks = pd.DataFrame({'사이즈':size_list, '소재':textile_list,'세탁방법':wash_list,
#                       '두께감':thickness_list, '계절감':weather_list})