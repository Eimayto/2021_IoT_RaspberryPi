import RPi.GPIO as GPIO
import time

BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 주파수 : 도 (262Hz)
pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(50)               # duty cycle (0~100)
# 음량 조절

melody = [262, 294, 330, 349, 392, 440, 494, 523]
#         도    레   미   파   솔   라    시   도

try: 
    for i in melody:
        pwm.ChangeFrequency(i)
        time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()