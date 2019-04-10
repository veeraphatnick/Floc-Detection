import cv2
import numpy as np

img = cv2.imread('image_example1.jpg')
cv2.namedWindow('Roi', cv2.WINDOW_NORMAL)
cv2.namedWindow('Threshold', cv2.WINDOW_NORMAL)

kernel = np.ones((7,7),np.uint8)
roi = img[: , :]
rows, cols, _ = roi.shape
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)

gray_roi = cv2.erode(gray_roi,kernel,iterations = 1)
#gray_roi = cv2.morphologyEx(gray_roi, cv2.MORPH_OPEN, kernel)

_, threshold = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)
#_, threshold = cv2.threshold(gray_roi,255,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


_, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

count = 0
for cnt in contours:
    (x, y, w, h) = cv2.boundingRect(cnt)
    area = w*h
    if area < 400000000:
        count = count+1
        cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 5)
        #cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.rectangle(roi, (0, 0), (200, 30), (255,255,255), -1)
    cv2.putText(roi,'Number of Floc : ' + str(count),
        (10,20),                  # bottomLeftCornerOfText
        cv2.FONT_HERSHEY_SIMPLEX, # font
        0.5,                      # fontScale
        (0,0,0),                  # fontColor
        1)                        # lineType

cv2.imshow("Threshold", threshold)
#cv2.imshow("gray roi", gray_roi)
cv2.imshow("Roi", roi)

cv2.waitKey(0)
cv2.destroyAllWindows()
