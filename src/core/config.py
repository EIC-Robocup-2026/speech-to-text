# src/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
ROBOT_IP = os.getenv("ROBOT_IP") # <-- เพิ่มบรรทัดนี้

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found.")
if not HF_TOKEN:
    raise ValueError("Hugging Face token not found.")
if not ROBOT_IP: # <-- เพิ่มการตรวจสอบ
    raise ValueError("Robot IP address not found. Please set ROBOT_IP in your .env file.")