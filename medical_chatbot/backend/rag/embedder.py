import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"

EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text: str) -> list[float]:
    response = openai.Embedding.create(
        input=[text],
        engine=EMBEDDING_MODEL
    )
    return response['data'][0]['embedding']