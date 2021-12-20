import RPi.GPIO as GPIO
import time
from math import floor

Trig1 = 10      # 첫번째 초음파 센서 Trig에 연결된 BCM번호
Echo1 = 9       # 첫번째 초음파 센서 Echo에 연결된 BCM번호

Trig2 = 27      # 두번째 초음파 센서 Trig에 연결된 BCM번호
Echo2 = 17      # 두번째 초음파 센서 Echo에 연결된 BCM번호

LED_PIN = 25    # LED가 연결된 BCM번호

flag = 0    # 0 : 입퇴장 확인 가능상태                                              -> 한명이 지나가길 시작하길 기다리는 상태
            # 1 : 아직 첫번째 초음파 센서 값만 작아져 두번째 초음파 센서 값 역시 작아지길 기다리는 상태 -> 한명이 완전히 지나갔음을 확인하는 상태
            # 2 : 아직 두번째 초음파 센서 값만 작아져 첫번째 초음파 센서 값 역시 작아지길 기다리는 상태 -> 한명이 완전히 지나갔음을 확인하는 상태
            # 3 : 순간적으로 입장해 제대로 측정되지 않는 경우를 대비해 1.5초를 기다리는 단계

flag_time = 0   # 언제부터 1.5 초를 기다렸는지 확인하기 위한 변수

led_time = 0    # led가 30초 켜져있었는지 확인하기 위한 변수

#               A  B  C    D   E  F  G
SEGMENT_PINS = [5, 6, 13, 19, 26, 8, 7]
DIGIT_PINS = [12, 16, 20, 21]
#             D1  D2  D3  D4

cnt = 0                         # 인원수를 저장하는 변수

criteria = 40                   # 몇cm 이내로 들어와야 사람이 지나간 것으로 판별할 것인가

data = [[1, 1, 1, 1, 1, 1, 0],  # 0
        [0, 1, 1, 0, 0, 0, 0],  # 1
        [1, 1, 0, 1, 1, 0, 1],  # 2
        [1, 1, 1, 1, 0, 0, 1],  # 3
        [0, 1, 1, 0, 0, 1, 1],  # 4
        [1, 0, 1, 1, 0, 1, 1],  # 5
        [1, 0, 1, 1, 1, 1, 1],  # 6
        [1, 1, 1, 0, 0, 0, 0],  # 7
        [1, 1, 1, 1, 1, 1, 1],  # 8
        [1, 1, 1, 0, 0, 1, 1]]  # 9

# GPIO 번호를 BCM으로 설정하고 목적에 맞게 핀을 각각 출력, 입력을 설저한다.
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig1, GPIO.OUT)
GPIO.setup(Trig2, GPIO.OUT)
GPIO.setup(Echo1, GPIO.IN)
GPIO.setup(Echo2, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

for segment in SEGMENT_PINS:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)

# 자릿수 제어 Pin HIGH->OFF, LOW->ON
for digit in DIGIT_PINS:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, GPIO.HIGH)



# 초음파 센서를 통해 거리를 측정해주는 함수
def ultra_sonic(trig, echo):
    GPIO.output(trig, GPIO.HIGH)
    # 10us (1us -> 0.000001s)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    while GPIO.input(echo) == 0:            # 펄스 발생 중
        pass
    start = time.time()                     # ECHO PIN HIGH(시작)

    while GPIO.input(echo) == 1:            # 펄스 발생 종료
        pass
    stop = time.time()                      # ECHo PIN LOW(종료)

    duration_time = stop - start
    distance = 17160 * duration_time

    return distance


# 4-digit FND에 숫자를 출력해주는 함수
def FND():
    global cnt

    _1000 = floor(cnt / 1000)                          # 천의 자릿수 구하기
    _100 = floor(cnt / 100) - 10 * _1000               # 백의 자릿수 구하기
    _10 = floor(cnt / 10) - 100 * _1000 - 10 * _100    # 십의 자릿수 구하기
    _1 = cnt - floor(cnt / 10) * 10                    # 일의 자릿수 구하기       

    num = [_1000, _100, _10, _1]

    for i in range(4):
        GPIO.output(DIGIT_PINS[i], GPIO.LOW)                            # DIGIT 선택
        for j in range(7):
            GPIO.output(SEGMENT_PINS[j], data[num[i]][j])               # 숫자 출력
            # print(str(data[num[i]][j]), end=' ')  <-- 디버깅용
        time.sleep(0.001)   
        GPIO.output(DIGIT_PINS[i], GPIO.HIGH)                           # DIGIT 선택 해제
        # print()  <-- 디버깅용
       
    time.sleep(0.001)
    # print()  <-- 디버깅용


# 입퇴장 확인과 LED 끄기켜기를 담당하는 함수
def in_or_out():
    global flag, cnt, criteria, flag_time, led_time
    
    ultra_1 = ultra_sonic(Trig1, Echo1)     # 첫번째 초음파 거리 측정
    ultra_2 = ultra_sonic(Trig2, Echo2)     # 두번째 초음파 거리 측정
    
    # print('ultra_1 : ' + str(ultra_1) + '\nultra_2 : '+str(ultra_2))  <-- 디버깅용
    
    if flag == 0:    # flag가 0인 경우
                    # -> 다음 입퇴장의 시작을 기다리는 경우

        if ultra_1 < criteria and ultra_2 >= criteria:      # 첫번째 초음파 센서만 짧아졌다면
            cnt += 1                                        # 1명 입장
            flag = 1                                        # 한명이 완전히 지나가기를 기다리는 상태
            
        elif ultra_1 >= criteria and ultra_2 < criteria:    # 두번째 초음파 센서만 짧아졌다면
            cnt -= 1                                        # 1명 퇴장
            flag = 2                                        # 한명이 완전히 지나가기를 기다리는 사앹

    if flag == 1:                                           # 두번째 초음파 센서 값 역시 작아지길 기다리는 상태
        # print(time.time()-flag_time)  <-- 디버깅용
        if ultra_2 < criteria:
            flag = 3                                        # 1.5 초 기다림 상태로 전환
            flag_time = time.time()                         # 현재 시간을 기록(1.5초 기다리기)
            led_time = time.time()                          # 현재 시간을 기록(LED 30초동안 켜기)
            GPIO.output(LED_PIN, GPIO.HIGH)                 # LED 켜기

    if flag == 2:                                           # 첫번째 초음파 센서 값 역시 작아지길 기다리는 상태
        # print(time.time()-flag_time)  <-- 디버깅용
        if ultra_1 < criteria:
            flag = 3                                        # 1.5 초 기다림 상태 
            flag_time = time.time()                         # 현재 시간을 기록(1.5초 기다리기)
            led_time = time.time()                          # 현재 시간을 기록(LED 30초동안 켜기)
            GPIO.output(LED_PIN, GPIO.HIGH)                 # LED 켜기

    if flag == 3:
        if time.time() - flag_time >= 1.5:                  # flag_time을 기록한 순간부터 1.5초가 지나면
            flag = 0                                        # 입퇴장 기다림 상태로 전환

    if time.time() - led_time >= 30:                        # LED가 켜진지 30초가 지나면
        GPIO.output(LED_PIN, GPIO.LOW)                      # LED 끄기


try:
    while True:
        in_or_out()                 # 입퇴장확인과 LED관리
        time.sleep(0.001)
        FND()                       # 지속적으로 인원수 4-digit FND에 출력


        
finally:
    GPIO.cleanup()
    print('cleanup and exit')