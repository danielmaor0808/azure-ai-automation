from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

endpoint = os.getenv('AZURE_FORMRECOGNIZER_ENDPOINT')
key = os.getenv('AZURE_FORMRECOGNIZER_KEY')

# instantiate client
ocr_client = DocumentAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def extract_text_from_pdf(file_path: str) -> str:
    with open(file_path, "rb") as f:
        poller = ocr_client.begin_analyze_document("prebuilt-layout", document=f)
        result = poller.result()

    text = ""
    for page in result.pages:
        for line in page.lines:
            text += line.content + "\n"
    return text