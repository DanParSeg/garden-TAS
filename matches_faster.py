import cv2
import numpy as np
import time

image = cv2.imread('test.png', cv2.IMREAD_COLOR)
template = cv2.imread('4.png', cv2.IMREAD_COLOR)

h, w = template.shape[:2]

method = cv2.TM_CCOEFF_NORMED

threshold = 0.90

res = cv2.matchTemplate(image, template, method)

# fake out max_val for first run through loop
max_val = 1
while max_val > threshold:
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val > threshold:
        print(max_val)
        res[max_loc[1]-h//2:max_loc[1]+h//2+1, max_loc[0]-w//2:max_loc[0]+w//2+1] = 0   
        image = cv2.rectangle(image,(max_loc[0],max_loc[1]), (max_loc[0]+w+1, max_loc[1]+h+1), (0,255,0) )

cv2.imshow('output.png', image)
cv2.waitKey(0)

