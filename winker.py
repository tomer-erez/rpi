
import RPi. GPIO as GPIO
import time
# Use pin numbers (not GPIO numbers!)
left=26
right=22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO. setup (left, GPIO. OUT)

GPIO. setup (right, GPIO. OUT)

    
def led_off(gpio_pin):
    GPIO. output (gpio_pin, GPIO. OUT)
    
def led_on(gpio_pin):
    GPIO. output (gpio_pin, GPIO. HIGH)
    
while True:
    ans=input()
    if ans=='L' or ans=='l':
        led_on(left)
        time.sleep(1)
        led_off(left)
    elif ans=='R' or ans=='r':
        led_on(right)
        time.sleep(1)
        led_off(right)
    else:
        break

GPIO. cleanup ()

