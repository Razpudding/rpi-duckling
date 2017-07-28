import RPi.GPIO as gpio
import time
#curses is used to capture the keyboard input
import curses
import pygame
from random import randint

#TODO: re-enable pylinter and set it up properly
#TODO: set up a finally that cleans up the GPIOs always instead of just after a keyboardbreak (ctr-c)
class Propulsion(object):
  def __init__(self):
    self.stdscr = curses.initscr()
    curses.endwin()
    #Disable warnings for the GPIOs being in use
    gpio.setwarnings(False)
    #Set the pinmode to BCM
    gpio.setmode(gpio.BCM)
    gpio.setup(18, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

    #Set pulse modulation to 50hz for pin 18 and store that initialization in a variable
    self.pwm1 = gpio.PWM(18, 50)
    self.pwm2 = gpio.PWM(13, 50)
    #Start the pwm at 0% duty cycle
    self.pwm1.start(0)
    self.pwm2.start(0)
    #The normal speed for forwards and backwards momentum
    self.cruisingSpeed = 60
    self.speedRight = 60
    self.speedLeft = 60
    #Initialize the state of the propulsion
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
    #TODO: put the following 2 lines in a function so the code is more DRY
    self.speedRight = self.speedLeft = self.cruisingSpeed
    self.updateCycle()
    self.state = "forward"
    self.turnWheel("right", "forward")
    self.turnWheel("left", "forward")

  def reverse(self):
    print("awkwardly backing away with speed "+ str(self.cruisingSpeed))
    self.speedRight = self.speedLeft = self.cruisingSpeed
    self.updateCycle()
    self.state = "reverse"
    self.turnWheel("right", "reverse")
    self.turnWheel("left", "reverse")

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
        # This is a nifty trick to control quickturning. If quickturn is true, the left wheel turns backward,
        # the right wheel forward; if quickturn is false, the left wheel stops (false, false) the right wheel turns forward.
        self.turnWheel("left", "reverse") if self.quickTurn else self.turnWheel("left", "stop")
        self.turnWheel("right", "forward")

  def right(self):
    print("to the right ")
    if self.state == "forward" and self.state != "right":
        print("forward right")
        #Todo, move speed to the turnWheel function as well, makes for easier code when turning when reversing
        #Maybe its best to turn wheels into an object and have the rest of the script only rack if the bot is moving forwards or backwards
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
        self.turnWheel("right", "reverse") if self.quickTurn else self.turnWheel("right", "stop")
        self.turnWheel("left", "forward")

  def goDuckYour(self):
    '''This function selects a random sequence and executes it. 
    Each sequence contains 1 or more instructions like "left" or "forward. Each instruction is coupled to a function
    each function sets the GPIOs up. After each instruction the sequence will wait for a number of seconds.
    The coding in this function may look a bit ugly that's what you get with custom sequences...'''
    print("Loose yourself (autonomous mode)") 
    testMoves = [self.left, self.right, self.reverse]
    waggleMoves = [self.left, self.right]
    sequence2 = ["enableQuickTurn"]
    waggleMode = True

    def test():
        ''''This mode is for testing out fun sequences. Just pop em in testmoves and watch her go.
        If you find a nice combo, save it an array, give it a name in the modemapping object and gooo'''
        print("Executing testmoves")
        for instruction in testMoves:
            instruction()
            time.sleep(3)

    def spin():
        ''''Time to go crazy'''
        print("WUBBA LUBBA DUB DUUUUB")
        #TODO: change this after I fix the math for changeSpeed so it accepts an absolute number
        self.changeSpeed(-10)
        self.left()
        time.sleep(.5)
        while (self.cruisingSpeed <= 90):
            self.changeSpeed(10)
            self.left()
            time.sleep(.5)
        self.right()
        time.sleep(2)

    def waggle():
        '''Waggle works like this: left,right,left,random quickturn, repeat patter with %chance through recursion'''
        print("Executing waggle")
        self.enableQuickTurn(False)
        for i in range(3):
            waggleMoves[0]()
            time.sleep(.3)
            waggleMoves[1]()
            time.sleep(.3)
        self.enableQuickTurn(True)
        waggleMoves[randint(0,1)]()
        time.sleep(1)
        if (randint(0,9) >= 4):
            waggle()
    #TODO: find a way to interrupt sleep so this process can be stopped by the user
    #This dict holds the dirrent modes for autonomous movement
    modeMapping = {
        "1" : test,
        "2" : waggle,
        "3" : spin
    }
    userInput = self.stdscr.getch()
    option = curses.keyname(userInput)
    curses.endwin()
    modeMapping[option]()
    self.stop()

  def start(self):
    try:
      while True:
        curses.cbreak()
        userInput = self.stdscr.getch()
        option = curses.keyname(userInput)
        curses.endwin()
        print("input is: " + str(option))
        #we could convert this to a dictionary mapping but that wouldnt work for the more complex options
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
        elif option == "0":
            self.goDuckYour()
        elif option=="k":
          self.changeSpeed(self.cruisingSpeed + 10)
        elif option=="m":
          self.changeSpeed(self.cruisingSpeed - 10)
        #build in a bit of a delay to not overwork the processor too much
        time.sleep(.02)
    except KeyboardInterrupt:
      self.quit()

  def changeSpeed(self, value):
    #TODO: Im pretty sure this function can work with absolute values being passed, as in
    # We want the speed to be 90 so we pass in 90. I started doing the math below and then realized Im
    # Too drunk/tired to finish it. Ah well, let future Laurens worry about it
    # Also it might be better to have a function that sets both the wheel direction and the speed. Then,
    # The wheels can be objects with direction and speed as properties, yay OOP
    # if (value >= 40 and value <= 90):
    #     self.cruisingSpeed = value
    #     self.speedRight *= 
    print("changeSpeed called with: " + str(value) + " cruisingspeed: " + str(self.cruisingSpeed))
    if ( (self.cruisingSpeed + value) <= 100 and (self.cruisingSpeed + value) >= 30 ):
        self.cruisingSpeed += value
        self.speedRight *= (1 + value / 100)
        self.speedLeft *= (1 + value / 100)
        if (self.speedRight > 100):
            print("right over limit: " + str(self.speedRight))
            self.speedRight = 100
    self.updateCycle()

  def stop(self):
    print("Stop! Hammertime")
    self.state = "still"
    self.turnWheel("left", "stop")
    self.turnWheel("right", "stop")

  def turnWheel(self, wheel, direction):
    if wheel == "left":
        if direction == "forward":
            gpio.output(23, True)
            gpio.output(24, False)
        elif direction == "reverse":
            gpio.output(23, False)
            gpio.output(24, True)
        elif direction == "stop":
            gpio.output(23, False)
            gpio.output(24, False)
    if wheel == "right":
        if direction == "forward":
            gpio.output(17, True)
            gpio.output(22, False)
        elif direction == "reverse":
            gpio.output(17, False)
            gpio.output(22, True)
        elif direction == "stop":
            gpio.output(17, False)
            gpio.output(22, False)

  def enableQuickTurn(self, value):
    self.quickTurn = value

  def updateCycle(self):
    self.pwm1.ChangeDutyCycle(self.speedRight)
    self.pwm2.ChangeDutyCycle(self.speedLeft)

  def quit(self):
    print("quitting program")
    self.pwm1.ChangeDutyCycle(0)
    self.pwm2.ChangeDutyCycle(0)
    gpio.cleanup()
    curses.endwin()

propulsion = Propulsion()
propulsion.start()
