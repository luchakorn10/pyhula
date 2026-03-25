import time
import pyhula

# ==============================================================
# ⚙️ ส่วนที่ 1: ระบบจัดการโดรน (ผู้สอนเตรียมไว้ให้ - นักเรียนไม่ต้องแก้ไข)
# ==============================================================
api = pyhula.UserApi()

print("⏳ กำลังเชื่อมต่อโดรน...")
if not api.connect():
    raise RuntimeError("❌ ไม่สามารถเชื่อมต่อกับโดรนได้ กรุณาตรวจสอบการเชื่อมต่อ!")
print("✅ เชื่อมต่อสำเร็จ!")

try:
    batt = api.get_battery()
    print(f"🔋 แบตเตอรี่: {batt}%")
except Exception:
    pass

# --- การตั้งค่าพื้นฐาน ---
SPEED = 100
BLOCK_SIZE = 100  # ระยะทางต่อ 1 บล็อก/1 ช่อง (ปรับให้เข้ากับขนาดสนามจริงได้)

# --- สร้างคำสั่งฉบับย่อให้ใช้งานเหมือน Block Code ---
def takeoff():
    print("⬆️ กำลังบินขึ้น (Takeoff)")
    api.single_fly_takeoff()
    time.sleep(3)

def land():
    print("🛬 กำลังลงจอด (Land)")
    api.single_fly_touchdown()
    time.sleep(2)

def forward(blocks=1):
    print(f"➡️ เดินหน้า {blocks} ช่อง")
    api.single_fly_forward(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def backward(blocks=1):
    print(f"⬅️ ถอยหลัง {blocks} ช่อง")
    api.single_fly_back(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def left(blocks=1):
    print(f"⬅️ บินซ้าย {blocks} ช่อง")
    api.single_fly_left(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def right(blocks=1):
    print(f"➡️ บินขวา {blocks} ช่อง")
    api.single_fly_right(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def up(blocks=1):
    print(f"⬆️ บินขึ้นสูง {blocks} ช่อง")
    api.single_fly_up(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def down(blocks=1):
    print(f"⬇️ บินลงต่ำ {blocks} ช่อง")
    api.single_fly_down(blocks * BLOCK_SIZE)
    time.sleep(2 * blocks)

def turn_left(degrees=90):
    print(f"↩️ หันหน้าทางซ้าย {degrees} องศา")
    api.single_fly_turnleft(degrees, 0)
    time.sleep(2)

def turn_right(degrees=90):
    print(f"↪️ หันหน้าทางขวา {degrees} องศา")
    api.single_fly_turnright(degrees, 0)
    time.sleep(2)

def flip_forward():  print("🤸 ตีลังกาไปข้างหน้า!"); api.single_fly_somersault(0); time.sleep(2)
def flip_backward(): print("🤸 ตีลังกาไปข้างหลัง!"); api.single_fly_somersault(1); time.sleep(2)
def flip_left():     print("🤸 ตีลังกาไปทางซ้าย!");  api.single_fly_somersault(2); time.sleep(2)
def flip_right():    print("🤸 ตีลังกาไปทางขวา!");  api.single_fly_somersault(3); time.sleep(2)


# ==============================================================
# 📝 ส่วนที่ 2: พื้นที่ภารกิจของนักเรียน (Student Mission Code)
# ==============================================================
print("\n🚀 เริ่มต้นรันโค้ดภารกิจของนักเรียน!")

try:
    # [ให้นักเรียนเขียนโค้ดเรียงต่อกันด้านล่างนี้เลย]
    
    takeoff()          # 1. สั่งให้โดรนบินขึ้น
    
    forward(2)         # 2. เดินหน้าไป 2 ช่อง (ผ่านอุโมงค์)
    turn_right()       # 3. หันขวา 90 องศา
    up(1)              # 4. บินสูงขึ้น 1 ช่อง (เพื่อเตรียมข้ามกำแพง)
    forward(1)         # 5. ข้ามกำแพงไปข้างหน้า 1 ช่อง
    down(1)            # 6. ลดระดับลงมา 1 ช่อง
    flip_forward()     # 7. ตีลังกาโชว์ 1 ทีเมื่อถึงเส้นชัย!

except Exception as e:
    # ถ้านักเรียนเขียนโค้ดผิด หรือเกิด Error กลางทาง จะแจ้งเตือน
    print(f"\n❌ เกิดข้อผิดพลาดระหว่างบิน: {e}")

finally:
    # ไม่ว่าจะเกิดอะไรขึ้น โดรนต้องลงจอดเสมอ! (สำคัญมากเพื่อความปลอดภัย)
    print("\n🚨 จบการทำงาน บังคับลงจอด...")
    land()
    print("🎉 จบภารกิจเรียบร้อย!")