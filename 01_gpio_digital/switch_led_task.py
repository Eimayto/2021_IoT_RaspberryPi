import RPi.GPIO as GPIO

RED_SWITCH = 10
YELLOW_SWITCH = 9
GREEN_SWITCH = 11

RED_LED = 13
YELLOW_LED = 19
GREEN_LED = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)


# 누르지 않았을 때 : 0, 눌렀을 때 : 1
GPIO.setup(RED_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 내부 풀다운 저항
GPIO.setup(YELLOW_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GREEN_SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

try:
    while True:
        red = GPIO.input(RED_SWITCH)
        yellow = GPIO.input(YELLOW_SWITCH)
        green = GPIO.input(GREEN_SWITCH)

        GPIO.output(RED_LED, red)
        GPIO.output(YELLOW_LED, yellow)
        GPIO.output(GREEN_LED, green)
finally:
    GPIO.cleanup()
    print("cleanup and exit")