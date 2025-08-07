import re
from typing import List
import tiktoken

def extract_text_from_html(html_path: str) -> str:
    from bs4 import BeautifulSoup

    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # flatten tables and preserve line breaks
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for td in soup.find_all("td"):
        td.insert_after("\n")

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def chunk_text(text: str, max_tokens: int = 256, overlap: int = 50) -> List[str]:
    enc = tiktoken.encoding_for_model("text-embedding-ada-002")
    tokens = enc.encode(text)


    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += max_tokens - overlap
    return chunks

