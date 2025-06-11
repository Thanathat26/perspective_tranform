import cv2
import numpy as np

def nothing(x):
    """Callback function สำหรับ trackbar (ไม่ต้องทำอะไร)"""
    pass

def main():
    # อ่านภาพ (เปลี่ยน path ตามภาพที่ต้องการ)
    image_path = input("กรุณาใส่ path ของภาพ (หรือกด Enter เพื่อใช้เว็บแคม): ")
    
    if image_path.strip() == "":
        # ใช้เว็บแคม
        cap = cv2.VideoCapture(0)
        use_camera = True
        print("กำลังใช้เว็บแคม... กด 'q' เพื่อออก")
    else:
        # ใช้ภาพจากไฟล์
        image = cv2.imread(image_path)
        if image is None:
            print("ไม่สามารถอ่านภาพได้ ตรวจสอบ path อีกครั้ง")
            return
        use_camera = False
        print("กำลังใช้ภาพจากไฟล์... กด 'q' เพื่อออก")

    # สร้างหน้าต่างสำหรับ trackbars
    cv2.namedWindow('HSV Controls')
    cv2.namedWindow('Original')
    cv2.namedWindow('HSV')
    cv2.namedWindow('Mask')
    cv2.namedWindow('Result')

    # สร้าง trackbars สำหรับ HSV ต่ำสุด
    cv2.createTrackbar('H Min', 'HSV Controls', 0, 179, nothing)
    cv2.createTrackbar('S Min', 'HSV Controls', 0, 255, nothing)
    cv2.createTrackbar('V Min', 'HSV Controls', 0, 255, nothing)

    # สร้าง trackbars สำหรับ HSV สูงสุด
    cv2.createTrackbar('H Max', 'HSV Controls', 179, 179, nothing)
    cv2.createTrackbar('S Max', 'HSV Controls', 255, 255, nothing)
    cv2.createTrackbar('V Max', 'HSV Controls', 255, 255, nothing)

    # ตั้งค่าเริ่มต้นสำหรับสีน้ำตาล
    cv2.setTrackbarPos('H Min', 'HSV Controls', 10)
    cv2.setTrackbarPos('S Min', 'HSV Controls', 100)
    cv2.setTrackbarPos('V Min', 'HSV Controls', 20)
    cv2.setTrackbarPos('H Max', 'HSV Controls', 35)
    cv2.setTrackbarPos('S Max', 'HSV Controls', 255)
    cv2.setTrackbarPos('V Max', 'HSV Controls', 200)

    print("\n=== คำแนะนำการใช้งาน ===")
    print("- ปรับ trackbars เพื่อเลือกช่วงสี HSV")
    print("- H (Hue): สีพื้นฐาน 0-179")
    print("- S (Saturation): ความอิ่มตัวของสี 0-255")
    print("- V (Value): ความสว่าง 0-255")
    print("- หน้าต่าง 'Mask': แสดงพื้นที่ที่ตรงกับเงื่อนไข (สีขาว)")
    print("- หน้าต่าง 'Result': แสดงผลลัพธ์ที่กรองแล้ว")
    print("- กด 'p' เพื่อพิมพ์ค่า HSV ปัจจุบัน")
    print("- กด 'r' เพื่อรีเซ็ตค่า")
    print("- กด 'q' เพื่อออก")

    while True:
        if use_camera:
            ret, frame = cap.read()
            if not ret:
                print("ไม่สามารถอ่านจากเว็บแคมได้")
                break
            current_image = frame
        else:
            current_image = image.copy()

        # แปลงเป็น HSV
        hsv = cv2.cvtColor(current_image, cv2.COLOR_BGR2HSV)

        # อ่านค่าจาก trackbars
        h_min = cv2.getTrackbarPos('H Min', 'HSV Controls')
        s_min = cv2.getTrackbarPos('S Min', 'HSV Controls')
        v_min = cv2.getTrackbarPos('V Min', 'HSV Controls')
        h_max = cv2.getTrackbarPos('H Max', 'HSV Controls')
        s_max = cv2.getTrackbarPos('S Max', 'HSV Controls')
        v_max = cv2.getTrackbarPos('V Max', 'HSV Controls')

        # สร้าง mask
        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # สร้างภาพผลลัพธ์
        result = cv2.bitwise_and(current_image, current_image, mask=mask)

        # เพิ่มข้อความแสดงค่า HSV บนภาพ
        text = f"HSV Lower: [{h_min}, {s_min}, {v_min}] Upper: [{h_max}, {s_max}, {v_max}]"
        cv2.putText(current_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(current_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        # แสดงภาพทั้งหมด
        cv2.imshow('Original', current_image)
        cv2.imshow('HSV', hsv)
        cv2.imshow('Mask', mask)
        cv2.imshow('Result', result)

        # รอการกดปุ่ม
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('p'):
            # พิมพ์ค่า HSV ปัจจุบัน
            print(f"\n=== ค่า HSV ปัจจุบัน ===")
            print(f"Lower HSV: [{h_min}, {s_min}, {v_min}]")
            print(f"Upper HSV: [{h_max}, {s_max}, {v_max}]")
            print(f"Code: lower_bound = np.array([{h_min}, {s_min}, {v_min}])")
            print(f"Code: upper_bound = np.array([{h_max}, {s_max}, {v_max}])")
        elif key == ord('r'):
            # รีเซ็ตค่า
            cv2.setTrackbarPos('H Min', 'HSV Controls', 0)
            cv2.setTrackbarPos('S Min', 'HSV Controls', 0)
            cv2.setTrackbarPos('V Min', 'HSV Controls', 0)
            cv2.setTrackbarPos('H Max', 'HSV Controls', 179)
            cv2.setTrackbarPos('S Max', 'HSV Controls', 255)
            cv2.setTrackbarPos('V Max', 'HSV Controls', 255)
            print("รีเซ็ตค่าเรียบร้อย")

    # ปิดการทำงาน
    if use_camera:
        cap.release()
    cv2.destroyAllWindows()

    # พิมพ์ค่าสุดท้าย
    print(f"\n=== ค่าสุดท้าย ===")
    print(f"lower_bound = np.array([{h_min}, {s_min}, {v_min}])")
    print(f"upper_bound = np.array([{h_max}, {s_max}, {v_max}])")

if __name__ == "__main__":
    main()