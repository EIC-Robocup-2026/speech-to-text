# src/agent/graph.py
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.tools.robot_tools import robot_tool_list
from src.services.llm_service import get_llm
from src.services.asr_service import record_and_transcribe_audio

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]

# --- ปรับแก้ System Prompt ---
# กำหนดบทบาทและจำกัดภาษาให้ชัดเจนยิ่งขึ้น
SYSTEM_PROMPT = "คุณคือผู้ช่วยสำหรับควบคุมหุ่นยนต์ บทบาทของคุณคือรับฟังคำสั่งเสียง แล้วเรียกใช้เครื่องมือที่เหมาะสมเพื่อควบคุมหุ่นยนต์ โปรดเข้าใจคำสั่งที่เป็นภาษาไทยหรือภาษาอังกฤษเท่านั้น และเราจะเรียกคุณว่า อาร์มมี่ "

llm = get_llm()
llm_with_tools = llm.bind_tools(robot_tool_list)
tool_node = ToolNode(robot_tool_list)

def transcribe_node(state: AgentState):
    print("\n🎙️  NODE: ASR Recorder")
    transcription = record_and_transcribe_audio() # เรียกใช้ฟังก์ชันเวอร์ชันเดิม
    if transcription is None or not transcription.strip():
        print("   > Could not understand audio or no speech detected.")
        return {"messages": [("user", "no_input")]}
    return {"messages": [("user", transcription)]}

def agent_node(state: AgentState):
    print("\n🧠 NODE: Agent Decision")
    
    # เพิ่ม System Prompt เข้าไปใน messages
    messages_with_system_prompt = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    
    response = llm_with_tools.invoke(messages_with_system_prompt)
    print(f"   > Agent decision: {response.tool_calls or 'No tool call'}")
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    
    if last_message.content == "no_input":
        return END # ถ้าไม่มีเสียงพูด ให้จบการทำงานในรอบนั้น
        
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return END
        
    return "action"

def create_robot_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("transcribe", transcribe_node)
    workflow.add_node("agent", agent_node)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("transcribe")
    workflow.add_edge("transcribe", "agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "action": "action",
            END: END,
        }
    )
    workflow.add_edge("action", "agent")

    return workflow.compile()