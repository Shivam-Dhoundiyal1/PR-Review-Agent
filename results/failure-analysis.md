# Failure Analysis

## Evaluation Context

This analysis uses the 30 simulated cases in `data/labeled_test_cases.json` and the saved policy output in `results/policy_results.json`. The expected action is a benchmark rule used only for analysis:

- Safe -> Merge
- Minor Defect -> Request Human Review
- Major Defect -> Decline / Block

The costs are the project cost matrix. A cost of 100 represents the simulated consequence of merging a Major Defect.

## Five Incorrect Decisions

| Case | Policy | Evidence | Hidden state | Selected action | Expected action | Posterior major-defect risk | Cost | Failure condition |
| :--- | :--- | :--- | :--- | :--- | :--- | ---: | ---: | :--- |
| TC-17 | Policy A | Pass CI, Small, High sensitivity, High-trust author | Major Defect | Merge | Decline / Block | 0.26% | 100 | Passing CI and author trust hid a sensitive security defect |
| TC-03 | Policy A | Pass CI, Large, High sensitivity, High-trust author | Major Defect | Merge | Decline / Block | 5.91% | Large sensitive change was under-escalated |
| TC-23 | Policy A | Pass CI, Large, High sensitivity, High-trust author | Major Defect | Merge | Decline / Block | 5.91% | Infrastructure risk was not represented strongly enough by the posterior |
| TC-30 | Policy A | Pass CI, Large, High sensitivity, High-trust author | Major Defect | Merge | Decline / Block | 5.91% | Data-deletion risk was treated as ordinary high-sensitivity work |
| TC-14 | Policy B | Pass CI, Medium, High sensitivity, Low-trust author | Major Defect | Request Human Review | Decline / Block | 14.45% | Caution was insufficient for a major defect above the review range |

## Analysis

### 1. Passing CI and author trust hid a sensitive security defect

Policy A merged TC-17 even though the case was labeled Major Defect. The small diff, passing CI, and high-trust author reduced the calculated posterior to 0.26%. The model does not include an independent security verification signal, so a small sensitive change can look safe. The simulated cost is 100 because the defect is merged. A possible design change is to require human review or an additional security check for sensitive paths, regardless of the posterior.

### 2. Large sensitive change was under-escalated

Policy A merged TC-03 with a 5.91% major-defect posterior. The evidence included a large authentication change, but the 8% merge threshold allowed the merge. The cost is 100. A possible design change is to add a hard review gate for large high-sensitivity changes before applying the Bayesian threshold.

### 3. Infrastructure risk was not represented strongly enough

Policy A merged TC-23 with the same evidence pattern and cost 100. This demonstrates that the current sensitivity category is too broad: infrastructure changes and ordinary application changes are treated alike. A possible design change is to split `Sensitivity=High` into security, data, payment, and infrastructure categories with separate likelihoods and costs.

### 4. Data-deletion risk was treated as ordinary high-sensitivity work

Policy A merged TC-30 with a 5.91% posterior and cost 100. The current input does not distinguish reversible changes from destructive data operations. A possible design change is to add a `Reversibility` or `DestructiveOperation` evidence field and require human review or blocking for destructive changes.

### 5. Review was not strict enough for a major defect

Policy B sent TC-14 to human review instead of blocking it. Human review is safer than merging, so the cost is 5 rather than 100, but the benchmark expected a block for a Major Defect. The failure indicates that Policy B's 20% block threshold still permits high-risk cases into a review queue. A possible design change is to use expected cost directly instead of a single major-defect threshold, or lower the block threshold for high-sensitivity, low-trust cases.

## Highest-Cost Error

The highest-cost failure is an automatic merge of a Major Defect. It costs 100 in the project matrix. Policy A makes this error on TC-03, TC-17, TC-23, and TC-30. Policy B makes the same error on TC-17. This is more costly than an unnecessary review or an unnecessary block because a merged major defect can cause an outage, security incident, or data loss.

## Limitation

These failure conditions come from simulated labels and a small controlled benchmark. They demonstrate weaknesses in the current policy and feature design; they do not prove that the same PR categories cause defects in production. The next experiment should add more realistic labels or independent human review before making claims about real-world performance.
