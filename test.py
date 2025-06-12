import cv2
import numpy as np

# อ่านรูป
image = cv2.imread(r'C:\Users\User\Desktop\perspective_tranform\img\p1.jpg')
orig_image = image.copy()
original = image.copy()

# แปลงเป็น HSV แล้วกำหนดช่วงสีน้ำตาล
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_brown = np.array([10, 100, 20])   # ปรับช่วงตามสีจริง
upper_brown = np.array([30, 255, 200])
mask = cv2.inRange(hsv, lower_brown, upper_brown)

# หา contour จาก mask ของสีน้ำตาล
contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# วาด contour และ rectangle เฉพาะวัตถุสีน้ำตาล
for c in contours:
    area = cv2.contourArea(c)
    if area < 1000:  # กรอง noise
        continue

    # วาดกรอบสี่เหลี่ยม
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(orig_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Polygon approximation
    accuracy = 0.03 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, accuracy, True)

    if len(approx) == 4:
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)

# แสดงผล
cv2.imshow('Brown Mask', mask)
cv2.imshow('Bounding Rectangles', orig_image)
cv2.imshow('Approximated Brown Polygons', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
