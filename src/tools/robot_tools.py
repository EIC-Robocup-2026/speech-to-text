# src/tools/robot_tools.py
import requests
import pyttsx3  # <-- เพิ่ม import
from typing import Literal
from langchain_core.tools import tool
from src.core.config import ROBOT_IP

# --- 1. ตั้งค่า TTS Engine ---
# สร้าง engine แค่ครั้งเดียวเพื่อประสิทธิภาพ
try:
    tts_engine = pyttsx3.init()
except Exception as e:
    print(f"Warning: Could not initialize TTS engine. TTS will be disabled. Error: {e}")
    tts_engine = None

def _speak(text: str):
    """Helper function to speak the given text using the TTS engine."""
    if tts_engine:
        try:
            print(f"🔊 TTS: Speaking '{text}'")
            # สั่งให้ engine พูดข้อความ
            tts_engine.say(text)
            # รอให้พูดจนจบ
            tts_engine.runAndWait()
        except Exception as e:
            print(f"Warning: TTS failed to speak. Error: {e}")
    else:
        # กรณีที่ TTS engine ไม่พร้อมใช้งาน
        print(f"🔊 TTS (disabled): {text}")


def _send_robot_command(action: str, duration_seconds: float, speed_percent: int) -> str:
    """
    Helper function to send a command to the robot via its API.
    """
    base_url = f"http://{ROBOT_IP}/move"
    duration_ms = int(duration_seconds * 1000)
    params = {
        "action": action,
        "duration": duration_ms,
        "speed": speed_percent
    }
    try:
        print(f"🤖 Sending command to robot: {action}, Duration: {duration_seconds:.2f}s, Speed: {speed_percent}%")
        response = requests.get(base_url, params=params, timeout=5)
        if response.status_code == 200:
            print(f"✅ Robot response: {response.text}")
            return f"Command '{action}' executed successfully."
        else:
            print(f"❌ Error from robot: {response.status_code} - {response.text}")
            return f"Robot returned an error for action '{action}'."
    except requests.exceptions.RequestException as e:
        print(f"🔥 FAILED to connect to robot at {ROBOT_IP}. Error: {e}")
        return "Could not send command to robot. Please check connection."


@tool
def move_robot(direction: Literal["forward", "backward"], duration_seconds: int = 2, speed_percent: int = 70):
    """
    Sends a command to move the robot forward or backward.
    """
    # --- 2. สร้างข้อความและสั่งให้ TTS พูด ---
    tts_message = f"Moving {direction} for {duration_seconds} seconds"
    _speak(tts_message)
    
    return _send_robot_command(action=direction, duration_seconds=duration_seconds, speed_percent=speed_percent)


@tool
def turn_robot(direction: Literal["left", "right"], duration_seconds: int = 1, speed_percent: int = 70):
    """
    Sends a command to turn the robot left or right for a specified duration.
    """
    # --- 2. สร้างข้อความและสั่งให้ TTS พูด ---
    tts_message = f"Turning {direction} for {duration_seconds} seconds"
    _speak(tts_message)

    return _send_robot_command(action=direction, duration_seconds=duration_seconds, speed_percent=speed_percent)


@tool
def spin_robot(direction: Literal["left", "right"], degrees: int, speed_percent: int = 70):
    """
    Spins the robot left or right by a specific number of degrees.
    """
    # --- 2. สร้างข้อความและสั่งให้ TTS พูด ---
    tts_message = f"Spinning {direction} for {degrees} degrees"
    _speak(tts_message)

    duration_seconds = degrees / 90.0
    return _send_robot_command(action=direction, duration_seconds=duration_seconds, speed_percent=speed_percent)


robot_tool_list = [move_robot, turn_robot, spin_robot]
