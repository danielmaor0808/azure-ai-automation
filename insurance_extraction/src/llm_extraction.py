import openai
from dotenv import load_dotenv
from openai import AzureOpenAI
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",  # or the correct one for your deployment
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g. "https://oai-lab-test-eastus-001.openai.azure.com/"
)

def extract_fields_from_ocr(text: str, prompt_template: str) -> dict:
    prompt = prompt_template.format(text=text)

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),  # 'gpt-4o' in your case
        messages=[
            {"role": "system", "content": "You are an assistant for form field extraction."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content
    return answer
