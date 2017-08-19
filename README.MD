# This is our raspberry pi 3b project where we experiment with a self-driving robot! 🤖🐤
The idea is that this code eventually drives a robot mimicking a lost little duckling, in search of its parent. The rpi duckling will autonomously drive around until it recognizes a person through computer vision, after which it imprints on that person and follows them around.
My dad and I are building this project together and it's still under development.

## Features
- A fluent driving controller (through keyboard keys)
- Built-in autonomous behavior (altoug the robot is not aware of its surroundings atm so it will eventually bump into them)
- A web stream of the video from the camera to a website available to all devices on the same WAN
- Audio playback support (altough the audio out pwm is on the same pin as one of the wheels PWM for the moment...)

The wiring scheme for our bot can be found [here](https://github.com/Razpudding/rpi-duckling/blob/master/docs/wiring_diagram.png)

## Todo
- [ ] Recognize something. Anything really (with open CV).
- [ ] Combine the streamhosting script with the engine propulsion script and the openCV script
- [ ] Expand the autonomous mode to include more complex behaviour as well as "quack" sounds indicating what the duckling is about to do.
- [ ] While in autonomous mode, respond to voice commands
- [ ] Rewrite code without using time.sleep() (possibly using events) allowig better control and simultaneous processes.
- [ ] Send audio through softPWM possibly using pigpio to free up the PWM channels for the DC engines
- [ ] Turns out some of the code examples I used are not Python 3 -> port code to Python 3

