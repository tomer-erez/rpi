#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
import pigpio
import time

servo = 18
# 18 is pin 6
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

print('90 degrees')
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 1 )

# pulse=500 -> 0 degrees
# pulse=2500 -> 180 degrees

# pulse= 500+(100*9)*x
while True:
    try:
        ang=int(input())
        pulse=500+(100/9)*ang
        if pulse>2500 or pulse<500:
            pwm.set_servo_pulsewidth( servo, 1500 ) ;
            time.sleep( 1 )
            pwm.set_PWM_dutycycle( servo, 0 )
            pwm.set_PWM_frequency( servo, 0 )
            print('please enter a degree between 0->180')
            print('bye')
            exit()
        pwm.set_servo_pulsewidth( servo, pulse ) ;
        time.sleep( 1 )
    except ValueError:
        pwm.set_servo_pulsewidth( servo, 1500 ) ;
        time.sleep( 1 )
        print('oops! ilegal input')
        pwm.set_PWM_dutycycle( servo, 0 )
        pwm.set_PWM_frequency( servo, 0 )
        print('bye')
        exit()
    
