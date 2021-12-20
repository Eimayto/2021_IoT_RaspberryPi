import cv2

# xml 분류기 파일 로드
face_cascade = cv2.CascadeClassifier('./xml/face.xml') 

img = cv2.imread('Avengers.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이미지에서 얼굴 검출
faces = face_cascade.detectMultiScale(gray) # 좌표값 나옴

# 얼굴에 사각형 출력하기
for (x,y,w,h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2) # 시작 좌표, 끝 좌표, 선 색깔(B,G,R), 선 두께

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()