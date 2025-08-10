from src.agent.graph import create_robot_agent_graph
import time

def main():
    """
    ฟังก์ชันหลักสำหรับรัน Agent แบบวนลูปต่อเนื่อง
    """
    print("Initializing Robot Voice Agent...")
    # สร้าง Agent แค่ครั้งเดียวตอนเริ่มต้น
    app = create_robot_agent_graph()
    print("✅ Initialization complete. Agent is now running.")
    print("Press Ctrl+C to exit.")

    # เริ่มการทำงานแบบวนลูป
    while True:
        print("\n" + "="*50)
        print("Agent is ready and listening...")
        try:
            # เรียกใช้ Graph เพื่อเริ่มรอบการทำงานใหม่
            # แต่ละ invoke คือการทำงาน 1 รอบ ตั้งแต่ฟังเสียงจนถึงสั่งการ
            app.invoke({})
            
            print("\n✅ Workflow cycle finished.")
            # อาจจะหน่วงเวลาเล็กน้อยก่อนเริ่มรอบใหม่
            time.sleep(1) 

        except KeyboardInterrupt:
            # จัดการเมื่อผู้ใช้กด Ctrl+C เพื่อออกจากลูป
            print("\n\n🛑 Shutting down agent... Goodbye!")
            break
        except Exception as e:
            # จัดการข้อผิดพลาดอื่นๆ ที่อาจเกิดขึ้นในรอบการทำงานนั้นๆ
            # เพื่อไม่ให้โปรแกรมทั้งหมดพัง
            print(f"\n⚠️ An error occurred during this cycle: {e}")
            print("Restarting listening cycle...")
            time.sleep(2)

if __name__ == "__main__":
    main()