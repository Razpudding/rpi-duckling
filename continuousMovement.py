import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses

class Propulsion(object):

  def init(self):
    self.stdscr = curses.initscr()
    #use cbreak to not require a return key press
    curses.cbreak()

    gpio.setwarnings(False)

    #Set the pinmode to BCM
    gpio.setmode(gpio.BCM)

    gpio.setup(18, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

    #Set pulse modulation to 50hz for pin 18 and store that initialization in $
    self.pwm = gpio.PWM(18, 50)
    #Start the pwm at 0% duty cycle
    self.pwm.start(0)
    self.speed = 60

  def forward(self):
    print("inching forward with speed "+ str(self.speed))
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)

  def reverse(self):
    print("awkwardly backing away with speed "+ str(self.speed))
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)

  def start(self):
    try:
      while True:
#        print ("waiting for input...")
        #inp = raw_input()
        curses.cbreak()
        userInput = self.stdscr.getch()
        option = curses.keyname(userInput)
        #dont know what this line does tbh
        curses.endwin()
        print("input is: " + str(option))
        if option == "w":
            self.forward()
        elif option == "s":
            self.reverse()
        elif option == "b":
            self.stop()
        elif option=="u" and self.speed <= 90:
          self.speed += 10
          self.pwm.ChangeDutyCycle(self.speed)
        elif option=="d" and self.speed >= 40:
          self.speed -= 10
          self.pwm.ChangeDutyCycle(self.speed)
    except KeyboardInterrupt:
      self.quit()

  def stop(self):
    print("shutting down all engines")
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)

  def quit(self):
    print("quitting program")
    self.pwm.ChangeDutyCycle(0)
    gpio.cleanup()
    curses.endwin()
propulsion = Propulsion()
propulsion.init()
propulsion.start()

