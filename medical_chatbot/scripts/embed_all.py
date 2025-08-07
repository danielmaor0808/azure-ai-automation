import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))  # Adds 'medical_chatbot/' to path

from ..backend.rag.embed_store import embed_and_store

project_root = Path(__file__).resolve().parents[1]
html_dir = project_root / "backend/data"
output_dir = html_dir / "embedded"
output_dir.mkdir(parents=True, exist_ok=True)

for file in html_dir.glob("*.html"):
    print(f"Processing {file.name}...")

    output_file = output_dir / file.with_suffix(".json").name  # ⬅️ new output path
    embed_and_store(str(file), str(output_file))

    print(f"Saved to {output_file}")
