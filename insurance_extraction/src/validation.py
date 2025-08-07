def flatten_dict(d, parent_key="", sep="."):
    """Flatten nested dictionaries into a single level dict with compound keys."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v.strip() if isinstance(v, str) else v))
    return dict(items)


def evaluate_output(predicted: dict, ground_truth: dict) -> dict:
    flat_pred = flatten_dict(predicted)
    flat_gt = flatten_dict(ground_truth)

    all_keys = set(flat_pred) | set(flat_gt)
    total = len(all_keys)
    correct = 0
    mismatches = {}

    for key in all_keys:
        pred_val = flat_pred.get(key, "")
        gt_val = flat_gt.get(key, "")
        if pred_val == gt_val:
            correct += 1
        else:
            mismatches[key] = {"expected": gt_val, "predicted": pred_val}

    accuracy = round(correct / total, 4)
    return {
        "accuracy": accuracy,
        "total_fields": total,
        "correct_fields": correct,
        "mismatches": mismatches,
    }
