#Volgende code laat iig de keys zien die je input
# import curses

# def main(stdscr):
#     # do not wait for input when calling getch
#     stdscr.nodelay(1)
#     while True:
#         # get keyboard input, returns -1 if none available
#         c = stdscr.getch()
#         if c != -1:
#             # print numeric value
#             stdscr.addstr(str(c) + ' ')
#             stdscr.refresh()
#             # return curser to start position
#             stdscr.move(0, 0)

# if __name__ == '__main__':
#     curses.wrapper(main)
###
#werkt mogelijk ook
# mport pygame
# pygame.init()

# finished = False

# while not finished:
#   for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#       finished = True
#    if event.type == pygame.KEYDOWN:
#       if event.key == #specify your keys and actions here
###
# Werkt sowieso en onderstaande code is erop gebaseerd
# import curses
# #init the curses screen
# stdscr = curses.initscr()
# #use cbreak to not require a return key press
# curses.cbreak()
# print "press q to quit"
# quit=False
# # loop
# while quit !=True:
#    c = stdscr.getch()
#    print curses.keyname(c),
#    if curses.keyname(c)=="q" :
#       quit=True

# curses.endwin()

import RPi.GPIO as gpio
import time
import curses
#init the curses screen
stdscr = curses.initscr()
#use cbreak to not require a return key press
curses.cbreak()
print "press q to quit"
quit=False

def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)
 
def forward(tf):
 init()
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
    print "starting loop, q not pressed yet"
    print "forward"
    forward(4)
    print "backward"
    reverse(2)
    c = stdscr.getch()
    #print curses.keyname(c),
    if curses.keyname(c)=="q" :
      quit=True
except KeyboardInterrupt:
        GPIO.cleanup()
curses.endwin()