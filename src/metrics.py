"""Calculate evaluation metrics from the saved policy results."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "results" / "policy_results.json"
OUTPUT_PATH = PROJECT_ROOT / "results" / "metrics.json"
UNSAFE_STATES = {"Minor Defect", "Major Defect"}


def calculate_policy_metrics(policy_result):
    cases = policy_result["cases"]
    binary = {"true_positive": 0, "true_negative": 0, "false_positive": 0, "false_negative": 0}
    major_defect_brier_total = 0.0

    for case in cases:
        actual_unsafe = case["actual_state"] in UNSAFE_STATES
        predicted_unsafe = case["action"] != "Merge"
        if predicted_unsafe and actual_unsafe:
            binary["true_positive"] += 1
        elif not predicted_unsafe and not actual_unsafe:
            binary["true_negative"] += 1
        elif predicted_unsafe:
            binary["false_positive"] += 1
        else:
            binary["false_negative"] += 1

        predicted_major = case["posterior_major_percent"] / 100
        actual_major = float(case["actual_state"] == "Major Defect")
        major_defect_brier_total += (predicted_major - actual_major) ** 2

    positive_predictions = binary["true_positive"] + binary["false_positive"]
    actual_unsafe_cases = binary["true_positive"] + binary["false_negative"]
    precision = binary["true_positive"] / positive_predictions if positive_predictions else 0.0
    recall = binary["true_positive"] / actual_unsafe_cases if actual_unsafe_cases else 0.0

    return {
        "binary_definition": {
            "positive_actual": "Minor Defect or Major Defect",
            "positive_prediction": "Request Human Review or Decline / Block",
        },
        "binary_confusion_matrix": binary,
        "precision_unsafe": round(precision, 4),
        "recall_unsafe": round(recall, 4),
        "false_positive_quantity": binary["false_positive"],
        "false_negative_quantity": binary["false_negative"],
        "human_review_rate": policy_result["human_review_rate"],
        "total_decision_cost": policy_result["total_decision_cost"],
        "major_defect_brier_score": round(major_defect_brier_total / len(cases), 6),
    }


def main():
    with INPUT_PATH.open(encoding="utf-8") as results_file:
        results = json.load(results_file)

    metrics = {
        "dataset": results["dataset"],
        "case_count": results["case_count"],
        "policies": {
            policy_name: calculate_policy_metrics(policy_result)
            for policy_name, policy_result in results["policies"].items()
        },
    }

    with OUTPUT_PATH.open("w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2)

    for policy_name, policy_metrics in metrics["policies"].items():
        print(
            f"{policy_name}: precision={policy_metrics['precision_unsafe']:.2%}, "
            f"recall={policy_metrics['recall_unsafe']:.2%}, "
            f"false_negatives={policy_metrics['false_negative_quantity']}, "
            f"cost={policy_metrics['total_decision_cost']}"
        )
    print(f"Saved metrics to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
