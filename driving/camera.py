#setting up the camera module
import cv2
import numpy as np



def find_lane(frame,lane_segments):
    left_lane_edge=-1
    right_lane_edge=-1
    
    for x in range(0,640,20):
        cur_shade=np.mean(frame[450:480,x:x+lane_segments])
        if cur_shade>220:
            left_lane_edge=x
            break
        
    for x in range(640,0,-20):
        cur_shade=np.mean(frame[450:480,x-lane_segments:x])
        if cur_shade>220:
            right_lane_edge=x
            break
        
        
    
    lane_area= (left_lane_edge,right_lane_edge)
    print("lane:",lane_area,"\n")
    return lane_area






def connect_camera():  
    vid = cv2.VideoCapture(0)

    if vid is None:
        print('could not find a camera\n exitting safely...')
        exit()
    else:
        for i in range(10):    
            ret, frame = vid.read()
    
    return vid

def shut_camera(vid):
    vid.release()
    cv2.destroyAllWindows()
    