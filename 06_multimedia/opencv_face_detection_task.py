import cv2

# xml 분류기 파일 로드
face_cascade = cv2.CascadeClassifier('./xml/face.xml') 
eye_cascade = cv2.CascadeClassifier('./xml/eye.xml')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed')
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
         # ROI(Region of Interest, 관심영역)
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0, 2))

    cv2.imshow('frame', frame)

    if cv2.waitKey(10) == 13:   # 0.01초
        break


cap.release()
cv2.destroyAllWindows()