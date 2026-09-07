# Pending Tasks: PR Review Agent

This file tracks the remaining work for the project. Complete the tasks in order because later tasks depend on earlier decisions and evidence.

## Current Project Status

### Already started

- Problem selected: PR review agent.
- Basic agent design exists in `README.md` and `research-file.md`.
- Bayesian posterior calculation exists in `src/main.py`.
- Three action types exist: Merge, Request Human Review, and Decline / Block.
- Three policies exist in code: baseline, Policy A, and Policy B.
- A probability decision record exists.
- Fifteen synthetic test cases exist in `data/test_cases.md`.
- Thirty-five fetched PR records exist in `data/real_pr_test_cases.json`.
- Reddit and X discussion evidence is recorded in `discussion-record.md`; no further discussion collection is planned.
- V1 has a separate expanded dataset, evaluation, metrics, and failure analysis.

### Important limitation

The fetched dataset currently labels cases as `Merged` or `Closed_Without_Merge`. These are outcomes, not verified hidden defect states. The evaluation needs defensible labels such as `Safe`, `Minor Defect`, or `Major Defect`, or a clearly documented and justified proxy label.

## Evidence Still Required

| Requirement | Current status | Required update |
| :--- | :--- | :--- |
| One specific problem statement | Complete | Final problem is stated in `README.md` and the probability decision record. |
| Agent design | Partially complete | V0 is documented. Create the equivalent V1 flow design with expanded evidence gathering and the LLM/Bayesian boundary. |
| Public discussions | Complete | Reddit and X evidence is recorded; no additional comments are planned. |
| Design updates from discussions | Complete | Accepted, rejected, and deferred findings are recorded in `discussion-record.md`, `README.md`, and the probability decision record. |
| Test cases | Complete for V0 and exploratory V1 | V0 uses `data/labeled_test_cases.json`; V1 uses `data/v1_labeled_test_cases.json` with inherited synthetic labels and expanded evidence. |
| Hidden actual result | Complete with limitation | Both datasets keep `actual_state` for post-decision evaluation; V1 labels are inherited synthetic labels, not independent historical labels. |
| Baseline and two policies | Complete for V0 and V1 | Baseline, Policy A, and Policy B are evaluated separately for both versions. |
| Metrics | Complete for V0 and exploratory V1 | Confusion matrices, precision, recall, false positives, false negatives, review rate, decision cost, and Brier scores are saved in the V0 and V1 metrics files. |
| Five wrong decisions | Complete for V0 and V1 | Analyses are saved in `results/failure-analysis.md` and `results/v1-failure-analysis.md`. |
| Reproducibility | Partially complete | Add exact V0/V1 run commands and file descriptions to `README.md`, then run both from a clean state. |
| Probability decision record | Complete for V0 and exploratory V1 | V1 evidence, provisional likelihoods, cost matrix, results, and limitations are recorded separately. |
| AI reviews | Missing | Complete three reviews and record accepted/rejected comments, changes, and evidence in `review-record.md`. |
| Preprint and publication | Missing | Create and compile the LaTeX paper, add references/figures, AI-use and contribution statements, and prepare the required LinkedIn and X materials. |

## Priority Order

### 1. Finalize the agent specification

Status: Partially complete

- Write the final one-sentence problem statement.
- Define the observable input fields and allowed values.
- Define the hidden states: Safe, Minor Defect, and Major Defect.
- Define the three actions and the human-review condition.
- Define what the agent remembers or learns after feedback.
- Add one human-reasoning function, such as identifying uncertainty or sending high-cost cases to a human.
- Resolve any remaining inconsistent thresholds and terminology across the V0 and V1 documentation.
- Create the V1 design flow image using the V0 design as the template.

Output: Updated `README.md` and consistent code/design terminology.

### 2. Create valid labeled test cases

Status: Complete

- Select 30 to 50 cases.
- Decide whether to use synthetic cases, real PRs with human labels, or a clearly documented mixture.
- Add a hidden `actual_state` label for every case: Safe, Minor Defect, or Major Defect.
- Document who assigned the labels, what evidence was used, and how uncertain labels were handled.
- Keep the labels separate from the agent decision function during prediction.
- Record the dataset version and date.

Output: A reproducible labeled dataset with evidence and hidden ground truth.

### 3. Implement the experiment

Status: Complete

- Create an evaluation script or notebook.
- Run the baseline, Policy A, and Policy B on exactly the same cases.
- Save each case's evidence, posterior probabilities, policy actions, actual hidden state, and decision cost.
- Make sure the agent does not read `actual_state` before making its decision.
- Add a fixed random seed if sampling or simulation is used.

Output: Per-case prediction results saved under `results/`.

### 4. Calculate evaluation metrics

Status: Complete

Calculate the applicable measurements for each of the three policies:

- Confusion matrix.
- Precision for detecting unsafe or major-defect cases.
- Recall for detecting unsafe or major-defect cases.
- False-positive quantity: safe cases blocked or unnecessarily escalated.
- False-negative quantity: unsafe cases merged.
- Human-review rate.
- Decision cost using the project cost matrix.
- Calibration of predicted probabilities, if enough labeled cases are available.

Output: A results table and a short interpretation in `README.md`.

### 5. Analyze five incorrect decisions

Status: Complete

- Select at least five incorrect or costly cases.
- Give each failure a clear name, for example `Passing CI missed security defect`.
- Explain the observed evidence, hidden state, selected action, and expected action.
- Calculate the cost of each error.
- Identify which error has the highest cost and explain why.
- State one design change that could reduce each failure.

Output: Failure analysis in `README.md` and/or `results/failure-analysis.md`.

### 6. Complete the probability decision record

Status: Complete

- Keep the prior probabilities summing to 100 percent.
- Add the full posterior probability for every hidden state, not only the major-defect probability.
- Add the source or justification for each prior and likelihood estimate.
- Add a second evidence event.
- Recalculate the posterior after the new evidence.
- Compare the new posterior with the threshold and record the new action.
- Add audit metadata: timestamp, dataset version, model version, and policy version.

Output: Completed `decisions/probability-decision-record.md`.

### 7. Complete real discussion evidence

Status: Complete

- Reddit and X evidence has been added and recorded.
- No additional discussion collection is planned.
- Any unanswered or awaiting-response item remains clearly marked as incomplete rather than being treated as evidence.

Output: Completed `discussion-record.md`.

### 8. Update the design using discussion findings

Status: Complete for the documented V1 scope

- Select the discussion findings that are relevant to the agent.
- Accept or reject each finding with a reason.
- Update the V1 agent, provisional probabilities, costs, and test cases where justified.
- Record the before-and-after design change.

Output: Evidence-linked design changes in `README.md` and `discussion-record.md`.

### 9. Complete AI review records

Status: Next

Complete three different reviews:

- Practitioner review.
- Probability and decision-cost review.
- Preprint review.

For each important comment, record the AI tool, comment, accept/reject decision, reason, resulting change, and evidence.

Output: Completed `review-record.md`.

### 10. Write and verify the preprint

Status: Later

- Create the IJCAI-style LaTeX paper.
- Include the problem, related work, discussions, agent design, probability model, test method, results, failure analysis, limitations, ethics, and conclusion.
- Include at least one result table or figure.
- Check every citation, equation, and reported result.
- Add the AI-use statement and contribution statement.
- Compile the PDF successfully.

Output: `paper/main.tex`, `paper/references.bib`, figures, and `paper/preprint.pdf`.

### 11. Prepare publication materials

Status: Later

- Write one LinkedIn post containing the required result, design change, limitation, and request for comments.
- Write the X thread containing the problem, test, result, and open question.
- Publish only after the evidence and PDF are verified.

Output: `social/linkedin-post.md` and `social/x-thread.md`.

### 12. Final quality check

Status: Later

- Confirm one problem was used throughout the project.
- Confirm no fabricated discussion, test, result, citation, or publication claim exists.
- Run the experiment from a clean state using the README instructions.
- Confirm all required files exist.
- Confirm every reported number matches the saved results.
- Complete the final project checklist and verify the documentation.

## Recommended Next Task

Create the V1 design flow image, then begin the three AI reviews. The first review should be a practitioner review of the agent workflow, V0/V1 separation, evidence contract, and failure analysis. Record each comment, decision, reason, resulting change, and evidence in `review-record.md`.
