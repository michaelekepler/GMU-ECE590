import cv2, numpy

img_path = "/home/student/Downloads/downloaded_robot.png"

img = cv2.imread(img_path,1) #1: color, 2: gray scale, 3: unchanged
cv2.imshow('image', img)
cv2.waitKey(10000)
cv2.destroyAllWindows()


