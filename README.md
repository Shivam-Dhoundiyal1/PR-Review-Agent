# PR Review Agent

## 1. Final Problem Statement

The agent observes pull-request evidence and selects **Merge**, **Request Human Review**, or **Decline / Block** because the true defect state is hidden until further testing or human review.

## 2. Project Objective

The project tests whether Bayesian risk estimates and cost-sensitive decision thresholds can make safer PR decisions than a simple rule-based baseline. The agent is a decision system, not only a chatbot: it must select an action and record feedback about that action.

## 3. Design Versions

### Agent V0: Evaluated baseline design

V0 uses four observable signals: CI status, diff scope, file sensitivity, and author history. It estimates the hidden defect state with a Bayesian model and passes the major-defect posterior to the existing Baseline, Policy A, and Policy B decision rules. The reported benchmark results use this version.

### Agent V1: Reddit-informed design

V1 preserves the V0 policies and adds design requirements based on Reddit feedback:

- Treat author history as a conditional signal; domain experience may not transfer from frontend work to infrastructure or other high-risk areas.
- Track CI reliability and flaky-test history instead of treating every pass or failure as equally reliable.
- Consider review latency, revert rate, and filtered review-comment signals as future evidence features.
- Keep the Bayesian posterior separate from the LLM. The LLM may extract or explain evidence, but it must not rewrite the posterior or final action.
- Keep API-rate-limit handling outside the V1 defect model; it is a data-collection concern rather than a PR-risk signal.

V1 uses provisional likelihoods for exploratory comparison. Its labels are inherited from the synthetic V0 scenarios, so the results do not establish production performance. Baseline, Policy A, and Policy B remain unchanged so the existing V0 benchmark stays comparable.

## 4. Agent Specification

### Observable Input

Each PR provides these evidence fields:

| Field | Allowed values | Meaning |
| :--- | :--- | :--- |
| `CI` | `Pass`, `Fail` | Whether the available CI checks pass. |
| `Scope` | `Small`, `Medium`, `Large` | Total changed lines: below 50, 50-300, or above 300. |
| `Sensitivity` | `Low`, `High` | Whether changed paths are low-risk UI/docs or sensitive auth, database, payment, security, or infrastructure paths. |
| `Author` | `High`, `Low` | Whether the author has at least 50 previously merged PRs. |

### Hidden State

The true state is not visible when the decision is made:

- **Safe:** No important regression or security problem is introduced.
- **Minor Defect:** A non-breaking problem exists, such as technical debt, style problems, or a minor logging defect.
- **Major Defect:** A breaking bug, security vulnerability, data corruption, or production outage risk exists.

### Actions

- **Merge:** Merge the PR without additional human review.
- **Request Human Review:** Send the PR to a senior developer for review before merging or blocking.
- **Decline / Block:** Do not merge the PR until the author provides a correction or new evidence.

### Belief and Decision Rule

The agent calculates a posterior probability for each hidden state using the prior probabilities and the four observed evidence fields. Policy A uses the posterior probability of a major defect:

- Below 8%: `Merge`
- From 8% through 45%: `Request Human Review`
- Above 45%: `Decline / Block`

Policy B uses the same posterior but is more cautious:

- Below 2%: `Merge`
- From 2% through 20%: `Request Human Review`
- Above 20%: `Decline / Block`

The baseline does not use Bayesian probabilities: it blocks failed CI, requests human review for high-sensitivity or large changes, and merges the remaining cases.

### Human Reasoning and Feedback

The agent identifies uncertainty through its posterior risk and sends high-cost or borderline cases to a human. After a human review or later test result, the result is recorded with the case ID, selected action, and observed hidden state. These records are retained as feedback for later review of the priors, likelihoods, thresholds, and failure conditions. The agent does not use the hidden label before making its original decision.

## 5. Cost Principle

An incorrect merge of a major defect has the highest cost because it can cause a production outage, security incident, or data loss. An unnecessary human review costs developer time. Blocking a safe PR costs developer time and delays delivery. The experiment will compare these costs for the baseline, Policy A, and Policy B.

## 6. Initial Evaluation Results

The experiment uses 30 simulated cases from `data/labeled_test_cases.json`. For these metrics, an unsafe case is a Minor or Major Defect, and an unsafe prediction is Request Human Review or Decline / Block. The hidden label is used only after each policy selects its action.

| Policy | True positives | True negatives | False positives | False negatives | Precision | Recall | Human-review rate | Total decision cost |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 17 | 5 | 5 | 3 | 77.27% | 85.00% | 53.33% | 56 |
| Policy A | 8 | 10 | 0 | 12 | 100.00% | 40.00% | 16.67% | 439 |
| Policy B | 14 | 9 | 1 | 6 | 93.33% | 70.00% | 33.33% | 142 |

Policy A has no false positives in this benchmark, but its 12 false negatives include unsafe cases that it merged, producing the highest cost. Policy B has a better cost and recall trade-off than Policy A, but the baseline has the lowest total cost on this simulated dataset. These results are preliminary: the cases and labels are simulated, and the benchmark is too small to support claims about production performance. The complete output is saved in `results/metrics.json`.

## 7. Failure Analysis

Five incorrect decisions are documented in `results/failure-analysis.md`. The highest-cost failure is an automatic merge of a Major Defect, with cost 100 in the project matrix. Policy A makes this error on TC-03, TC-17, TC-23, and TC-30; Policy B makes it on TC-17. The main design weaknesses are that passing CI and author trust can suppress risk, and the current `Sensitivity` field does not distinguish security, infrastructure, payment, and destructive data changes. These results are based on simulated labels and are not production-performance claims.

## 8. V1 Exploratory Evaluation

V1 is evaluated separately on `data/v1_labeled_test_cases.json`, which extends the V0 scenarios with CI reliability, domain-aware author matching, review latency, revert rate, and filtered review-comment signals. The hidden labels are inherited synthetic scenario labels, not independent historical labels.

| Policy | Precision | Recall | False positives | False negatives | Human-review rate | V1 decision cost |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 77.27% | 85.00% | 5 | 3 | 53.33% | 92 |
| Policy A | 100.00% | 40.00% | 0 | 12 | 16.67% | 421 |
| Policy B | 100.00% | 50.00% | 0 | 10 | 10.00% | 276 |

The complete V1 confusion matrices, per-case posteriors, and Brier scores are saved in `results/v1_metrics.json` and `results/v1_policy_results.json`. V1 costs use a separate provisional cost matrix, so V0 and V1 total costs should not be compared as if they used the same units.