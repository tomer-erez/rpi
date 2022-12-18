#the whole driving app
import numpy as np
from time import sleep






from camera import *




#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import pigpio
# 18 is pin 6
servo_pin = 18
pwm = pigpio.pi()
base_forward_direction=1500
from servo import connect_servo,shut_servo,steer,angle_to_pulse,find_steering_angle







import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
left=26
right=22
winker_state=0
from winker import wink,led_on,led_off,shut_winker,connect_winker


      
        
        
        
        
        
in1 = 17
in2 = 27
en_a = 4
#percentage of motor speed
starting_Speed=70
driving_speed=60
from l298n import start_driving,change_speed,connect_l298n,shut_l298n



 
    
    
    
    
    
    
    
vid=connect_camera()    
connect_servo()
connect_winker(GPIO,left,right)
connect_l298n(GPIO)
q=start_driving(GPIO,starting_Speed)
sleep(4)
 #after starting the car, we need less force to keep it moving at a normal speed
q=change_speed(GPIO,driving_speed,q)


for i in range(5):
    ret, frame = vid.read()

no_lane_sequence=0
lane_segments=20
for i in range(1000):
    ret, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    ret,thresh = cv2.threshold(frame,155,255,cv2.THRESH_BINARY)
    #cv2.imshow('threshed_img', thresh)
    #cv2.waitKey(1)
    lane_area=find_lane(thresh,lane_segments)
    
    
    
    if lane_area==(-1,-1):
        no_lane_sequence+=1
        print("did not find a lane in this frame")
        if no_lane_sequence>=10:
            print("did not find a lane in 10 straight frames, exitting...")
            break
        else:
            continue
    else:
        no_lane_sequence=0
    
    
    
    
    angle=steer(lane_area,winker_state,pwm,servo_pin)
    
    winker_state=wink(angle,winker_state,left,right,GPIO)
    
   
    
    
    
    
    
shut_l298n(GPIO)
shut_servo()
shut_camera(vid)
shut_winker(GPIO,left,right)
GPIO.cleanup()
exit()