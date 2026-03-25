from tensorflowjs.converters import load_keras_model

print("🔄 กำลังแปลงไฟล์จาก TensorFlow.js เป็น Keras (.h5)...")
try:
    # โหลดไฟล์ model.json ที่คุณโหลดมาจากเว็บ
    model = load_keras_model("model.json")
    
    # เซฟเป็นไฟล์ h5 ทันที
    model.save("keras_model.h5")
    print("✅ แปลงไฟล์สำเร็จ! ได้ไฟล์ keras_model.h5 เอาไปคุมโดรนได้เลย!")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")