#l298n functions

in1 = 17
in2 = 27
en_a = 4
#percentage of motor speed
speed=35


def connect_l298n(GPIO):
    global in1
    global in2
    global en_a
    global speed
    
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(en_a,GPIO.OUT)


def start_driving(GPIO,starting_Speed):
    q=GPIO.PWM(en_a,100)
    q.start(starting_Speed)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    return q
    
def change_speed(GPIO,myspeed,q):
    q.start(myspeed)
    return q

def shut_l298n(GPIO):
    GPIO.output(in1,GPIO.OUT)
    GPIO.output(in2,GPIO.OUT)