#!/bin/bash

echo "Starting Streamlit app on port 8501..."
streamlit run insurance_extraction/src/app.py &

echo "Starting FastAPI backend on port 8000..."
uvicorn medical_chatbot.backend.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Gradio chatbot UI on port 7860..."
python medical_chatbot/frontend/app_gradio.py
