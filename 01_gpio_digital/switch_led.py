import RPi.GPIO as GPIO

SWITCH_PIN = 4
LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
# 누르지 않았을 때 : 0, 눌렀을 때 : 1
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # 내부 풀다운 저항

try:
    while True:
        val = GPIO.input(SWITCH_PIN)
        print(val)
        GPIO.output(LED_PIN, val)
finally:
    GPIO.cleanup()
    print("cleanup and exit")