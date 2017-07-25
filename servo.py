# Autor:	Ingmar Sxtapel
# Date:		20160811
# Version:	1.0
# Homepage:	www.custom-build-robots.com

import RPi.GPIO as GPIO
import time
from random import randint

GPIO.setmode(GPIO.BCM)

# define the servo pins. 
# Here you could change the code and add your pins for example
servoPIN18 = 18

move1 = 0
move2 = 0

GPIO.setup(servoPIN18, GPIO.OUT)

# GPIO 18 als PWM mit 50Hz 
p18 = GPIO.PWM(servoPIN18, 50) 
# initial position
p18.start(4) 
time.sleep(1)

# This loop will not end until you kill the program
try:
  while True:
    # Via random define the new value for the DutyCycle
    move1 = randint(4,11)
    move2 = randint(4,11)
	# Change the DutyCycle to move the robot to the position
    p18.ChangeDutyCycle(move2)
    time.sleep(1)
	
except KeyboardInterrupt:
  p18.stop()
  GPIO.cleanup()
