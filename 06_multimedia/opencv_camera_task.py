import cv2

cap = cv2.VideoCapture(0)   # 카메라 장치 열기

if not cap.isOpened():
    print('Camera open failed')
    exit()

# 동영상 촬영하기
while True:
    ret, frame = cap.read()
    if not ret:
        break
    edge = cv2.Canny(frame, 50, 100)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    cv2.imshow('edge', edge)
    cv2.imshow('gray', gray)

    if cv2.waitKey(10) == 13:   # 0.01초
        break


# 사용자 자원 해제
cap.release()
cv2.destroyAllWindows()