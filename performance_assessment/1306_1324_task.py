import cv2
import RPi.GPIO as GPIO
import time
from lcd import drivers

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# model, config 파일 설정
model = './dnn/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = './dnn/face_deploy.prototxt'

# 스위치 핀, 서보모터 핀 세팅
SWITCH_PIN = 4

flag = 0    # 계속 누르고 있다고 계속 촬영하지 않기 위한 변수
# 스위치를 누르고 있으면 1
#   ''   안  ''  있으면 0

# 도트메트릭스 스마일 출력 좌표
smile = [(0,2),(0,3),(0,4),(0,5),(1,1),(1,6),(2,0),(2,2),(2,5),(2,7),(3,0),(3,7),(4,0),(4,2),(4,5),(4,7),(5,0),(5,3),(5,4),(5,7),(6,1),(6,6),(7,2),(7,3),(7,4),(7,5)]

# 도트메트릭스 찡그린 얼굴 출력 좌표
frown = [(0,2),(0,3),(0,4),(0,5),(1,1),(1,6),(2,0),(2,2),(2,5),(2,7),(3,0),(3,7),(4,0),(4,2),(4,3),(4,4),(4,5),(4,7),(5,0),(5,7),(6,1),(6,6),(7,2),(7,3),(7,4),(7,5)]

# 꽉 차있어야 하는 인원수 = 반 인원수를 입력받음
max_cnt = int( input("반 인원수 > ") )

# 카메라 세팅
cap = cv2.VideoCapture(0)

# Load a pre-trained network
net = cv2.dnn.readNet(model, config)

if not cap.isOpened():
    print('Camera open failed')
    exit()

# 디스플레이 인스터스 생성
display = drivers.Lcd()

GPIO.setmode(GPIO.BCM)

# 스위치 내부 풀다운저항 세팅
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 인원수에 따라서 표정을 출력
def dot_matrix(n, block_orientation, rotate, inreverse, cnt):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,
                     cascaded=n or 1, 
                     block_orientation=block_orientation,
                     rotate=rotate or 0,
                     blocks_arranged_in_reverse_order=inreverse)
    x = device.width
    virtual = viewport(device, width=1 + x + x, height=device.height)
    # print("Created device")

    if cnt < max_cnt:
        emotion = frown
    else :
        emotion = smile   

    with canvas(virtual) as draw:
        for i in range(7):
            for j in range(7):
                draw.point((i, j), fill = None)
        for x, y in emotion:
            draw.point((x, y), fill = "white")


def face_detection():
    cnt = 0 # 인원수 측정
    _, frame = cap.read()
    if frame is None:
        return

    # blob 이미지 생성
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 117, 123))

    # blob 이미지를 네트워크 입력으로 설정
    net.setInput(blob)

    # 네트워크 실행 (순방향)
    detect = net.forward()
    detect = detect[0, 0, :, :]

    (h, w) = frame.shape[:2]

    # 얼굴 인식을 위한 반복
    for i in range(0, detect.shape[0]):
        # 얼굴 인식 확률 추출
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        cnt += 1

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)    # 얼굴 위치 표시
        label = 'Face: %4.3f' % confidence
        cv2.putText(frame, label, (x1, y1-1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)  # 확률 표시

    cv2.imshow('frame', frame)
    return cnt   # 인식한 얼굴 수 반환

# Lcd에 인원수 출력
def displaye(cnt):
    display.lcd_display_string('current student', 1)                # 첫 번째 줄에 'current stuend' 출력
    display.lcd_display_string(str(cnt)+' / ' + str(max_cnt), 2)    # 두 번째 줄에 인원수 출력

# 사진 찍기
def capture():
    global cap
    ret, frame  = cap.read()
    if not ret:
        return 0
    now_str = time.strftime("%Y%m%d_%H%M%S")
    cv2.imwrite('%s.jpg' % now_str, frame)    # 시간을 이름으로 사진 저장
    print('successfully captured!')

try:
    while True:
        cnt = face_detection()
        displaye(cnt)
        if cv2.waitKey(10) == 27:   # 0.01초, esc키 누르면 꺼짐
            break


        val = GPIO.input(SWITCH_PIN)    # 풀다운 저항 누르면 : 1, 안누르면 : 0
        if val and not flag:            # 처음 스위치를 누르면
            capture()
            flag = 1
        elif not val and flag:          # 스위치를 다시 때면
            flag = 0

        dot_matrix(1,0,0,False, cnt)    # 인원수에 따라 다른 표정 출력


finally:
    # 사용자 자원 해제
    cap.release()
    cv2.destroyAllWindows()
    display.lcd_clear()
    GPIO.cleanup()