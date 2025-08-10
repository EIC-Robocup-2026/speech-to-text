from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.config import GOOGLE_API_KEY

def get_llm():
    """
    สร้างและคืนค่า LLM client โดยใช้โมเดล Gemini 1.5 Flash ผ่าน API
    """
    model_name = "gemini-2.5-flash"
    print(f"Initializing LLM with Google API: {model_name}")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=GOOGLE_API_KEY,
        convert_system_message_to_human=True
    )
    return llm