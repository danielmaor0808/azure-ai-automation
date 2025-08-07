import json
import re
from pathlib import Path

from processing_pipeline import process_document
from validation import evaluate_output

def clean_json_block(gpt_response: str) -> str:
    match = re.search(r"```json\s*(.*?)\s*```", gpt_response, re.DOTALL)
    return match.group(1).strip() if match else gpt_response.strip()

pdf_path = Path("data/283_ex2.pdf")
output_path = Path("outputs/283_ex2.json")
gt_path = Path("data/ground_truth/283_ex2.json")

raw_prediction = process_document(pdf_path)  # Returns string (not dict)
cleaned = clean_json_block(raw_prediction)

try:
    prediction = json.loads(cleaned)
except json.JSONDecodeError as e:
    raise e

# save predictions
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(prediction, f, ensure_ascii=False, indent=2)

# loads
with open(gt_path, "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# evaluate
result = evaluate_output(prediction, ground_truth)

# print results
print(f"Accuracy: {result['accuracy'] * 100:.2f}%")
if result["mismatches"]:
    print("Mismatches:")
    for key, diff in result["mismatches"].items():
        print(f"  - {key}: expected '{diff['expected']}', got '{diff['predicted']}'")
else:
    print("All fields match the ground truth!")
