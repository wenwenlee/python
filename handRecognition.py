# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:18:09 2017

@author: ranarangganguowa
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 18:03:09 2017

@author: ranarangganguowa
"""

import cv2
import numpy as np
import math
#from matplotlib import pyplot as plt

def threshImg(crop_img):

    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

     #applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    #blurred = cv2.bilateralFilter(grey,9,35,35)
     # thresholdin: Otsu's Binarization method
    _, thresh = cv2.threshold(blurred, 227, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                               
    return (blurred,thresh)
    
    
def getCnt(thresh):
    
     (version, _, _) = cv2.__version__.split('.')

     if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     elif version == '2':
        contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)
               
     cnt = max(contours, key = lambda x: cv2.contourArea(x))
     #return contours
     return (contours,cnt)
    
def getHull(cnt):
    
     # create bounding rectangle around the contour (can skip below two lines)
     x, y, w, h = cv2.boundingRect(cnt)
     cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

    # finding convex hull
     hull = cv2.convexHull(cnt)
     
     return hull
     
     
def gestureDection(crop_img,cnt,thresh):
#    count_defects = gestureDection(crop_img,cnt,thresh)
  # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)
    
      # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh, contours, -1, (0, 255, 0), 3)
    
    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0,0,255], -1)

    return count_defects       
 
def action(cnt):
    
    cv2.putText(img,"This is "+str(count_defects),(5,100),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
    return img

cap = cv2.VideoCapture(0)
while(1):
    # read image

    ret, img = cap.read()
     # get hand data from the rectangle sub window on the screen
    cv2.rectangle(img, (100,100), (400,400), (0,255,0),0)
    crop_img = img[100:400, 100:400]
    
    blurred,thresh = threshImg(crop_img)
    contours,cnt = getCnt(thresh)
    hull = getHull(cnt)

    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)
    
    cv2.imshow("drawing", drawing) 
    
    cv2.drawContours(crop_img, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(crop_img, [hull], 0,(0, 0, 255), 0)
    
    cv2.imshow("crop_img", crop_img)
    
    count_defects = gestureDection(crop_img,cnt,thresh)

    img = action(cnt)
    #show appropriate images in windows
    cv2.imshow('img', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
