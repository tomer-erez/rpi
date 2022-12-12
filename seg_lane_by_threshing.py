import cv2
import numpy as np
#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
GPIO.cleanup()
import pigpio
import time
from math import atan,pi
servo = 18
# 18 is pin 6 outside
# two more connections are needed: voltage and ground.
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
base_forward_direction=1500
pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;
time.sleep( 1 )

''' 
pulse=(5000/109)*(angle+32.7)
angle=-32.7+(0.0218)*pulse
'''
# resoloution is 640x480
vid = cv2.VideoCapture(0)
width=640
height=480
cam_span_width=12# camera sees 12 centimeters at 7 centimeter away from chassis
pixel_width=cam_span_width/width
width_strip=40
height_strip=40
vertical_cam_distance=7 #cam starts seeing 7cm away in horizontal distance

def shutdowncam():
    vid.release()
    cv2.destroyAllWindows()
    
def shut_down_servo():
    pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;
    time.sleep( 1 )
    pwm.set_PWM_dutycycle( servo, 0 )
    pwm.set_PWM_frequency( servo, 0 )
    GPIO.cleanup()
    exit()
    
def find_lane(frame):
    '''
    gets a frame and returns the left edge of the lane, right edge of the lane as list
    '''
    for x in range(0,640,width_strip):
        left_lane_edge=-1
        right_lane_edge=-1
        cur_shade=np.mean(frame[440:480,x:x+width_strip])
        if cur_shade>200:
            left_lane_edge=x
            break
    for x in range(640,0,-width_strip):
        cur_shade=np.mean(frame[440:480,x-width_strip:x])
        if cur_shade>200:
            right_lane_edge=x
            
            break
    print("lane",left_lane_edge,right_lane_edge,"\n")
    return (left_lane_edge,right_lane_edge)

def find_steering_angle(lane_area):
    width=640
    cam_span_width=12# camera sees 12 centimeters at 7 centimeter away from chassis
    pixel_width=cam_span_width/width
    vertical_cam_distance=7
    
    center_lane=(lane_area[0]+lane_area[1])//2
    if center_lane in range(315,325):
        return 0
    width_distance=(320-center_lane)*pixel_width
    angle=atan(width_distance/vertical_cam_distance)*180/pi
    print("steering_angle=", angle)

    return angle

def angle_to_pulse(angle):
    pulse=(5000/109)*(angle+32.7)
    if pulse<500:
        pulse=500
    if pulse>2500:
        pulse=2500
    return int(pulse)


def steer(lane_area):
    angle=find_steering_angle(lane_area)
    pulse=angle_to_pulse(angle)
    pwm.set_servo_pulsewidth( servo, pulse )

for i in range(10):    
    ret, frame = vid.read()
    
for i in range(500):
    ret, frame = vid.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    ret,thresh = cv2.threshold(frame,160,255,cv2.THRESH_BINARY)
    lane_area=find_lane(thresh)
    
    if lane_area==(-1,-1):
        print("why -1 -1")
        continue

    steer(lane_area)
    cv2.imshow('threshed_img', thresh)
    cv2.waitKey(1)

print('exitting')    
shut_down_servo()
shutdowncam()