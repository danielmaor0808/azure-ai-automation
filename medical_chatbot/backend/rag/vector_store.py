import json
from pathlib import Path
from typing import List, Dict
import numpy as np
from numpy.linalg import norm

# load all embeddings to memory
def load_embeddings_from_dir(directory: str) -> List[Dict]:
    all_chunks = []
    for path in Path(directory).glob("*.json"):
        with open(path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            for item in chunks:
                item["embedding"] = np.array(item["embedding"])  # Convert to NumPy for cosine sim
                all_chunks.append(item)
    return all_chunks

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def search_similar_chunks(query_embedding, all_chunks, top_k=3):
    scored = [
        (cosine_similarity(query_embedding, chunk["embedding"]), chunk["text"])
        for chunk in all_chunks
    ]
    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]