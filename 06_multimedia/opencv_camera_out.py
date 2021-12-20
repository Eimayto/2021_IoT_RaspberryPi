import cv2

# 카메라로부터 VideoCapture 객체 생성
cap = cv2.VideoCapture(0)   # 카메라 장치 열기

if not cap.isOpened():
    print('Camera open failed')
    exit()

# fourcc(four character code) : DIVX(avi), MP4V(mp4), X264(h265)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # = 'D','I','V','X'

# 동영상 저장을 위한 VideoWriter 객체 생성
# fps, 해상도
out = cv2.VideoWriter('output.avi', fourcc, 30, (640, 480))


# 동영상 촬영하기
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('frame', frame)
    out.write(frame)

    if cv2.waitKey(10) == 13:   # 0.01초
        break


# 사용자 자원 해제
cap.release()
out.release()
cv2.destroyAllWindows()