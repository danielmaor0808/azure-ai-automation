import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

hebrew_prompt_template_path = os.path.join(SCRIPT_DIR, "prompt_templates", "hebrew_prompt_template.txt")
english_prompt_template_path = os.path.join(SCRIPT_DIR, "prompt_templates", "english_prompt_template.txt")


def load_prompt_from_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
