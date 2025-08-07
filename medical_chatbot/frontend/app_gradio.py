import gradio as gr
import requests
import json
from typing import Optional, Literal
from pydantic import BaseModel, Field

# endpoint of backend
BACKEND_URL = "http://127.0.0.1:8000/chat/"

USER_INFO = {
    "first_name": "",
    "last_name": "",
    "id_number": "",
    "gender": "",
    "age": None,
    "hmo": "",
    "card_number": "",
    "membership_tier": ""
}

CURRENT_PHASE = "info_collection"

def sanitize_user_info(info_dict):
    return {k: (v if v not in ["", None] else None) for k, v in info_dict.items()}


def chat_with_bot(message, history):
    global USER_INFO, CURRENT_PHASE

    history_texts = [msg["content"] for msg in history if msg["role"] == "user"]

    payload = {
        "user_info": sanitize_user_info(USER_INFO),
        "history": history_texts,
        "message": message,
        "phase": CURRENT_PHASE
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            answer = response_data["answer"]

            # update info
            updated_info = response_data.get("user_info", {})
            if updated_info:
                USER_INFO.update(updated_info)

            # update phase
            updated_phase = response_data.get("phase")
            if updated_phase:
                CURRENT_PHASE = updated_phase

        else:
            answer = f"Error: {response.status_code}\n{response.json().get('detail')}"

    except Exception as e:
        answer = str(e)

    return answer




chatbot = gr.ChatInterface(
    fn=chat_with_bot,
    title=" קופת חולים - Chatbot",
    description="שאל את הצ'אט על השירותים שמגיעים לך",
    theme="default",
    type="messages"
)

if __name__ == "__main__":
    print("Gradio chatbot available at http://localhost:7861", flush=True)
    chatbot.launch(server_name="0.0.0.0", server_port=7860)

