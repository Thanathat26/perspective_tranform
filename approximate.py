import cv2
import numpy as np
image = cv2.imread(r'C:\Users\User\Desktop\perspective_tranform\img\p8.jpg')  
original = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_brown = np.array([22, 85, 20])
upper_brown = np.array([65, 255, 212])
mask = cv2.inRange(hsv, lower_brown, upper_brown)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # top-left
    rect[2] = pts[np.argmax(s)]      # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left
    return rect
if contours:
    l_contours = max(contours, key=cv2.contourArea)
    epsilon = 0.06 * cv2.arcLength(l_contours, True)
    approx = cv2.approxPolyDP(l_contours, epsilon, True)
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
        
    else:
        hulls = [cv2.convexHull(c) for c in contours]
        areas = [cv2.contourArea(h) for h in hulls]
        if len(areas) > 0:
            max_idx = np.argmax(areas)
            max_hull = hulls[max_idx]
            cv2.drawContours(original, [max_hull], -1, (0, 255, 0), 3)
            mask_hull = np.zeros_like(mask)
            cv2.drawContours(mask_hull, [max_hull], -1, 255, -1)
            masked_image = cv2.bitwise_and(original, original, mask=mask_hull)

            cv2.imshow("Masked Hull Area", masked_image)
cv2.imshow("convex hull", original)
cv2.imshow("mask", mask)
cv2.waitKey(0)