import cv2
import numpy as np
import time
import keyboard
import pyhula
import json
from tensorflow.keras.models import load_model

# ==========================================
# 🧠 1. โหลด AI จากไฟล์ที่แปลงมาหมาดๆ
# ==========================================
print("==============================================")
print("🧠 กำลังเตรียมระบบ AI (Offline 100%)")
print("==============================================")

# ดึงชื่อท่าทางจากไฟล์ metadata.json โดยตรง
try:
    with open("metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
        # ดึงรายชื่อท่าทางและทำให้เป็นตัวพิมพ์เล็กทั้งหมด ป้องกันการพิมพ์ผิด
        class_names = [label.lower() for label in metadata["labels"]]
    print(f"✅ พบท่าทางทั้งหมด: {class_names}")
except Exception as e:
    raise RuntimeError("❌ หาไฟล์ metadata.json ไม่พบ! (ก๊อปปี้มาวางหรือยัง?)")

# โหลดโมเดล Keras ที่เพิ่งแปลงเสร็จ
try:
    np.set_printoptions(suppress=True)
    model = load_model("keras_model.h5", compile=False)
    print("✅ โหลด AI Model พร้อมใช้งาน!")
except Exception as e:
    raise RuntimeError("❌ โหลดไฟล์ keras_model.h5 ไม่สำเร็จ! (รันไฟล์ convert_model.py หรือยัง?)")


# ==========================================
# 🚁 2. เชื่อมต่อโดรน Hula
# ==========================================
print("\n⏳ กำลังเชื่อมต่อโดรน (ต่อ Wi-Fi โดรนได้เลย)...")
api = pyhula.UserApi()
if not api.connect():
    raise RuntimeError("❌ ไม่สามารถเชื่อมต่อกับโดรนได้!")
print("✅ เชื่อมต่อโดรนสำเร็จ!")

STEP = 50
COOLDOWN = 1.0  
last_cmd_time = 0
flying = False

def takeoff():
    global flying
    if not flying:
        print("\n🚀 TAKEOFF (กำลังบินขึ้น)")
        api.single_fly_takeoff()
        flying = True
        time.sleep(3)

def land():
    global flying
    if flying:
        print("\n🛬 LAND (กำลังลงจอด)")
        api.single_fly_touchdown()
        flying = False
        time.sleep(2)


# ==========================================
# 🎥 3. เปิดกล้องสั่งการ
# ==========================================
print("\n--- 🟢 ระบบพร้อมใช้งาน 🟢 ---")
print("🚨 กด 'ESC' เพื่อลงจอดและปิดโปรแกรม")

# Array สำหรับใส่รูปให้ Keras
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, image = cap.read()
        if not ret: break
        
        # คีย์บอร์ดฉุกเฉิน
        if keyboard.is_pressed('esc'): break
        if keyboard.is_pressed('t'): takeoff()
        if keyboard.is_pressed('l'): land()
        
        image = cv2.flip(image, 1) # กลับซ้ายขวา
        h, w, _ = image.shape
        
        # ตัดภาพเป็นสี่เหลี่ยมจัตุรัสและย่อขนาด
        start_x = w//2 - h//2
        img_cropped = image[:, start_x:start_x+h]
        img_resized = cv2.resize(img_cropped, (224, 224), interpolation=cv2.INTER_AREA)
        
        # แปลงเป็น Array 
        image_array = np.asarray(img_resized)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1.0
        data[0] = normalized_image_array

        # ให้ AI ทายผล
        prediction = model.predict(data, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        
        current_time = time.time()

        # มั่นใจเกิน 85% ค่อยทำงาน
        if confidence_score > 0.85:
            text = f"{class_name.upper()} ({str(int(confidence_score * 100))}%)"
            cv2.putText(image, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # --- ส่งคำสั่งไปที่โดรน ---
            if current_time - last_cmd_time > COOLDOWN:
                
                # ท่า Takeoff (เฉพาะตอนอยู่พื้น)
                if class_name == "takeoff" and not flying:
                    takeoff()
                    last_cmd_time = current_time + 2
                
                # คำสั่งอื่นๆ (เฉพาะตอนบิน)
                elif flying:
                    if class_name in ["landing", "land"]:
                        land()
                        last_cmd_time = current_time
                        
                    elif class_name == "up":
                        print("⬆️ บินขึ้น")
                        api.single_fly_up(STEP, STEP) # แก้บั๊กบัคพารามิเตอร์ให้แล้วครับ!
                        last_cmd_time = current_time
                        
                    elif class_name == "down":
                        print("⬇️ บินลง")
                        api.single_fly_down(STEP, STEP) 
                        last_cmd_time = current_time
                        
                    elif class_name == "flip":
                        print("🤸 ตีลังกา")
                        api.single_fly_somersault(0)
                        last_cmd_time = current_time + 1
                        
                    elif class_name == "hover":
                        pass
        else:
            cv2.putText(image, "Analyzing...", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.rectangle(image, (start_x, 0), (start_x+h, h), (255, 0, 0), 2)
        cv2.imshow("Teachable Machine x Hula Drone", image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    print("\n🚨 ลงจอดและปิดกล้อง...")
    land()
    cap.release()
    cv2.destroyAllWindows()