import time
lastsave = 0


if time.time() - lastsave > 0.2:
	lastsave = time.time()
	

	
	
	
	 
def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)
 
def forward(tf):
 init()
 lastsave = time.time()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
#time.sleep(tf)
 gpio.cleanup()
 
def reverse(tf):
 init()
 lastsave = time.time()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, True)
#time.sleep(tf)
 gpio.cleanup()

 
 try:
	while True:
		print "forward"
		forward(1)
		if time.time() - lastsave > 1:
		print "backward"
		reverse(1)
		if time.time() - lastsave > 1:
except KeyboardInterrupt:
        gpio.cleanup()
