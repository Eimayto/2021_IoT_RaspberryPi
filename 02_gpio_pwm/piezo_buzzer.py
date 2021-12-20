import RPi.GPIO as GPIO
import time

BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 주파수 : 도 (262Hz)
pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(50)               # duty cycle (0~100)
# 음량 조절

try:
    time.sleep(2)
    pwm.ChangeDutyCycle(0)  # 부저음이 나지 않음

finally:
    pwm.stop()
    GPIO.cleanup()