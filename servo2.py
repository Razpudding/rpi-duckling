# Authors: 	Laurens Aarnoudse, Jelle Aarnoudse
# Date:		2017
# Version:	0.1

#Import the necessary packages
import RPi.GPIO as GPIO
import time
from random import randint

#Set the pinmode to BCM
GPIO.setmode(GPIO.BCM)

#Set the right outputs for the pins
GPIO.setup(18, GPIO.OUT)

#Set pulse modulation to 50hz for pin 18 and store that initialization in a variable
pwm = GPIO.PWM(18, 50)
#Start the pwm at 4% duty cycle
pwm.start(4)

#Set up a try to allow the programme to be ended by keyboard input
#After which the GPIO will be cleaned up
#The forloop will pick a random int and change the dutycycle to that int
DC=4
i=1
try:
        while True:
                pwm.ChangeDutyCycle(DC)
                time.sleep(1)
				DC=DC+i
				if DC=11 then i=i*(-1)

except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()