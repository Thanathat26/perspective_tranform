import cv2
import numpy as np
import math
image = cv2.imread(r'C:\Users\User\Desktop\perspective_tranform\img\p1.jpg')
orig_image = image.copy()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_brown = np.array([10, 100, 20]) 
upper_brown = np.array([30, 255, 200])
mask = cv2.inRange(hsv, lower_brown, upper_brown)
contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
def equilateral_third_point(P1, P5):
    x1, y1 = P1
    x2, y2 = P5

    # 1. หาความยาวด้าน d
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # 2. หาจุดกึ่งกลาง M
    mx, my = (x1 + x2)/2, (y1 + y2)/2

    # 3. หาค่าความสูง h ของสามเหลี่ยมด้านเท่า
    h = (math.sqrt(3)/2) * d

    # 4. หาเวกเตอร์ตั้งฉาก v⊥ จาก P1->P2
    vx_perp = -(y2 - y1)
    vy_perp = (x2 - x1)

    # 5. ปรับขนาดเวกเตอร์ตั้งฉากให้ความยาวเท่าความสูง h
    # ความยาวเวกเตอร์ตั้งฉากคือ d (ตามที่คุณบอก)
    ux = vx_perp / d
    uy = vy_perp / d

    # 6. คำนวณพิกัดจุดที่ 3
    x3 = mx + h * ux
    y3 = my + h * uy

    return (x3, y3)
for c in contours:
    area = cv2.contourArea(c)
    if area < 1000:
        continue
    accuracy = 0.03 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, accuracy, True)

    if len(approx) >= 3:
        points = approx.reshape(-1, 2)
        
        if len(points) >= 5:
            P1, P2, P3, P4, P5 = points[:5]
            P6 = equilateral_third_point(P1, P5)

            for i, pt in enumerate([P1, P2, P3, P4, P5]):
                cv2.circle(image, tuple(pt), 6, (255, 0, 0), -1)
                cv2.putText(image, f"P{i+1}", (pt[0] + 10, pt[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # วาด P6 จุดที่คำนวณได้
            cv2.circle(image, (int(P6[0]), int(P6[1])), 6, (0, 255, 0), -1)
            cv2.putText(image, "P6", (int(P6[0]) + 10, int(P6[1]) + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            quad = np.array([P1, P2, P3, P4, P5], dtype=np.int32)
            cv2.polylines(image, [quad], isClosed=True, color=(0, 255, 255), thickness=2)

            print("P6:", P6)
# แสดงผล
cv2.imshow('Mask', mask)
cv2.imshow('Detected Rectangle with P1-P4', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
