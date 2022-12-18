import cv2
import numpy as np
#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.cleanup()
import pigpio
import time
from math import atan,pi

in1 = 17
in2 = 27
en_a = 4
servo = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)
q=GPIO.PWM(en_a,100)
#percentage of motor speed
speed=35
q.start(speed)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

# 18 is pin 6 outside
# two more connections are needed: voltage and ground.
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo, 50 )
base_forward_direction=1500
pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;

# Use pin numbers (not GPIO numbers!)
left=26
right=22
GPIO. setup (left, GPIO. OUT)
GPIO. setup (right, GPIO. OUT)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
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
width_strip=30
height_strip=40
vertical_cam_distance=7 #cam starts seeing 7cm away in horizontal distance
winker_state=0


def led_off(gpio_pin):
    GPIO. output (gpio_pin, GPIO. OUT)
    
def led_on(gpio_pin):
    GPIO. output (gpio_pin, GPIO. HIGH)

def shutdowncam():
    vid.release()
    cv2.destroyAllWindows()
def shut_down_servo():
    pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;
    time.sleep( 1 )
    pwm.set_PWM_dutycycle( servo, 0 )
    pwm.set_PWM_frequency( servo, 0 )
def shut_down_l298n():
    GPIO.output(in1,GPIO.OUT)
    GPIO.output(in2,GPIO.OUT)
    GPIO.cleanup()
    
    
def find_lane(frame):
    '''
    gets a frame and returns the left edge of the lane, right edge of the lane as list
    '''
    for x in range(0,640,width_strip):
        left_lane_edge=-1
        right_lane_edge=-1
        cur_shade=np.mean(frame[450:480,x:x+width_strip])
        if cur_shade>200:
            left_lane_edge=x
            break
    for x in range(640,0,-width_strip):
        cur_shade=np.mean(frame[450:480,x-width_strip:x])
        if cur_shade>200:
            right_lane_edge=x
            
            break
    print("lane",left_lane_edge,right_lane_edge,"\n")
    return (left_lane_edge,right_lane_edge)

def find_steering_angle(lane_area):
    global width
    global cam_span_width# camera sees 12 centimeters at 7 centimeter away from chassis
    global vertical_cam_distance
    
    pixel_width=cam_span_width/width
    center_lane=(lane_area[0]+lane_area[1])//2
    if center_lane in range(290,350):
        return 0
    width_distance=(320-center_lane)*pixel_width
    angle=atan(width_distance/vertical_cam_distance)*180/pi
    print("center_lane", center_lane)
    print("steering_angle=", angle)

    return angle

def angle_to_pulse(angle):
    pulse=(5000/109)*(angle+32.7)
    if pulse<500:
        pulse=500
    if pulse>2500:
        pulse=2500
    return int(pulse)

def wink(angle,winker_state):
    
    if angle>12:
        if winker_state!=1:
            print('winking left')
            led_on(left)
            winker_state=1
            
    elif angle<-12:
        if winker_state!=-1:
            print('winking right')
            led_on(right)
            winker_state=-1
    else :
        if winker_state!=-1:
            led_off(left)
            led_off(right)
            winker_state=0
        
def steer(lane_area,winker_state):
    angle=find_steering_angle(lane_area)
    pulse=angle_to_pulse(angle)
    wink(angle,winker_state)
    pwm.set_servo_pulsewidth( servo, pulse )

for i in range(10):    
    ret, frame = vid.read()
try:    
    for i in range(500):
        ret, frame = vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
        ret,thresh = cv2.threshold(frame,160,255,cv2.THRESH_BINARY)
        lane_area=find_lane(thresh)
        
        if lane_area==(-1,-1):
            print("why no lane -1 -1")
            continue

        steer(lane_area,winker_state)
        cv2.imshow('threshed_img', thresh)
        cv2.waitKey(1)
except KeyboardInterrupt:
    led_off(left)
    led_off(right)
    shut_down_servo()
    shutdowncam()
    shut_down_l298n()
        
print('exitting')
led_off(left)
led_off(right)
shut_down_servo()
shutdowncam()
shut_down_l298n()
exit()