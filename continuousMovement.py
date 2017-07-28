import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses
import pygame

class Propulsion(object):

  def __init__(self):
    self.stdscr = curses.initscr()
    #I think this line makes sure that if the program crashes, you can still see what you're typing in the console
    curses.endwin()
    gpio.setwarnings(False)

    #Set the pinmode to BCM
    gpio.setmode(gpio.BCM)

    gpio.setup(18, gpio.OUT)  #PWM-port for left motor
    gpio.setup(13, gpio.OUT)  #PWM-port for right motor
    gpio.setup(17, gpio.OUT)  #motor-left pin
    gpio.setup(22, gpio.OUT)  #motor-left pin
    gpio.setup(23, gpio.OUT)  #motor-right pin
    gpio.setup(24, gpio.OUT)  #motor-right pin

    #Set pulse modulation to 50hz for pins 18 and 13 and store that initialization in pwm1 and pwm2
    self.pwm1 = gpio.PWM(18, 50)
    self.pwm2 = gpio.PWM(13, 50)
    #Start the pwm at 0% duty cycle
    self.pwm1.start(0)
    self.pwm2.start(0)
    self.cruisingSpeed = 60
    self.speedRight = 60
    self.speedLeft = 60
    self.state = "awake"
    # The higher the steerforce, the more extreme the steering effect will be (1/2, 1/3 * power of other wheel)
    self.steerForce = 4
    self.quickTurn = True
    #self.laugh()

  def laugh(self):
    pygame.mixer.init()
    pygame.mixer.music.load("laugh.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

  def forward(self):
    print("inching forward with speed "+ str(self.cruisingSpeed))
    # Reset the speed of both wheels to cruising speed to disable left and right modes
    self.speedRight = self.speedLeft = self.cruisingSpeed
    self.updateCycle()
    self.state = "forward"
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)

  def reverse(self):
    print("awkwardly backing away with speed "+ str(self.cruisingSpeed))
    self.speedRight = self.speedLeft = self.cruisingSpeed
    self.updateCycle()
    self.state = "reverse"
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)

  def left(self):
    #When driving forward, slow down the left wheel to turn left
    #As of right now, the state has no 'forward left' so it will just output left
    if self.state == "forward" and self.state != "left":
        print("forward left")
        #TODO: keep separate state for forwardleft and right because this sin't dry
        #HEre the wheelspeeds are reset because if you turn forward right after forward left, the wheelspeeds would both be
        # divided by steerforce
        self.speedRight = self.speedLeft = self.cruisingSpeed
        self.speedLeft /= self.steerForce
        self.updateCycle()
    # The next mode is for when the bot stands still
    elif self.state != "forward" and self.state != "reverse":
        print("to the left from " + self.state)
        self.speedRight = self.speedLeft = self.cruisingSpeed
        self.updateCycle()
        self.state = "left"
        gpio.output(17, True)
        gpio.output(22, False)
        gpio.output(23, False)
        gpio.output(24, True) if self.quickTurn else gpio.output(24, False)

  def right(self):
    print("to the right ")
    if self.state == "forward" and self.state != "right":
        print("forward right")
        self.speedRight = self.speedLeft = self.cruisingSpeed
        self.speedRight /= self.steerForce
        self.updateCycle()
    # The next mode is for when the bot stands still
    elif self.state != "forward" and self.state != "reverse":
        print("to the right from " + self.state)
        #reset the speed of both wheels before turning.
        self.speedRight = self.speedLeft = self.cruisingSpeed
        self.updateCycle()
        self.state = "right"
        gpio.output(17, False)
        # This is a nifty trick to control quickturning. If quickturn is true, the left wheel turns backward,
        # the right wheel forward; if quickturn is false, the left wheel stops (false, false) the right wheel turns forward.
        gpio.output(22, True) if self.quickTurn else gpio.output(22, False)
        gpio.output(23, True)
        gpio.output(24, False)

  def goDuckYour(self):
    print("Loose yourself (autonomous mode)") 


  def start(self):
    try:
      while True:
        curses.cbreak()
        userInput = self.stdscr.getch()
        option = curses.keyname(userInput)
        #The next line makes sure your terminal typing wont crash
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
        elif option=="k" and self.cruisingSpeed <= 90:
          self.cruisingSpeed += 10
          self.speedRight *= 1.1
          self.speedLeft *= 1.1
          self.updateCycle()
          # self.pwm1.ChangeDutyCycle(self.speedRight * 1.1)
          #self.pwm2.ChangeDutyCycle(self.speedLeft * 1.1)
        elif option=="m" and self.cruisingSpeed >= 40:
          self.cruisingSpeed -= 10
          self.speedRight *= .9
          self.speedLeft *= .9
          self.updateCycle()
        #build in a bit of a delay to not overwork the processor too much
        #controls should still be snappy at this speed
        time.sleep(.1)
    except KeyboardInterrupt:
      self.quit()

  def stop(self):
    print("Stop! Hammertime")
    self.state = "still"
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)

  def updateCycle(self):
    self.pwm1.ChangeDutyCycle(self.speedRight)
    self.pwm2.ChangeDutyCycle(self.speedLeft)
    # if wheel == "left":
    #     self.pwm2.ChangeDutyCycle(speed)
    # elif wheel == "right":
    #     self.pwm1.ChangeDutyCycle(speed)

  def quit(self):
    print("quitting program")
    self.pwm1.ChangeDutyCycle(0)
    self.pwm2.ChangeDutyCycle(0)

    gpio.cleanup()
    curses.endwin()
propulsion = Propulsion()
#propulsion.init()
propulsion.start()

