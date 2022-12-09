import RPi.GPIO as GPIO          
from time import sleep
GPIO.setwarnings(False)
'''
cod is base on
https://collvy.com/blog/controlling-dc-motor-with-raspberry-pi/
'''
in1 = 17
in2 = 27
en_a = 4



GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en_a,GPIO.OUT)

print('enter initial speed- 45 is recommended')

try:
    speed=int(input())

except ValueError:
    GPIO.output(in1,GPIO.OUT)
    GPIO.output(in2,GPIO.OUT)
    GPIO.cleanup()
    print('illegal speed')
    print('exitting')
    GPIO.cleanup()
    exit()
q=GPIO.PWM(en_a,100)
 #percentage of motor speed
q.start(speed)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)


# Wrap main content in a try block so we can  catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent the user seeing lots of unnecessary error messages.
try:
# Create Infinite loop to read user input
   while(True):
      # Get user Input
      user_input = input()
      
      # To see users input
      # print(user_input)

      if user_input in ['f','F']:
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
      
      elif user_input in ['u','U']:
          
          print('current speed=', speed, '%')
          print('which speed % should i change to')
          try:
              user_input=int(input())
          except ValueError:
              print ('ValueError')
              GPIO.cleanup()
              exit()
              
          
          print('changing speed from',speed, 'to', user_input)
          speed=user_input
          
          q.start(speed)
          
          
         
          
      
      elif user_input in ['r','R']:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)

         print('reverse')

         
      # Press 'c' to exit the script
      elif user_input == 's':
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.LOW)
         print('Stop')
      
      else:
          GPIO.output(in1,GPIO.OUT)
          GPIO.output(in2,GPIO.OUT)
          GPIO.cleanup()
          print("GPIO Clean up")
          print('exitting')
          break
# If user press CTRL-C
except KeyboardInterrupt:
  # Reset GPIO settings
  GPIO.output(in1,GPIO.OUT)
  GPIO.output(in2,GPIO.OUT)
  GPIO.cleanup()
  print("GPIO Clean up")