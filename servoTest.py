#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

servoPinTop = 17
servoPinBottom = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPinTop, GPIO.OUT)
GPIO.setup(servoPinBottom, GPIO.OUT)

pulseTop = GPIO.PWM(servoPinTop, 50)
pulseBottom = GPIO.PWM(servoPinBottom, 50)

pulseTop.start(7.5)
pulseBottom.start(7.5)

try:
    while True:
        pulseTop.ChangeDutyCycle(10)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(10)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(5)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(5)
        time.sleep(0.5)
        pulseTop.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(10)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(10)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(5)
        time.sleep(0.5)
        pulseBottom.ChangeDutyCycle(7.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    pulseTop.stop()
    pulseBottom.stop()
    GPIO.cleanup()
