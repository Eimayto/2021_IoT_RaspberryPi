# piezo_buzzer_task.py
import RPi.GPIO as GPIO
import time

BUZZER_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)


melody = [262, 294, 330, 349, 392, 440, 494, 523]
#         도    레   미   파   솔   라    시   도


# 주파수 : 도 (262Hz)
pwm = GPIO.PWM(BUZZER_PIN, melody[0])
pwm.start(50)               # duty cycle (0~100)
# 음량 조절

play = [4, 4, 5, 5, 4, 4, 2, 4, 4, 2, 2, 1, 4, 4, 5, 5, 4, 4, 2, 4, 2, 1, 2, 0]


try: 
    for i in range(24):
        pwm.ChangeDutyCycle(50)
        pwm.ChangeFrequency(melody[play[i]])
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)
        time.sleep(0.2)
        if((i+1) == 7 or (i+1) == 19):
            time.sleep(0.3)
        if((i+1) % 12 == 0):
            time.sleep(0.5)

finally:
    pwm.stop()
    GPIO.cleanup()