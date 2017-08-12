# The process of building our lost duckling bot

*Disclaimer: This "guide" was written so we, the creators of the project, could retrace our steps. It might be hard to follow for anyone else.*

### Setup
* Download the latest raspBian OS
* Put it on a micro SD card like so https://www.raspberrypi.org/documentation/installation/installing-images/README.md (you may need additional software to cmplete this step)
* Next step is to enable SSH on the Pi. We went with the quick way (described here https://hackernoon.com/raspberry-pi-headless-install-462ccabd75d0) and put an empty file called ssh on the boot sd card before booting the Pi. That way Pi will recognize the file on startup and configure SSH on it's own (and then delete the SSH file). Pretty handy :)
* Now it's time to put the SD card in the Pi, connect the Pi by ethernet cable to your WiFi router and connect a power cable to the Pi. It will boot and enable SSH.
* At this point, while looking up the ip address of the Pi, we gave it a static address in the router so it's easier to SSH to it later.
* Once you've SSHed into your Pi (make sure you're on the same network when doing this) you should get a message from Debian. You can now use `sudo raspi-config` to configure your Pi. It's always good to at least run the update function to make sure you're using the latest version. We also updated the timezone and locale to avoid annoying timing issues in the future. Finally, we expanded the file system (this is recommended in  lot of tutorials and is done automatically if you set up your rPi with 
* Now would also be a good time to update to the latest kernel using `sudo apt-get update` and `sudo apt-get dist-upgrade`
* Installing a GUI viewer like VNC is optional, but if you want to see the Raspbian GUI and not just the CLI you will need something like it.
* Now would also be the time to change the standard pwd so nobody else can SSH into your 🍰
* If you want you can now setup things like Wifi and Bluetooth like we did, using this guide: http://www.makeuseof.com/tag/setup-wi-fi-bluetooth-raspberry-pi-3/
* Now you'll want to make a (Github) repository holding your project's code. Then clone it to your own computer as well as to the Pi using the CLI. I chose to clone the project into the Pi's Documents folder (but there might be better places for this.)
* I experienced some problems sshin into my Pi on a network where I couldn't access the router. I used nmap to scan the network like so `nmap your.local.ip.0/24` which scans the entire subnet. Amongst the results should be one with a couple open ports like 22 for ssh, and 5900 for vnc and in my case a port for camera streaming. As I have no way of setting a static ip for the pi, i'll have to do this a lot... So I found better ways, [explained here](https://serialized.net/2013/04/headless_rpi/). I used that tutorial to set up a bash script for the mac terminal that will auto find and ssh to any rPi on the same network! Because the guide was working with the bash shell and I use the standard terminal, [I needed this post](https://stackoverflow.com/questions/8967843/how-do-i-create-a-bash-alias) as well to set things up. And for that I need tot install ssh-copy-id like so. In the end I had an issue with ssh-copy-id not finding the right keys(file?) so for now I just work with rpi_ip and then manually ssh into that ip.

Now that the initial setup works it's time to write our first python program. We used this tutorial (https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software)
We ran into the problem that importing wiringpi seems to fail. Possibly a Python3 vs 2 issue.
* we installed ipython3 as
* We set up a bash script you can execute remotely that [pulls the latest code from our Github repo](https://stackoverflow.com/questions/17099564/make-a-shell-script-to-update-3-git-repos) [using this to set up the bash script](http://www.circuitbasics.com/how-to-write-and-run-a-shell-script-on-the-raspberry-pi/)
* I went through [this tutorial](https://learn.sparkfun.com/tutorials/raspberry-gpio) to figure out how the raspberry works and how to code Python for rPi.

### SD Backup
* [Some background info](https://www.raspberrypi.org/documentation/linux/filesystem/backup.md) from Raspberry Pi.
* To be able to duplicate the exact rPi setup to our second bot, we're backing up the image of Eentje to a computer. W can then write that image to another SD card to duplicate the setup [like so](https://computers.tutsplus.com/articles/how-to-clone-raspberry-pi-sd-cards-using-the-command-line-in-os-x--mac-59911). Be sure to FORMAT AS FAT32 (at least for us that was the original formatting of the SD card). BTW, reading the image from a 16GB micro SD took my macbook pro 30minutes... Writing the new image to the second card will take a LOT longer. Might be faster using Etcher (for mac)
* Following this tutorial didn't work for us, the second SD card with the new image (which looks fine) won't let the rPi boot. It could be that because both cards are from different manufacturers en seem to have slightly different sizes (15.5 vs 15.6GB) that the whole image can't be written. It's also possible that reading the image file wasn't exectured properly. We're now attempting the same process using windows following [this guide](http://lifehacker.com/how-to-clone-your-raspberry-pi-sd-card-for-super-easy-r-1261113524). The windows method also failed, looks like it's a difference in SD cards :S
In the end we had to flash the original image and redo all the precious settings.
* Retrying [with this method](sudo%20dd%20if=/dev/disk2%20of=~/eentje.dmg) (essentially the same only now backup up SDcard 1 and then formatting SD1 and then writing to it again)
* After cloning the image of the first working rPis SD card to the second rPis SD card, the Github credentials on the second rPi as well as some other settings (like its identifier name it reports to the router) have to be edited manually.

### WiringPi
* We had some problems earlier getting wiringpi to work. To solve this, I had to install some Python-dev libs as per [this stackoverflow question](https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory). That allowed me to install wiringpi.
* I still couldn't run code with wiringpi, apparently it's an issue with a package in the latest kernel. I downgraded my kernel [following ths thread](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=182191). **Seems like something that might cause issues later**.

### MPU6050
* Enable and [Install i2c modules](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial). For us enabling was available from the interfacing menu
* To verify we can read the chips acc. [we used this tutorial](https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-32-mpu6050-gyro-acceleration-sensor-sensor-kit-v2-0-for-b-plus.html). This [tutorial describes how the code works](http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html) that reads out the sensor.
* Next, we followed [this tutorial](http://www.instructables.com/id/Building-a-segway-in-Raspberry-Pi/) to start balancing the robot.
* Then we set up a script to operate the DC motors using PWM. Here's a [basic tutorial](http://www.instructables.com/id/Raspberry-PI-L298N-Dual-H-Bridge-DC-Motor/) I used. The PWM part is self written and can be found in [the Github repo](https://github.com/Razpudding/rpi-duckling/blob/master/pwmDC.py).
* Found t[his very useful tut](https://www.hackster.io/Sam_ashu/simple-pi-robot-8270b5) showing how to use raw_input to get keyboar dinput. IMO a lot better then the screen method I was using previously. Also shows how to use vlc to stream video but we'll get to that later.

### Camera
* We're using the official rPi camera v2. It's easy enough to install, just make sure the silver art of the connector cable faces the HDMI port (on the rPi3B)
* To enable the camera, go through the config menu on your rPi and then reboot it
* Then we followed [this tutorial](http://www.instructables.com/id/Raspberry-Pi-remote-webcam/) to stream the video to a web address hosted by the rPi. Pretty cool trick that seems to be widely supported. Well that didn't work. Looks like it's supposed to be used with webcams connected through the USB port of the rpi.
* Yes! This [very brief picamera script](https://picamera.readthedocs.io/en/release-1.13/recipes2.html#web-streaming) works perfectly! I just use ipython3 filename.py to run it and then pi.ip.address.here:8000 to access the feed from my laptop.

### OpenCV
Finally, some computer vision!
* I followed this [extensive and excellent walkthrough](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/) of the installation process.
* I also took the time to set up a virtualenv
* During installation I made the decision to go with Python3. **This probably means I have to rewrite some of the scripts I wrote previously.** More importantly, using a virtualenv means that **any packages installed in the global environment will not be available in the virtual env and vise versa** it's a completely separate environment! `workon` command is used to go into the vurtalenv.
* Next up, [this tutorial](http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/) on getting started iwth OpenCV
* Finally finished installing openCV. looks like it all went well. Should prob do this later after verifying it works properly: 

### Differences between eentje & tweetje
Eentje:
* Tutorial on installing openCV finished. (takes 1.5 hours...)
Tweetje:
