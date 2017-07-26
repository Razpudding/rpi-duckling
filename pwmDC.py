import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses
gpio.setwarnings(False)

#Set the pinmode to BCM
gpio.setmode(gpio.BCM)

#init the curses screen
stdscr = curses.initscr()
#use cbreak to not require a return key press
curses.cbreak()
quit=False

gpio.setup(18, gpio.OUT)
#Set pulse modulation to 50hz for pin 18 and store that initialization in a va$
pwm = gpio.PWM(18, 50)
#Start the pwm at 0% duty cycle
pwm.start(0)
speed = 30

def init():
  gpio.setmode(gpio.BCM)
  gpio.setup(17, gpio.OUT)
  gpio.setup(22, gpio.OUT)
  gpio.setup(23, gpio.OUT)
  gpio.setup(24, gpio.OUT)
  gpio.setup(18, gpio.OUT)
  pwm.ChangeDutyCycle(speed)

def forward(tf):
  init()
  print("moving forward with speed "+ str(speed))
  gpio.output(17, True)
  gpio.output(22, False)
  gpio.output(23, True)
  gpio.output(24, False)
  time.sleep(tf)
  gpio.cleanup()

def reverse(tf):
  init()
  gpio.output(17, False)
  gpio.output(22, True)
  gpio.output(23, False)
  gpio.output(24, True)
  time.sleep(tf)
  gpio.cleanup()

try:
  while quit!=True:
    print "waiting for input..."
    #get the entered characters
    c = stdscr.getch()
    #dont know what this line does tbh
    curses.endwin()
    if curses.keyname(c)=="w" :
      forward(2)
    elif curses.keyname(c)=="s" :
      reverse(2)
    elif curses.keyname(c)=="u" and speed <= 90:
      speed += 10
    elif curses.keyname(c)=="d" and speed >= 40:
      speed -= 10
    #print curses.keyname(c),
    # if curses.keyname(c)=="q" :
    #   quit=True
except KeyboardInterrupt:
  pwm.stop()
  gpio.cleanup()