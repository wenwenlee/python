# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import numpy as np
#import numpy as np
import cv2
import time
import datetime

cap = cv2.VideoCapture(0)
#time.sleep(0.25)
#firstframe = None
#ret2, firstframe = cap.read()
#firstframe = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
#firstframe = cv2.GaussianBlur(firstframe,(21,21),0)
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
time.sleep(10)
while(True):
    # Capture frame-by-frame
    tiestamp = datetime.datetime.now()
    ret, frame = cap.read()
    text = "unoccupied"
    if not ret:
        break
    

    # Our operations on the frame come here
   # gray = cv2.resize(frame,width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    if avg is None:
        avg = gray.copy().astype("float")
        continue
    cv2.accumulateWeighted(gray,avg,0.5)
    # Display the resulting frame
    cv2.imshow('frame',gray)
    #if firstframe is None:
       # firstframe = gray
       # continue
  #  cv2.imshow('first',firstframe)
    #frameDelta = cv2.absdiff(firstframe,gray)
    frameDelta = cv2.absdiff(gray,cv2.convertScaleAbs(avg))
   # cv2.imshow('first2',frameDelta)
    thresh = cv2.threshold(frameDelta, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow('thresh',thresh)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:] 
  #  cv2.imshow('thresh2',thresh.copy())
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 500:
           continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('found',frame)
        text = "Occupied"
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    #if text == "Occupied":
      #  if (timestamp-lastUploaded).second>=2:
           # motionCounter+=1
            #if motionCounter>=23:
                
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
