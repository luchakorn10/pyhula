import time
import threading
import keyboard
import pyhula

# ===== CONFIG (ตั้งค่าการบิน) =====
STEP = 100         # ระยะทาง/ความแรง ต่อการกด 1 ครั้ง
SPEED = 100        # ความเร็วในการเคลื่อนที่
YAW = 90           # องศาการหมุน
TICK = 0.01        # ความถี่ในการอ่านคีย์บอร์ด (ยิ่งน้อยยิ่งสมูท)
TAKEOFF_DELAY = 3.0

# ===== INIT & CONNECT =====
print("⏳ Waiting for drone connection...")
api = pyhula.UserApi()

if not api.connect():
    raise RuntimeError("❌ ไม่สามารถเชื่อมต่อกับโดรนได้ (Connect ไม่ผ่าน)")
print("✅ Connected Successfully!")

# เช็คแบตเตอรี่
try:
    batt = api.get_battery()
    print(f"🔋 Battery: {batt}%")
except Exception:
    pass

# ===== STATE =====
running = True
flying = False

# ===== COMMANDS (คำสั่งขึ้น-ลงจอด) =====
def takeoff():
    global flying
    if not flying:
        print("⬆️ TAKEOFF (กำลังบินขึ้น)")
        api.single_fly_takeoff()
        flying = True
        time.sleep(TAKEOFF_DELAY)

def land():
    global flying
    if flying:
        print("🛬 LAND (กำลังลงจอด)")
        api.single_fly_touchdown()
        flying = False
        time.sleep(2)

# ===== CONTROL LOOP (ระบบดักจับคีย์บอร์ด) =====
def control_loop():
    global running
    
    while running:
        # 1. คำสั่งพื้นฐาน (กดได้ตลอด)
        if keyboard.is_pressed('t'):
            takeoff()
        elif keyboard.is_pressed('l'):
            land()
        elif keyboard.is_pressed('esc'):
            print("🚨 EMERGENCY STOP / EXIT")
            land()
            running = False
            break
            
        # 2. คำสั่งเคลื่อนที่ (ทำได้เฉพาะตอนบินอยู่เท่านั้น)
        if flying:
            # ใช้ elif เพื่อให้โดรนรับทีละ 1 คำสั่ง ป้องกันการกด 2 ปุ่มพร้อมกันแล้วเอ๋อ
            if keyboard.is_pressed('w'):
                print("➡️ forward")
                api.single_fly_forward(STEP)
                time.sleep(0.1) # หน่วงเวลาเล็กน้อยให้โดรนขยับเสร็จ

            elif keyboard.is_pressed('s'):
                print("⬅️ back")
                api.single_fly_back(STEP)
                time.sleep(0.1)

            elif keyboard.is_pressed('a'):
                print("⬅️ left")
                api.single_fly_left(STEP)
                time.sleep(0.1)

            elif keyboard.is_pressed('d'):
                print("➡️ right")
                api.single_fly_right(STEP)
                time.sleep(0.1)

            elif keyboard.is_pressed('up'):
                print("⬆️ up")
                api.single_fly_up(STEP)
                time.sleep(0.1)

            elif keyboard.is_pressed('down'):
                print("⬇️ down")
                api.single_fly_down(STEP)
                time.sleep(0.1)

            elif keyboard.is_pressed('q'):
                print("↩️ turn left")
                api.single_fly_turnleft(YAW, 0)
                time.sleep(0.1)

            elif keyboard.is_pressed('e'):
                print("↪️ turn right")
                api.single_fly_turnright(YAW, 0)
                time.sleep(0.1)

            # โหมดตีลังกา (จาก Version B)
            elif keyboard.is_pressed('1'):
                print("🤸 flip fwd")
                api.single_fly_somersault(0)
                time.sleep(1.5) # ตีลังกาต้องใช้เวลาหน่วงนานหน่อย
            elif keyboard.is_pressed('2'):
                print("🤸 flip back")
                api.single_fly_somersault(1)
                time.sleep(1.5)
            elif keyboard.is_pressed('3'):
                print("🤸 flip left")
                api.single_fly_somersault(2)
                time.sleep(1.5)
            elif keyboard.is_pressed('4'):
                print("🤸 flip right")
                api.single_fly_somersault(3)
                time.sleep(1.5)

        time.sleep(TICK)

# ===== START PROGRAM =====
# แยก Thread ให้การรอรับปุ่มคีย์บอร์ดทำงานอยู่เบื้องหลัง
threading.Thread(target=control_loop, daemon=True).start()

print("""
===================================
🎮 Hula Drone: Keyboard Control 🎮
===================================
[ T ] = บินขึ้น (Takeoff)     |  [ L ] = ลงจอด (Land)

[ W / S ] = เดินหน้า / ถอยหลัง |  [ ↑ / ↓ ] = บินขึ้น / บินลง
[ A / D ] = บินซ้าย / บินขวา   |  [ Q / E ] = หมุนหันหน้าซ้าย / ขวา

[ 1, 2, 3, 4 ] = ตีลังกา (หน้า/หลัง/ซ้าย/ขวา)
[ ESC ] = ลงจอดและปิดโปรแกรม
===================================
*** คลิกเมาส์ที่หน้าต่าง Command Prompt ค้างไว้เวลาจะกดบังคับ ***
""")

# รันโปรแกรมหลักทิ้งไว้เพื่อไม่ให้โค้ดจบการทำงาน
while running:
    time.sleep(1)