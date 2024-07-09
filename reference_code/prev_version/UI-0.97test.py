#####File Properties######
#file name: UI-0.97.py
#target: UI
#version: 0.97
##########################

import RPi.GPIO as GPIO
import time

target = 18
delay = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(target,GPIO.OUT)

while True:
    GPIO.output(target,True)
    time.sleep(delay)
    GPIO(target,False)
    time.sleep(delay)
