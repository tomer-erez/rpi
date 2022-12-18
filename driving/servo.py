#servo functions and setup
from time import sleep
#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import pigpio

# 18 is pin 6
servo_pin = 18
pwm = pigpio.pi()
base_forward_direction=1500

def connect_servo():
    global servo_pin
    global pwm
    global base_forward_direction
    
    pwm.set_mode(servo_pin, pigpio.OUTPUT)
    pwm.set_PWM_frequency( servo_pin, 50 )
    pwm.set_servo_pulsewidth( servo_pin, base_forward_direction ) ;
    sleep( 1 )
    
    
    
    
    

''' 
pulse=(5000/109)*(angle+32.7)
angle=-32.7+(0.0218)*pulse     
          
     \21.8 |21.8/
      \    |   /
       \   |  /
        \  | /
         \ |/
___________|______________0
        max 21.8 left and right
'''
width=640
cam_span_width=12# camera sees 12 centimeters at 7 centimeter away from chassis
pixel_width=cam_span_width/width
width_strip=30
height_strip=40
vertical_cam_distance=7


from math import atan,pi

def find_steering_angle(lane_area):
    global width
    global cam_span_width# camera sees 12 centimeters at 7 centimeter away from chassis
    global vertical_cam_distance
    
    pixel_width=cam_span_width/width
    center_lane=(lane_area[0]+lane_area[1])//2
    if center_lane in range(305,335):
        return 0
    width_distance=(320-center_lane)*pixel_width
    angle=atan(width_distance/vertical_cam_distance)*180/pi
    print("center_lane", center_lane)
    print("steering_angle=", angle)
    #right is negative degrees, left is positive
    return angle

def angle_to_pulse(angle):
    pulse=(5000/109)*(angle+32.7)
    if pulse<500:
        pulse=500
    if pulse>2500:
        pulse=2500
    return int(pulse)

def steer(lane_area,winker_state,pwm,servo_pin):
    angle=find_steering_angle(lane_area)
    pulse=angle_to_pulse(angle)
    pwm.set_servo_pulsewidth( servo_pin, pulse )
    
    return angle
        












def shut_servo():
    pwm.set_servo_pulsewidth( servo_pin, base_forward_direction ) ;
    sleep( 1 )
    pwm.set_PWM_dutycycle( servo_pin, 0 )
    pwm.set_PWM_frequency( servo_pin, 0 )