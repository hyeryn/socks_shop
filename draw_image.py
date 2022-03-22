import cv2
import numpy as np

img_rgb = cv2.imread('C:\sockshopping\crawling\image\example2.jpg')
template = cv2.imread('C:\sockshopping\crawling\image\example2_template.jpg')
h, w = template.shape[:-1]
h_all, w_all = img_rgb.shape[:-1]
print(h_all, w_all)

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .95
loc = np.where(res >= threshold)

thick = ['얇음', '보통', '도톰', '두툼']
weather = ['봄', '여름', '가을', '겨울']

thick_row = 27
weather_row = 76
column = [170, 300, 435, 565]

thick_list = []
weather_list = []

for pt in zip(*loc[::-1]):  # Switch collumns and rows
    print(pt)
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    if (pt[1] >= (thick_row - 5) and pt[1] <= (thick_row + 5)):
        for i in range(len(column)):
            if (pt[0]>=(column[i]-5) and pt[0]<=(column[i]+5)):
                thick_list.append(thick[i])
    else:
        for i in range(len(column)):
            if (pt[0]>=(column[i]-5) and pt[0]<=(column[i]+5)):
                weather_list.append(weather[i])

cv2.imshow('img',img_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(thick_list, weather_list)
