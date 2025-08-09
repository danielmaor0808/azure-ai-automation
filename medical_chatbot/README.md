# KPMG - Home Assignment

This repository contains two separate applications:

1. **Insurance Extraction** – A Streamlit app for extracting structured fields from scanned insurance documents.
2. **Medical Chatbot** – A Gradio + FastAPI based chatbot for answering user queries about available health fund services.

Both apps are containerized and can be run together with a single Docker command.

---

## 1. How to Run

Make sure you have Docker installed and running. Then, from the project root:

```bash
docker build -t kpmg-assignment .
docker run --env-file .env -p 8501:8501 -p 8000:8000 -p 7861:7860 kpmg-assignment
```
### Accessing the Apps

| App                                | Host URL                                             | Notes                                       |
|------------------------------------|------------------------------------------------------|---------------------------------------------|
| Insurance Extraction (Streamlit)   | [http://localhost:8501](http://localhost:8501)       | Main UI for document processing             |
| Medical Chatbot (FastAPI backend)  | [http://localhost:8000/docs](http://localhost:8000/docs) | API docs for the chatbot backend            |
| Medical Chatbot (Gradio frontend)  | [http://localhost:7861](http://localhost:7861)       | Chat UI for interacting with the bot        |

## 2. Notes on Insurance Extraction

- **Accuracy:** *86.6%* – Calculated as the ratio of correctly extracted fields to total fields across the evaluation dataset.

  Formula:
```markdown
  accuracy = (number_of_correct_extractions / total_number_of_fields) * 100
```

## 3. Notes on Medical Chatbot

- To start the conversation, **the user should first say "hello" (or a similar greeting)** without providing personal details yet.
- The chatbot will then guide the user through information collection before answering queries.

## Environment Variables

The applications require the following environment variables to be set in a `.env` file at the project root:

- `AZURE_FORMRECOGNIZER_ENDPOINT` – Endpoint URL for Azure Form Recognizer.
- `AZURE_FORMRECOGNIZER_KEY` – API key for Azure Form Recognizer.
- `AZURE_OPENAI_ENDPOINT` – Endpoint URL for Azure OpenAI service.
- `AZURE_OPENAI_KEY` – API key for Azure OpenAI service.
- `AZURE_OPENAI_DEPLOYMENT_ID` – Deployment ID for the Azure OpenAI chat/completion model.
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID` – Deployment ID for the Azure OpenAI embedding model.


