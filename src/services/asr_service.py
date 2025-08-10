# src/services/asr_service.py
import sounddevice as sd
import soundfile as sf
import io
import numpy as np
from scipy import signal
from huggingface_hub import InferenceClient

from src.core.config import HF_TOKEN

# สร้าง client เพียงครั้งเดียว
client = InferenceClient(token=HF_TOKEN)

# --- กำหนด Sample Rate เป้าหมายและ Sample Rate ที่จะใช้บันทึก ---
TARGET_SR = 16000  # Sample Rate ที่ Whisper ต้องการ
RECORD_SR = 44100  # Sample Rate ที่ฮาร์ดแวร์ส่วนใหญ่รองรับ

def record_and_transcribe_audio(duration=5):
    """
    บันทึกเสียงที่ 44.1kHz แล้ว Resample เป็น 16kHz ก่อนส่งให้ API
    พร้อมทั้งบังคับให้ถอดความเป็นภาษาไทยเท่านั้น
    """
    print(f"   > กรุณาพูดคำสั่งของคุณ ({duration} วินาที)...")
    
    # บันทึกเสียงด้วย RECORD_SR (44100 Hz)
    recording = sd.rec(int(duration * RECORD_SR), samplerate=RECORD_SR, channels=1, dtype='float32')
    sd.wait()
    print("   > บันทึกเสียงเสร็จสิ้น, กำลังประมวลผล...")

    try:
        # ทำการ Resample เสียง
        num_samples = int(len(recording) * TARGET_SR / RECORD_SR)
        resampled_recording = signal.resample(recording, num_samples)

        # จัดการเสียงที่ Resample แล้วในหน่วยความจำ
        buffer = io.BytesIO()
        sf.write(buffer, resampled_recording, TARGET_SR, format='WAV')
        buffer.seek(0)
        
        # --- เพิ่มพารามิเตอร์ language="th" ---
        # บังคับให้โมเดลถอดความเป็นภาษาไทยเท่านั้น
        response = client.automatic_speech_recognition(
            audio=buffer.read(),
            model="openai/whisper-large-v3",
        )
        
        transcription = response['text']
        print(f"   > ข้อความที่ได้ (โหมดภาษาไทย): '{transcription}'")
        return transcription

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเรียกใช้ ASR API: {e}")
        return None
