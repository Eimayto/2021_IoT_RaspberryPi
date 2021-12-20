import cv2

# image 파일 읽기
img = cv2.imread('example.jpg')
img2 = cv2.resize(img, (1120, 586))

# imshow(윈도우 이름, 출력할 영상 데이터)
cv2.imshow('Son', img2)

# Edge선 추출하기
edge1 = cv2.Canny(img2, 50, 100)    # 임계치 min, max
edge2 = cv2.Canny(img2, 100, 150)
edge3 = cv2.Canny(img2, 150, 200)

cv2.imshow('edge1', edge1)
cv2.imshow('edge2', edge2)
cv2.imshow('edge3', edge3)

# 키보드 입력을 기다림 (millisecond)
# 기본값 0, 0인 경우 키보드 입력이 있을 때까지 계속 기다림
# waitKey()를 호출해야 화면에 영상이 나타남
cv2.waitKey(0)

# 열려있는 모든 창 닫기
cv2.destroyAllWindows()