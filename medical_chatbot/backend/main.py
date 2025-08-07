from fastapi import FastAPI
from medical_chatbot.backend.routers import chat

app = FastAPI(
    title="HMO Chatbot Microservice",
    description="Answers questions about Israeli health fund services.",
    version="1.0.0"
)

app.include_router(chat.router, prefix="/chat")
