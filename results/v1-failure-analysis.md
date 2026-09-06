# V1 Failure Analysis

## Evaluation Context

This analysis uses the 30 exploratory V1 cases in `data/v1_labeled_test_cases.json` and the saved outputs in `results/v1_policy_results.json`. V1 keeps the V0 policy thresholds but adds CI reliability, domain-aware author matching, review latency, revert rate, and filtered review-comment signals.

The expected action is a benchmark rule used only after the policy action is selected:

- Safe -> Merge
- Minor Defect -> Request Human Review
- Major Defect -> Decline / Block

V1 uses this cost matrix:

| Action | Safe | Minor Defect | Major Defect |
| :--- | ---: | ---: | ---: |
| Merge | 0 | 3 | 120 |
| Request Human Review | 2 | 2 | 8 |
| Decline / Block | 6 | 3 | 0 |

## Five Incorrect Decisions

| Case | Policy | Key V1 evidence | Hidden state | Selected action | Expected action | Major-defect posterior | Cost | Failure condition |
| :--- | :--- | :--- | :--- | :--- | :--- | ---: | ---: | :--- |
| V1-TC-17 | Policy A | Pass CI, small high-sensitivity change, high author experience but domain mismatch, long review latency, high revert rate | Major Defect | Merge | Decline / Block | 4.12% | 120 | Domain mismatch and negative history did not overcome the low posterior |
| V1-TC-14 | Policy A | Pass CI, medium high-sensitivity change, low author experience, domain match, actionable comments | Major Defect | Merge | Decline / Block | 1.32% | 120 | Domain match and stable history suppressed risk too strongly |
| V1-TC-08 | Policy A | Failed CI, small high-sensitivity change, stable CI, domain match, clean comments | Major Defect | Merge | Decline / Block | 120 | CI failure was outweighed by otherwise favorable evidence |
| V1-TC-30 | Policy A | Pass CI, large high-sensitivity change, domain mismatch, long review latency, high revert rate, actionable comments | Major Defect | Request Human Review | Decline / Block | 32.02% | 8 | Policy A's 45% block threshold was too high for a concentrated high-risk profile |
| V1-TC-22 | Policy B | Pass CI, small low-sensitivity change, flaky CI, noisy comments | Minor Defect | Merge | Request Human Review | 0.02% | 3 | Minor-defect risk is not represented by the major-defect-only threshold |

## Analysis

### 1. Domain mismatch was not strong enough for a sensitive change

Policy A merged V1-TC-17 even though the hidden state was Major Defect. The case has high sensitivity, domain mismatch, long review latency, high revert rate, and actionable review comments. However, the small scope and passing, stable CI kept the major-defect posterior at 4.12%, below the 8% merge threshold. The cost is 120 because a Major Defect was merged. A possible V2 change is to add a hard review gate for domain-mismatched high-sensitivity changes or calibrate the domain likelihoods with independent labels.

### 2. Domain match created excessive confidence

Policy A merged V1-TC-14 with a 1.32% major-defect posterior. Domain match, short review latency, low revert rate, stable CI, and medium scope outweighed the high-sensitivity path and actionable comments. The hidden state was Major Defect, producing cost 120. This shows that domain familiarity should reduce uncertainty but should not override strong path-risk or review evidence. A possible change is to cap the confidence benefit from domain match when sensitivity is high.

### 3. Failed CI did not guarantee a safe action

Policy A and Policy B both merged V1-TC-08, a Major Defect, despite failed CI. The V1 annotations marked the CI history as stable, the author domain as matched, and the review comments as clean. The posterior was only 0.10%, but the hidden defect cost is 120. This exposes a weakness in multiplying many independent likelihoods: favorable signals can cancel a critical failure. A possible change is a hard block or mandatory human review whenever CI fails, before applying the posterior threshold.

### 4. High-risk evidence remained below the block threshold

Policy A sent V1-TC-30 to human review with a 32.02% major-defect posterior, although the hidden state was Major Defect. The case includes a large high-sensitivity change, domain mismatch, long review latency, high revert rate, and actionable comments. The review action costs 8, which is safer than merging but still differs from the benchmark's expected block. A possible change is a lower block threshold for large, high-sensitivity, domain-mismatched changes or an expected-cost decision rule.

### 5. Major-defect-only thresholds missed a Minor Defect

Policy B merged V1-TC-22, whose hidden state was Minor Defect. Its major-defect posterior was only 0.02%, so the policy's major-defect threshold selected Merge. However, the case had flaky CI and noisy review comments, which indicate uncertainty even when major-defect risk is low. The cost is 3. A possible change is to include the full posterior distribution or a separate uncertainty rule so minor-defect evidence can trigger human review.

## Highest-Cost Error

The highest-cost V1 failures are automatic merges of Major Defects. Each costs 120 under the V1 matrix. Policy A makes this error on V1-TC-17, V1-TC-14, and V1-TC-08; Policy B makes it on V1-TC-14 and V1-TC-08. These errors dominate the V1 cost because the benchmark assigns the largest penalty to merging a Major Defect.

## Limitation

The V1 labels are inherited from the synthetic V0 scenarios, and the additional evidence fields are benchmark annotations rather than independently collected historical measurements. The failure analysis therefore demonstrates behavior of the exploratory model; it does not establish that these signals or failure patterns predict production defects.
