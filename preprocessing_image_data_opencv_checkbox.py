import os
import cv2
import numpy as np

# load image
image_path='C:\sockshopping\crawling\image\example.jpg'
image=cv2.imread(image_path)
cv2.imshow('original',image)

# binarisation
gray_scale=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
th1,img_bin = cv2.threshold(gray_scale,150,225,cv2.THRESH_BINARY)
img_bin=~img_bin
cv2.imshow('test',img_bin)

### selecting min size as 15 pixels
line_min_width = 15
kernal_h = np.ones((1,line_min_width), np.uint8)
kernal_v = np.ones((line_min_width,1), np.uint8)

# apply kernel on image
img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
img_bin_final=img_bin_h|img_bin_v
cv2.imshow('test2',img_bin_final)

_, labels, stats,_ = \
    cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

print("label", labels, "\nstats", stats)

for x,y,w,h,area in stats[2:]:
    rec_img = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    print(rec_img)

#cv2.imshow('test3', rec_img)
cv2.waitKey(0)
cv2.destroyAllWindows()