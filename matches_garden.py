import cv2
import numpy as np

def next_match(large_image, small_image, method):
    result = cv2.matchTemplate(small_image, large_image, method)

    # We want the minimum squared difference
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    MPx,MPy = mnLoc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),-1)

    return large_image,(MPx,MPy,MPx+tcols,MPy+trows)

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
small_image = cv2.imread('4.png')
large_image = cv2.imread('test.png')
original=large_image.copy()

matches=[]
for i in range(100):
    large_image,m=next_match(large_image,small_image,method)
    matches.append(m)

# Display the original image with the rectangle around the match.
cv2.imshow('output',large_image)
cv2.imshow('original', original)

# The image is only displayed if we call this
cv2.waitKey(0)
