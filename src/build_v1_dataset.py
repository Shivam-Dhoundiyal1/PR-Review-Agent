"""Build the separate V1 benchmark from the fixed V0 scenarios.

The hidden labels are inherited from the synthetic V0 scenarios. New evidence
fields are benchmark annotations for exploratory V1 comparison, not production
measurements or independently labeled historical data.
"""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
V0_PATH = PROJECT_ROOT / "data" / "labeled_test_cases.json"
V1_PATH = PROJECT_ROOT / "data" / "v1_labeled_test_cases.json"

FLAKY_CI_CASES = {"TC-04", "TC-11", "TC-15", "TC-22", "TC-27"}
DOMAIN_MISMATCH_CASES = {"TC-03", "TC-05", "TC-11", "TC-17", "TC-23", "TC-30"}
LONG_REVIEW_CASES = {"TC-03", "TC-05", "TC-11", "TC-17", "TC-19", "TC-21", "TC-23", "TC-26", "TC-30"}
HIGH_REVERT_CASES = {"TC-03", "TC-11", "TC-17", "TC-21", "TC-23", "TC-26", "TC-30"}
ACTIONABLE_COMMENT_CASES = {"TC-02", "TC-03", "TC-05", "TC-07", "TC-11", "TC-14", "TC-17", "TC-19", "TC-21", "TC-23", "TC-26", "TC-29", "TC-30"}
NOISY_COMMENT_CASES = {"TC-04", "TC-13", "TC-15", "TC-22", "TC-27"}


def build_evidence(case):
    case_id = case["case_id"]
    old_evidence = case["evidence"]
    if case_id in NOISY_COMMENT_CASES:
        review_comments = "Noisy"
    elif case_id in ACTIONABLE_COMMENT_CASES:
        review_comments = "Actionable"
    else:
        review_comments = "Clean"

    return {
        **old_evidence,
        "CIReliability": "Flaky" if case_id in FLAKY_CI_CASES else "Stable",
        "AuthorDomain": "Mismatch" if case_id in DOMAIN_MISMATCH_CASES else "Match",
        "ReviewLatency": "Long" if case_id in LONG_REVIEW_CASES else "Short",
        "RevertRate": "High" if case_id in HIGH_REVERT_CASES else "Low",
        "ReviewComments": review_comments,
    }


def main():
    with V0_PATH.open(encoding="utf-8") as input_file:
        v0_cases = json.load(input_file)

    v1_cases = [
        {
            "case_id": f"V1-{case['case_id']}",
            "source_case_id": case["case_id"],
            "description": case["description"],
            "evidence": build_evidence(case),
            "actual_state": case["actual_state"],
            "label_source": "Inherited synthetic scenario label from V0",
        }
        for case in v0_cases
    ]

    with V1_PATH.open("w", encoding="utf-8") as output_file:
        json.dump(v1_cases, output_file, indent=2)
        output_file.write("\n")

    print(f"Saved {len(v1_cases)} V1 cases to {V1_PATH}")


if __name__ == "__main__":
    main()
