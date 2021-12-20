import RPi.GPIO as GPIO
import time

RED = 4
GREEN = 17
YELLOW = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)

GPIO.output(RED, GPIO.HIGH)
print("Red Led ON")
time.sleep(2)
GPIO.output(RED, GPIO.LOW)
print("Red Led OFF")

GPIO.output(GREEN, GPIO.HIGH)
print("Green Led ON")
time.sleep(2)
GPIO.output(GREEN, GPIO.LOW)
print("Green Led OFF")

GPIO.output(YELLOW, GPIO.HIGH)
print("Yellow Led ON")
time.sleep(2)
GPIO.output(YELLOW, GPIO.LOW)
print("Yellow Led OFF")

GPIO.cleanup()