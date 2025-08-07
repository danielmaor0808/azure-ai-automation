from ocr_client import extract_text_from_pdf
from prompts import hebrew_prompt_template_path, english_prompt_template_path, load_prompt_from_file
from llm_extraction import extract_fields_from_ocr
import re

def extract_first_name_from_text(text: str) -> str:
    """
    Extract first name by finding 'שם פרטי' and taking the next non-empty line.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "שם פרטי" in line:
            # Try next line if it’s not empty and not a label
            for j in range(i+1, min(i+4, len(lines))):  # check up to 3 lines after
                candidate = lines[j].strip()
                if candidate and not any(kw in candidate for kw in ["שם משפחה", "פרטי התובע", "ת.ז"]):
                    return candidate
    return ""

def detect_language(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "הצהרה" in line:
            for j in range(i - 1, max(0, i - 5), -1):
                candidate = lines[j].strip()
                if "האיבר שנפגע" in candidate:
                    continue
                print(f"Checking candidate: {candidate}")
                if candidate:
                    hebrew_count = sum(1 for c in candidate if '\u0590' <= c <= '\u05FF')
                    latin_count = sum(1 for c in candidate if 'a' <= c.lower() <= 'z')
                    if hebrew_count == 0 and latin_count == 0:
                        continue
                    return "english" if latin_count > 1 else "hebrew"

    # default to hebrew
    return "hebrew"

def process_document(file_path: str) -> dict:
    # ocr
    text = extract_text_from_pdf(file_path)

    # detect language
    language = detect_language(text)
    prompt_template_path = hebrew_prompt_template_path if language == "hebrew" else english_prompt_template_path
    prompt_template = load_prompt_from_file(prompt_template_path)

    extracted_fields = extract_fields_from_ocr(text, prompt_template)

    return extracted_fields