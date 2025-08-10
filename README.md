# Voice Robot Agent 🤖

โปรเจกต์นี้คือ Agent สั่งการหุ่นยนต์ด้วยเสียง ที่ถูกออกแบบมาให้มีความยืดหยุ่นและสามารถเข้าใจคำสั่งที่ซับซ้อนได้ โดยใช้เทคโนโลยีล่าสุดดังนี้:

  - **Core Logic (LLM):** ใช้โมเดล **Gemini 2.0 Flash** ผ่าน Google AI API เป็นสมองของ Agent ในการตัดสินใจและเรียกใช้ฟังก์ชันพร้อมพารามิเตอร์
  - **Speech-to-Text (ASR):** ใช้โมเดล **Whisper Large v3** ผ่าน Hugging Face Inference API เพื่อแปลงเสียงพูดเป็นข้อความอย่างแม่นยำ
  - **Agent Framework:** สร้างบน **LangGraph** เพื่อจัดการสถานะ (State) และลำดับการทำงานที่ซับซ้อนได้อย่างเป็นระบบ ทำให้เห็นภาพรวมและง่ายต่อการดีบัก

-----

## ✨ คุณสมบัติ

  - **Intelligent & Voice-Powered:** รับคำสั่งเสียงภาษาไทยและภาษาอังกฤษ
  - **Parameterized Commands:** สามารถรับพารามิเตอร์ในคำสั่งเสียงได้ เช่น "เดินหน้า 5 วินาที" หรือ "เลี้ยวซ้าย 3 วิ"
  - **Robust Audio Handling:** บันทึกเสียงด้วย Sample Rate ที่ฮาร์ดแวร์รองรับ และแปลง (Resample) ให้เหมาะสมกับโมเดล ASR โดยอัตโนมัติ เพื่อลดปัญหาด้านความเข้ากันได้ของฮาร์ดแวร์
  - **API-Driven:** ลดภาระการใช้ทรัพยากรบนเครื่อง local โดยเรียกใช้ ASR และ LLM ผ่าน API ทำให้ไม่จำเป็นต้องใช้ GPU ที่มีประสิทธิภาพสูง
  - **Structured & Scalable:** โครงสร้างโปรเจกต์แบบมืออาชีพที่ง่ายต่อการบำรุงรักษาและต่อยอด

-----

## 🛠️ การติดตั้ง (Setup)

### 1\. Prerequisites (สิ่งที่ต้องมีก่อน)

  - **Conda:** แนะนำให้ใช้ Conda ในการจัดการ Environment เพื่อแก้ปัญหาเรื่อง Library ที่ซับซ้อน (โดยเฉพาะเรื่องเสียง)
  - **Git:** สำหรับ Clone โปรเจกต์

### 2\. Clone Repository

เปิด Terminal แล้วรันคำสั่ง:
`git clone <your-repository-url>`
`cd voice-robot-agent`

### 3\. สร้างและเปิดใช้งาน Conda Environment

`conda create --name voice-robot-agent python=3.11 -y`
`conda activate voice-robot-agent`

### 4\. ตั้งค่า Environment Variables

โปรเจกต์นี้ต้องการ API Keys 2 ตัวในการทำงาน

1.  สร้างไฟล์ `.env` ขึ้นมาในโฟลเดอร์หลักของโปรเจกต์

2.  ใส่ Keys ของคุณลงไปในไฟล์:

      - `GOOGLE_API_KEY`: รับได้จาก [Google AI Studio](https://aistudio.google.com/app/apikey)
      - `HF_TOKEN`: รับได้จาก [Hugging Face Settings](https://huggingface.co/settings/tokens) (ต้องมีสิทธิ์ "read")

    <!-- end list -->

    ```.env
    GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxx"
    HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```

### 5\. ติดตั้ง Dependencies

การติดตั้งจะแบ่งเป็น 2 ส่วนเพื่อความเสถียร

**ส่วนที่ 1: ติดตั้งไลบรารีเสียงสำหรับ Ubuntu/Linux (The Conda Way)**

**สำคัญมาก:** สำหรับผู้ใช้ Linux เพื่อหลีกเลี่ยงปัญหาเรื่อง `PortAudio` และ `libstdc++` ที่เคยเจอ ให้ใช้คำสั่ง **Conda** ต่อไปนี้ในการติดตั้งไลบรารีที่เกี่ยวข้องกับเสียงทั้งหมด วิธีนี้จะช่วยจัดการ System-level dependency ที่ซับซ้อนให้โดยอัตโนมัติ

```bash
conda install -c conda-forge python-sounddevice soundfile
```

**ส่วนที่ 2: ติดตั้งไลบรารีอื่นๆ ผ่าน `pip`**

สร้างไฟล์ `requirements.txt` แล้วใส่เนื้อหาต่อไปนี้:

```txt
langchain
langgraph
langchain_google_genai
huggingface_hub
numpy
scipy
python-dotenv
```

จากนั้นรันคำสั่งติดตั้ง:

```bash
pip install -r requirements.txt
```

-----

## ▶️ วิธีการใช้งาน

หลังจากติดตั้งและตั้งค่าเรียบร้อยแล้ว ให้รันไฟล์ `main.py` ผ่าน Terminal

`python main.py`

โปรแกรมจะแจ้งให้คุณเริ่มพูดคำสั่งเสียง จากนั้นจะแสดงขั้นตอนการทำงานของ Agent ใน Terminal

-----

## 🗣️ ตัวอย่างคำสั่ง (Example Commands)

คุณสามารถทดลองใช้คำสั่งที่มีพารามิเตอร์ได้หลากหลายรูปแบบ:

  - `"เดินไปข้างหน้า 5 วินาที"`
  - `"ถอยหลังหน่อย"` (Agent จะใช้ค่า Default คือ 2 วินาที)
  - `"turn left for 3 seconds"`
  - `"เลี้ยวขวา 1 วิ"`