# import RPi.GPIO as gpio
import time
 
lastsave = time.time()
 
state = "still"
def init():
  pass
# gpio.setmode(gpio.BCM)
# gpio.setup(17, gpio.OUT)
# gpio.setup(22, gpio.OUT)
# gpio.setup(23, gpio.OUT)
# gpio.setup(24, gpio.OUT)
 
def forward(tf):
  init()
  global lastsave
  lastsave = time.time()
  global state
  state = "forward"
  print(state)
# gpio.output(17, True)
# gpio.output(22, False)
# gpio.output(23, True) 
# gpio.output(24, False)
# time.sleep(tf)
# gpio.cleanup()
 
def reverse(tf):
  init()
  global lastsave
  lastsave = time.time()
  global state
  state = "reverse"
  print(state)
# gpio.output(17, False)
# gpio.output(22, True)
# gpio.output(23, False) 
# gpio.output(24, True)
# time.sleep(tf)
# gpio.cleanup()

try:
  while True:
    
    global lastsave
    if time.time() - lastsave > 1 and state == "forward":
      reverse(1)
    elif time.time() - lastsave > 1:
      forward(1)
#		if time.time() - lastsave > 1:
except KeyboardInterrupt:
  pass
        # gpio.cleanup()
