#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
GPIO.cleanup()

import pigpio
import time

servo = 18
# 18 is pin 6
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

print('3.825 degrees right is the base, because the car drifts left')

print('base is 3.825 right compared to a forward line or 86.175 compared to right line')
print( 'so pulse=1347 is straight, pulse of 500 is 23.5 degrees right, pulse of 2500 is 25 degrees left')
base_forward_direction=1500
steering_sides=['l','L','r','R']
pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;

time.sleep( 1 )

''' 
pulse=(5000/109)*(angle+32.7)
angle=-32.7+(0.0218)*pulse
'''

'''        
          straight
          
          
     \21.8 |21.8/
      \    |   /
       \   |  /
        \  | /
         \ |/
___________|______________0
        
here are the possible angles for the wheels to point to:

'''
print('range of steering angles: 18.5 degrees right to 25.078 degrees left\n\n')



def shut_down_servo():
    pwm.set_servo_pulsewidth( servo, base_forward_direction ) ;
    time.sleep( 1 )
    pwm.set_PWM_dutycycle( servo, 0 )
    pwm.set_PWM_frequency( servo, 0 )
    print('oops! ilegal input')
    print('bye')
    GPIO.cleanup()
    exit()

def angle_to_pulse(angle):
    pulse=(5000/109)*(angle+32.7)
    if pulse<500:
        pulse=500
    if pulse>2500:
        pulse=2500
    return int(pulse)

def steer(angle,side):
    if side in ['r','R']:
        angle*=-1
    pulse=angle_to_pulse(angle)
    pwm.set_servo_pulsewidth( servo, pulse ) ;
    time.sleep( 0.1 )
    print('\n\n')

while True:
    try:
        print('insert steering side: L/R')
        side=input()
        if side not in steering_sides:
            shut_down_servo()
        print('insert steering angle: max left= 21.8, max right= 21.8')
        angle=float(input())
        steer(angle,side)
        
    except ValueError:
        shut_down_servo()
    except KeyboardInterrupt:
        shut_down_servo()

