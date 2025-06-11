import cv2
import numpy as np

# อ่านภาพ
image = cv2.imread(r'C:\Users\ASUS\Desktop\Pill classification\perspective tranform\pic\pic01.jpg')
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# กำหนดช่วงค่าสีน้ำตาลใน HSV
lower_brown = np.array([10, 100, 20])
upper_brown = np.array([35, 255, 200])

# สร้าง mask
mask = cv2.inRange(hsv, lower_brown, upper_brown)

# กำจัด noise
kernel = np.ones((5,5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# หา contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ฟังก์ชันเรียงลำดับจุด
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left
    return rect

# วาด contour และแปลงภาพ
for cnt in contours:
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    if len(approx) == 4 and cv2.isContourConvex(approx):
        area = cv2.contourArea(approx)
        if area > 500:
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

            # --- เพิ่ม Perspective Transform ---
            pts = approx.reshape(4, 2)
            rect = order_points(pts)

            (tl, tr, br, bl) = rect
            widthA = np.linalg.norm(br - bl)
            widthB = np.linalg.norm(tr - tl)
            maxWidth = int(max(widthA, widthB))

            heightA = np.linalg.norm(tr - br)
            heightB = np.linalg.norm(tl - bl)
            maxHeight = int(max(heightA, heightB))

            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]
            ], dtype="float32")

            # Perspective transform
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(original, M, (maxWidth, maxHeight))

            # แสดงผลภาพแปลงมุมมอง
            cv2.imshow("Warped", warped)

# แสดงภาพต้นฉบับ + ตรวจจับ
cv2.imshow("Detected Brown Rectangles", image)
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
