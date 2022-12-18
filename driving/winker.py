#set up+winker functions
from time import sleep

#left=26
#right=22
#winker_state=0

    
def led_off(gpio_pin,GPIO):
    GPIO. output (gpio_pin, GPIO. OUT)
    
def led_on(gpio_pin,GPIO):
    GPIO. output (gpio_pin, GPIO. HIGH)

def connect_winker(GPIO,left,right):

    
    GPIO. setup (left, GPIO. OUT)
    GPIO. setup (right, GPIO. OUT)
    led_on(left,GPIO)
    led_on(right,GPIO)
    sleep(2)
    led_off(left,GPIO)
    led_off(right,GPIO)
    

def wink(angle,winker_state,left,right,GPIO):
    if angle>9:
        if winker_state!=ord('l'):
            print('winking left')
            led_on(left,GPIO)
            winker_state=ord('l')
            
    elif angle<-9:
        if winker_state!=('r'):
            print('winking right')
            led_on(right,GPIO)
            winker_state=ord('r')
    else :
        if winker_state!=0:
            led_off(left,GPIO)
            led_off(right,GPIO)
            winker_state=0
    
    return winker_state
            
def shut_winker(GPIO,left,right):
    
    led_off(left,GPIO)
    led_off(right,GPIO)
