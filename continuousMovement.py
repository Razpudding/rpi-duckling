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
    gpio.setup(13, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

    #Set pulse modulation to 50hz for pin 18 and store that initialization in $
    self.pwm1 = gpio.PWM(18, 50)
    self.pwm2 = gpio.PWM(13, 50)
    #Start the pwm at 0% duty cycle
    self.pwm1.start(0)
    self.pwm2.start(0)
    self.speed1 = 60
    self.speed2 = 60

  def forward(self):
    print("inching forward with speed "+ str(self.speed1))
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)

  def reverse(self):
    print("awkwardly backing away with speed "+ str(self.speed1))
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)

  def left(self):
    print("to the left ")
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)

  def right(self):
    print("to the right ")
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)

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
        elif option == "a":
            self.left()
        elif option == "d":
            self.right()
        elif option == "b":
            self.stop()
        #Todo check if both speeds are within bounds
        elif option=="k" and self.speed1 <= 90:
          self.speed1 += 10
          self.speed2 += 10
          self.pwm1.ChangeDutyCycle(self.speed1)
          self.pwm2.ChangeDutyCycle(self.speed2)
        elif option=="m" and self.speed1 >= 40:
          self.speed1 -= 10
          self.speed2 -= 10

          self.pwm1.ChangeDutyCycle(self.speed1)
          self.pwm2.ChangeDutyCycle(self.speed2)
        time.sleep(.1)
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
    self.pwm1.ChangeDutyCycle(0)
    self.pwm2.ChangeDutyCycle(0)

    gpio.cleanup()
    curses.endwin()
propulsion = Propulsion()
propulsion.init()
propulsion.start()

