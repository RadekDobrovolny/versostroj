# Code for operation matrix LED display. It is 3 x 7 LEDs.
# 3 rows and 7 columns.

import RPi.GPIO as GPIO
import time
        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#constants; GPIO pins for every row and column
#HOR are rows, VER are columns.
HOR0 = 23
HOR1 = 24
HOR2 = 25

VER0 = 11
VER1 = 9
VER2 = 10
VER3 = 22
VER4 = 21
VER5 = 17
VER6 = 4

# setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(HOR0,GPIO.OUT)
GPIO.setup(HOR1,GPIO.OUT)
GPIO.setup(HOR2,GPIO.OUT)

GPIO.setup(VER0,GPIO.OUT)
GPIO.setup(VER1,GPIO.OUT)
GPIO.setup(VER2,GPIO.OUT)
GPIO.setup(VER3,GPIO.OUT)
GPIO.setup(VER4,GPIO.OUT)
GPIO.setup(VER5,GPIO.OUT)
GPIO.setup(VER6,GPIO.OUT)

# init message
print "LED on"

# Let there be light!
while True:    
    GPIO.output(HOR0, GPIO.HIGH)
    GPIO.output(HOR1, GPIO.HIGH)
    GPIO.output(HOR2, GPIO.HIGH)
    GPIO.output(VER0, GPIO.LOW)
    GPIO.output(VER1, GPIO.LOW)
    GPIO.output(VER2, GPIO.LOW)
    GPIO.output(VER3, GPIO.LOW)
    GPIO.output(VER4, GPIO.LOW)
    GPIO.output(VER5, GPIO.LOW)
    GPIO.output(VER6, GPIO.LOW)
