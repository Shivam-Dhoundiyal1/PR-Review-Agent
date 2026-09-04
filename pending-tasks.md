# Pending Tasks: PR Review Agent

This file tracks the remaining work for the Week 1 project. Complete the tasks in order because later tasks depend on earlier decisions and evidence.

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
- Four Reddit discussion entries are recorded in `discussion-record.md`.

### Important limitation

The fetched dataset currently labels cases as `Merged` or `Closed_Without_Merge`. These are outcomes, not verified hidden defect states. The evaluation needs defensible labels such as `Safe`, `Minor Defect`, or `Major Defect`, or a clearly documented and justified proxy label.

## Priority Order

### 1. Finalize the agent specification

Status: Incomplete

- Write the final one-sentence problem statement.
- Define the observable input fields and allowed values.
- Define the hidden states: Safe, Minor Defect, and Major Defect.
- Define the three actions and the human-review condition.
- Define what the agent remembers or learns after feedback.
- Add one human-reasoning function, such as identifying uncertainty or sending high-cost cases to a human.
- Resolve inconsistent thresholds and terminology across `README.md`, `src/main.py`, and the probability decision record.

Deliverable: Updated `README.md` and consistent code/design terminology.

### 2. Create valid labeled test cases

Status: Complete

- Select 30 to 50 cases.
- Decide whether to use synthetic cases, real PRs with human labels, or a clearly documented mixture.
- Add a hidden `actual_state` label for every case: Safe, Minor Defect, or Major Defect.
- Document who assigned the labels, what evidence was used, and how uncertain labels were handled.
- Keep the labels separate from the agent decision function during prediction.
- Record the dataset version and date.

Deliverable: A reproducible labeled dataset with evidence and hidden ground truth.

### 3. Implement the experiment

Status: Complete

- Create an evaluation script or notebook.
- Run the baseline, Policy A, and Policy B on exactly the same cases.
- Save each case's evidence, posterior probabilities, policy actions, actual hidden state, and decision cost.
- Make sure the agent does not read `actual_state` before making its decision.
- Add a fixed random seed if sampling or simulation is used.

Deliverable: Per-case prediction results saved under `results/`.

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

Deliverable: A results table and a short interpretation in `README.md`.

### 5. Analyze five incorrect decisions

Status: Complete

- Select at least five incorrect or costly cases.
- Give each failure a clear name, for example `Passing CI missed security defect`.
- Explain the observed evidence, hidden state, selected action, and expected action.
- Calculate the cost of each error.
- Identify which error has the highest cost and explain why.
- State one design change that could reduce each failure.

Deliverable: Failure analysis in `README.md` and/or `results/failure-analysis.md`.

### 6. Complete the probability decision record

Status: Complete

- Keep the prior probabilities summing to 100 percent.
- Add the full posterior probability for every hidden state, not only the major-defect probability.
- Add the source or justification for each prior and likelihood estimate.
- Add a second evidence event.
- Recalculate the posterior after the new evidence.
- Compare the new posterior with the threshold and record the new action.
- Add audit metadata: timestamp, dataset version, model version, and policy version.

Deliverable: Completed `decisions/probability-decision-record.md`.

### 7. Complete real discussion evidence

Status: Next

- Verify the four existing Reddit entries.
- Add at least one more relevant community.
- Make two contributions in each selected community.
- Complete at least five discussions with two or more human replies.
- Add exact links, dates, human answers, and your follow-up answer.
- Record whether each discussion caused a new assumption, failure condition, test, design change, or no change.
- Do not invent human replies or claim a change that is not reflected in the code or design.

Deliverable: Completed `discussion-record.md`.

### 8. Update the design using discussion findings

Status: Partially complete

- Select the discussion findings that are relevant to the agent.
- Accept or reject each finding with a reason.
- Update the agent, probabilities, costs, test cases, or policy where justified.
- Record the before-and-after design change.

Deliverable: Evidence-linked design changes in `README.md` and `discussion-record.md`.

### 9. Complete AI review records

Status: Missing

Complete three different reviews:

- Practitioner review.
- Probability and decision-cost review.
- Preprint review.

For each important comment, record the AI tool, comment, accept/reject decision, reason, resulting change, and evidence.

Deliverable: Completed `review-record.md`.

### 10. Write and verify the preprint

Status: Missing

- Create the IJCAI-style LaTeX paper.
- Include the problem, related work, discussions, agent design, probability model, test method, results, failure analysis, limitations, ethics, and conclusion.
- Include at least one result table or figure.
- Check every citation, equation, and reported result.
- Add the AI-use statement and contribution statement.
- Compile the PDF successfully.

Deliverable: `paper/main.tex`, `paper/references.bib`, figures, and `paper/preprint.pdf`.

### 11. Prepare publication materials

Status: Missing

- Write one LinkedIn post containing the required result, design change, limitation, and request for comments.
- Write the X thread containing the problem, test, result, and open question.
- Publish only after the evidence and PDF are verified.

Deliverable: `social/linkedin-post.md` and `social/x-thread.md`.

### 12. Final quality check

Status: Not started

- Confirm one problem was used throughout the project.
- Confirm no fabricated discussion, test, result, citation, or publication claim exists.
- Run the experiment from a clean state using the README instructions.
- Confirm all required files exist.
- Confirm every reported number matches the saved results.
- Complete the assignment checklist in the course instructions.

## Recommended Next Task

Start with Task 1: finalize the agent specification. Then create the labeled dataset in Task 2 before writing the evaluation metrics. Without hidden labels, the policy comparison and error-cost analysis cannot be valid.
