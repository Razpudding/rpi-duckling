import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses

class Propulsion(object):

  def init(self):

    gpio.setwarnings(False)

    #Set the pinmode to BCM
    gpio.setmode(gpio.BCM)

    #init the curses screen
    self.stdscr = curses.initscr()
    #use cbreak to not require a return key press
    curses.cbreak()
    self.quit=False

    gpio.setup(18, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    #Set pulse modulation to 50hz for pin 18 and 13 and store that initialization in a va$
    self.pwm = gpio.PWM(18, 50)
    self.pwm = gpio.PWM(13, 50)
    #Start the pwm at 0% duty cycle
    self.pwm.start(0)
    self.speed = 30

  def resetGpio(self):
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    gpio.setup(18, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    self.pwm.ChangeDutyCycle(self.speed)

  def forward(self, tf):
    self.resetGpio()
    print("inching forward with speed "+ str(self.speed))
    self.pwm.ChangeDutyCycle(self.speed)
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(tf)
    gpio.cleanup()

  def reverse(self, tf):
    self.resetGpio()
    print("awkwardly backing away with speed "+ str(self.speed))
    self.pwm.ChangeDutyCycle(self.speed)
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()

  def start(self):
    try:
      while quit!=True:
        print ("waiting for input...")
        #get the entered characters
        c = self.stdscr.getch()
        #dont know what this line does tbh
        curses.endwin()
        if curses.keyname(c)=="w" :
          self.forward(2)
        elif curses.keyname(c)=="s" :
          self.reverse(2)
        elif curses.keyname(c)=="u" and self.speed <= 90:
          self.speed += 10
        elif curses.keyname(c)=="d" and self.speed >= 40:
          self.speed -= 10
        #print curses.keyname(c),
        # if curses.keyname(c)=="q" :
        #   quit=True
    except KeyboardInterrupt:
      self.pwm.stop()
      gpio.cleanup()
  
  def stop(self):
    self.resetGpio()
propulsion = Propulsion()
propulsion.init()
propulsion.start()






