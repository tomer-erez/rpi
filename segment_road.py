import cv2
import time  
import numpy as np
vid = cv2.VideoCapture(0)
# resoloution is 640x480
width=640
height=480
while True:

    ret, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    ret,thresh = cv2.threshold(frame,175,255,cv2.THRESH_BINARY)

    cv2.imshow('frame', thresh)
    cv2.waitKey(1)
    
    

vid.release()
cv2.destroyAllWindows()