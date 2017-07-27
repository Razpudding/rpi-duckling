import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses

class Propulsion(object):

  def init(self):

    gpio.setwarnings(False)

    #Set the pinmode to BCM
    gpio.setmode(gpio.BCM)

    gpio.setup(18, gpio.OUT)
    #Set pulse modulation to 50hz for pin 18 and store that initialization in $
    self.pwm = gpio.PWM(18, 50)
    #Start the pwm at 0% duty cycle
    self.pwm.start(30)
    self.speed = 60

#   gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

  def forward(self, tf):
    #self.resetGpio()
    print("inching forward with speed "+ str(self.speed))
    self.pwm.ChangeDutyCycle(self.speed)
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    #time.sleep(tf)
    #gpio.cleanup()

  def reverse(self, tf):
    self.resetGpio()
    print("awkwardly backing away with speed "+ str(self.speed))
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()


  def start(self):
    try:
      while True:
        print ("waiting for input...")
        inp= raw_input()
        if input == "w":
            self.forward()
        #get the entered characters
        if input == "q":
            self.stop()
    except KeyboardInterrupt:
      self.stop()

  def stop(self):
    print("shutting down all engines")
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    self.pwm.ChangeDutyCycle(0)
    gpio.cleanup()
propulsion = Propulsion()
propulsion.init()
propulsion.start()



