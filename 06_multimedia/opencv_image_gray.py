import cv2

# image 파일 읽기
img = cv2.imread('example.jpg')
img2 = cv2.resize(img, (1120, 586))

gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)   # RGB(X) BGR(O)

cv2.imshow('Son', img2)
cv2.imshow('Son_GRAY', gray)

# 키보드 입력을 기다림 (millisecond)
# 기본값 0, 0인 경우 키보드 입력이 있을 때까지 계속 기다림
while True:
    if cv2.waitKey(0) == 13:
        break

# 파일로 저장하기
cv2.imwrite('Son_GRAY.jpg', gray)

# 열려있는 모든 창 닫기
cv2.destroyAllWindows()