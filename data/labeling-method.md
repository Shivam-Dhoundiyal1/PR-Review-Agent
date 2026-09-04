# Test-Case Labeling Method

## Dataset

`labeled_test_cases.json` contains 30 synthetic PR-review cases. This satisfies the assignment requirement for 30 to 50 labeled or simulated cases.

## Observable evidence

The agent receives only the `evidence` object for a case:

- `CI`: Pass or Fail.
- `Scope`: Small, Medium, or Large.
- `Sensitivity`: Low or High.
- `Author`: High or Low.

## Hidden label

The `actual_state` field is the scenario ground truth and is hidden from the decision function until evaluation:

- `Safe`: The change has no important regression or security problem.
- `Minor Defect`: The change has a non-breaking defect.
- `Major Defect`: The change has a breaking bug, security vulnerability, data corruption risk, or outage risk.

## How labels were assigned

These are simulated cases, not claims about real production PRs. Each label was assigned from the scenario description before policy evaluation. The scenarios deliberately include safe, minor-defect, and major-defect cases with both low-risk and high-risk observable evidence. This allows the policies to make mistakes that can be examined later.

The labels are not generated from the agent's posterior or action. The evaluation must first pass only `evidence` to the agent, save the action and posterior, and use `actual_state` afterward to calculate metrics and costs.

## Dataset metadata

- Dataset version: `synthetic-pr-review-v1`
- Case count: 30
- Label classes: Safe, Minor Defect, Major Defect
- Label source: Scenario ground truth designed for this course experiment
- Real-world status: Simulated; not evidence of actual repository defect rates
- Creation date: 2026-09-04

## Limitation

Because these labels are simulated, the results demonstrate policy behavior on a controlled benchmark rather than real-world PR-review performance. The final report must state this limitation and must not present the results as production accuracy.
