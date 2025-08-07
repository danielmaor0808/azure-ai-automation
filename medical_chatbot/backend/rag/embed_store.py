import openai
import os
import json
from dotenv import load_dotenv
from .preprocess import extract_text_from_html, chunk_text
from openai import AzureOpenAI

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def embed_and_store(path, output_path):
    all_chunks = []
    text = extract_text_from_html(path)
    chunks = chunk_text(text)
    print(f"{path} produced {len(chunks)} chunks")
    for chunk in chunks:
        response = client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"),
            input=chunk
        )
        embedding = response.data[0].embedding
        all_chunks.append({"text": chunk, "embedding": embedding})
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)



