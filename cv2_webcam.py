import cv2
import time  
  
vid = cv2.VideoCapture(0)

total_time=0
total_frames=0

for i in range(200):

    start=time.time()
    ret, frame = vid.read()
    end=time.time()
    total_time+=(end-start)
    total_frames+=1
    #print(end-start)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)  

print(total_frames)
print(total_time)
print('avg', total_frames/total_time)

vid.release()
cv2.destroyAllWindows()