#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
import pigpio
import time

servo = 18
# gpio 18 is pin 6, a pwm type
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

print('90 degrees')
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 1 )
total=0

def turn(ang):
    pulse=500+(100/9)*ang
    pwm.set_servo_pulsewidth( servo, pulse ) ;
    time.sleep( 2 )

turn(0)
turn(180)
turn(0)
turn(180)


pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 1 )
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )
print('bye')
exit()   
 




     



