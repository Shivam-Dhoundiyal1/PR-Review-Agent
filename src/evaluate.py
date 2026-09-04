"""Evaluate the PR review policies on the labeled benchmark.

The agent receives only a case's evidence while selecting an action. The
actual_state field is read only after the action is selected, for evaluation.
"""

import json
from pathlib import Path

from main import compute_posterior, evaluate_baseline, evaluate_policy_a, evaluate_policy_b


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "labeled_test_cases.json"
RESULTS_PATH = PROJECT_ROOT / "results" / "policy_results.json"

STATES = ["Safe", "Minor Defect", "Major Defect"]
ACTIONS = ["Merge", "Request Human Review", "Decline / Block"]

COSTS = {
    "Merge": {"Safe": 0, "Minor Defect": 2, "Major Defect": 100},
    "Request Human Review": {"Safe": 1, "Minor Defect": 1, "Major Defect": 5},
    "Decline / Block": {"Safe": 5, "Minor Defect": 2, "Major Defect": 0},
}


def expected_action(actual_state):
    """Return the conservative benchmark action for a hidden state."""
    if actual_state == "Safe":
        return "Merge"
    if actual_state == "Minor Defect":
        return "Request Human Review"
    return "Decline / Block"


def choose_actions(evidence):
    """Select all policy actions using evidence only."""
    posterior_major = compute_posterior(evidence)
    return {
        "posterior_major_percent": posterior_major,
        "baseline": evaluate_baseline(evidence),
        "policy_a": evaluate_policy_a(posterior_major),
        "policy_b": evaluate_policy_b(posterior_major),
    }


def evaluate_policy(cases, policy_name):
    """Evaluate one policy after all actions have been selected."""
    policy_results = []
    confusion_matrix = {state: {action: 0 for action in ACTIONS} for state in STATES}
    action_counts = {action: 0 for action in ACTIONS}
    total_cost = 0
    errors = 0

    for case in cases:
        actions = choose_actions(case["evidence"])
        action = actions[policy_name]

        # The hidden label is intentionally used only after action selection.
        actual_state = case["actual_state"]
        expected = expected_action(actual_state)
        cost = COSTS[action][actual_state]
        is_error = action != expected

        confusion_matrix[actual_state][action] += 1
        action_counts[action] += 1
        total_cost += cost
        errors += int(is_error)
        policy_results.append({
            "case_id": case["case_id"],
            "evidence": case["evidence"],
            "posterior_major_percent": actions["posterior_major_percent"],
            "action": action,
            "actual_state": actual_state,
            "expected_action": expected,
            "decision_cost": cost,
            "is_error": is_error,
        })

    return {
        "cases": policy_results,
        "confusion_matrix": confusion_matrix,
        "action_counts": action_counts,
        "error_count": errors,
        "human_review_rate": round(action_counts["Request Human Review"] / len(cases), 4),
        "total_decision_cost": total_cost,
    }


def main():
    with DATA_PATH.open(encoding="utf-8") as data_file:
        cases = json.load(data_file)

    results = {
        "dataset": "synthetic-pr-review-v1",
        "case_count": len(cases),
        "cost_matrix": COSTS,
        "policies": {
            "baseline": evaluate_policy(cases, "baseline"),
            "policy_a": evaluate_policy(cases, "policy_a"),
            "policy_b": evaluate_policy(cases, "policy_b"),
        },
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8") as results_file:
        json.dump(results, results_file, indent=2)

    for policy_name, policy_result in results["policies"].items():
        print(
            f"{policy_name}: errors={policy_result['error_count']}, "
            f"review_rate={policy_result['human_review_rate']:.2%}, "
            f"total_cost={policy_result['total_decision_cost']}"
        )
    print(f"Saved results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
