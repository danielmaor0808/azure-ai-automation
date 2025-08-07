import os
from openai import AzureOpenAI
from medical_chatbot.backend.models.schemas import ChatRequest, UserInfo
from dotenv import load_dotenv
from medical_chatbot.backend.rag.vector_store import load_embeddings_from_dir, search_similar_chunks
import re
import numpy as np

load_dotenv()

embedded_chunks = load_embeddings_from_dir("data/embedded")


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def update_user_info_from_message(user_info: UserInfo, message: str):
    # update name
    name_match = re.match(r"([\u0590-\u05FFa-zA-Z]{2,})\s+([\u0590-\u05FFa-zA-Z]{2,})", message)
    if name_match and not user_info.first_name and not user_info.last_name:
        user_info.first_name = name_match.group(1)
        user_info.last_name = name_match.group(2)

    # ID
    id_match = re.search(r"\b(\d{9})\b", message)
    if id_match and not user_info.id_number:
        user_info.id_number = id_match.group(1)

    # gender
    if "male" in message.lower() and not user_info.gender:
        user_info.gender = "male"
    elif "female" in message.lower() and not user_info.gender:
        user_info.gender = "female"
    elif "זכר" in message.lower() and not user_info.gender:
        user_info.gender = "זכר"
    elif "נקבה" in message.lower() and not user_info.gender:
        user_info.gender = "נקבה"

    # age
    age_match = re.search(r"\b(\d{2})\b", message)
    if age_match and not user_info.age:
        user_info.age = int(age_match.group(1))

    # HMO
    for hmo in ["מכבי", "מאוחדת", "כללית"]:
        if hmo in message and not user_info.hmo:
            user_info.hmo = hmo

    # card number
    card_match = re.search(r"\b(\d{9})\b", message)
    if card_match and not user_info.card_number and user_info.id_number != card_match.group(1):
        user_info.card_number = card_match.group(1)

    # tier
    for tier in ["זהב", "כסף", "ארד"]:
        if tier in message and not user_info.membership_tier:
            user_info.membership_tier = tier

def get_query_embedding(query: str):
    response = client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"),
        input=query
    )
    return np.array(response.data[0].embedding)


async def ask_openai(payload: ChatRequest) -> str:
    messages = build_chat_messages(payload)
    update_user_info_from_message(payload.user_info, payload.message)

    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
            messages=messages
        )
        return response.choices[0].message.content

    except Exception as e:
        print("Call failed:", str(e))
        return f"[ERROR] {str(e)}"


# message builder
def build_chat_messages(payload: ChatRequest) -> list:
    user = payload.user_info

    if payload.phase == "info_collection":
        system_prompt = (
            "You are a friendly assistant collecting personal information needed to access health fund services in Israel. "
            "Please collect the following fields one at a time:\n"
            "- First and last name\n"
            "- 9-digit ID number\n"
            "- Gender (male/female/זכר/נקבה)\n"
            "- Age (0–120)\n"
            "- Health fund (מכבי, מאוחדת, כללית)\n"
            "- 9-digit HMO card number\n"
            "- Insurance tier (זהב, כסף, ארד)\n"
            "Once all details are collected, confirm them with the user and instruct them to start asking questions about their health services."
        )

        return [
            {"role": "system", "content": system_prompt},
            *[{"role": "user", "content": msg} for msg in payload.history],
            {"role": "user", "content": payload.message}
        ]

    else:
        # embed query
        query_embedding = get_query_embedding(payload.message)

        # retrieve top-k similar knowledge chunks
        top_chunks = search_similar_chunks(query_embedding, embedded_chunks, top_k=4)
        knowledge_context = "\n---\n".join(top_chunks)

        # compose full context
        system_prompt = (
            "You are a helpful assistant answering questions about Israeli health fund services. "
            "Use only the following information from the official health fund knowledge base to answer the user's question. "
            "If the answer is not included in the knowledge base, say you don't know.\n\n"
            f"Relevant knowledge base:\n{knowledge_context}"
        )

        user_profile = (
            f"User profile:\n"
            f"- Name: {user.first_name} {user.last_name}\n"
            f"- ID: {user.id_number}\n"
            f"- Age: {user.age}\n"
            f"- Gender: {user.gender}\n"
            f"- HMO: {user.hmo}\n"
            f"- Tier: {user.membership_tier}"
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_profile},
            *[{"role": "user", "content": msg} for msg in payload.history],
            {"role": "user", "content": payload.message}
        ]
