#sudo pigpiod
import subprocess 
subprocess.check_output(["sudo", "pigpiod", "params"])
import RPi.GPIO as GPIO
import pigpio
import time

servo = 18

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

print('90 degrees')
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 1 )


for i in range(4):
    if i%2==0:
        ang=0
    else:
        ang=180
        
    pulse=500+(100/9)*ang
    pwm.set_servo_pulsewidth( servo, pulse ) ;
    time.sleep( 1 )
    
    
    
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 1 )
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )
print('bye')
exit()        

    

