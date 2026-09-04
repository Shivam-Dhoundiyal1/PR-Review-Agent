# Discussion Record

| Platform | Community or account | Link | My first contribution | Human answer | My next answer | Design change |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Reddit** | [r/AI_Agents](https://www.reddit.com/r/AI_Agents/) | [Post Link](https://www.reddit.com/r/AI_Agents/s/ceHxw9AX1P) | Post: Using Bayesian updating over LLM heuristics for deterministic agent actions. | Discussed using probabilistic layers over raw LLM outputs to handle decision calibration. | Clarified cost-sensitive decision gates and prior calibration. | Updated belief update module to use Bayesian updating $P(\text{Defect} \mid \text{CI}, \text{Diff}, \text{Author})$ instead of static LLM thresholding. |
| **Reddit** | [r/softwareengineer](https://www.reddit.com/r/softwareengineer/) | [Post Link](https://www.reddit.com/r/softwareengineer/s/RIVVBeFCEp) | Post: How do you deal with alert fatigue from automated PR review tools? | Feedback on noise levels, false positive thresholds, and path-based filtering. | Clarified balancing strict security gates against developer velocity. | Added path sensitivity weighting (e.g., `/auth`, `.github/`) as an explicit factor in human escalation rules. |
| **Reddit** | [r/devsecops](https://www.reddit.com/r/devsecops/) | [Post Link](https://www.reddit.com/r/devsecops/s/EKfgUgqCXc)  | Post: How do you balance path sensitivity vs. author trust when setting up automated PR review gates? | Discussions on path risk vs. author seniority/tenure in security gating. | Evaluated mandatory security sign-off conditions vs. trust scores. | Incorporated Author Trust Score ($T_{\text{author}}$) as an explicit prior input to the probability model. |
| **Reddit** | [r/learnpython](https://www.reddit.com/r/learnpython/) | [Post Link](https://www.reddit.com/r/learnpython/comments/1w61dub/best_way_to_handle_github_api_rate_limits_when/) | Post: Best way to handle GitHub API rate limits when scraping repo data in Python? | Recommended GraphQL query bundling, `ETag` conditional requests, and parsing `Retry-After` headers. | Acknowledged ETags saving API quota on unchanged data and PyGithub exponential backoff. | Refactored data collection pipeline to use `If-None-Match` conditional requests and GraphQL batching to optimize rate limits. |

---

## Assignment audit

This record contains four Reddit entries. The assignment requires at least five relevant communities, two contributions in each community, and five discussions with two or more replies. Complete the table with the second contribution, reply evidence, dates, and exact links. Do not mark a requirement complete unless the original post or comment and the human reply can be checked.

The design changes recorded above need supporting evidence from the original discussions. The record mentions Bayesian updating, path sensitivity, author trust, and API-rate-limit changes, but the current `src/main.py` does not implement ETag requests, GraphQL batching, or a separate author-trust prior beyond its likelihood table. Verify each claim against the code before treating it as a completed design change.

## Evidence still required

| Requirement | Current status | Required update |
| :--- | :--- | :--- |
| One specific problem statement | Partially complete | State the final problem as: “The agent observes PR evidence and selects merge, human review, or block because the true defect state is hidden.” |
| Agent design | Partially complete | Add the final input schema, hidden states, actions, human reasoning function, feedback, and conditions for asking a human. |
| Public discussions | Incomplete | Add one more verified community, the second contribution for every community, five discussions with two or more replies, and dates or screenshots/archives where needed. |
| Design updates from discussions | Unverified | For each accepted suggestion, link the exact human response and name the corresponding code, data, or policy change. Record rejected suggestions and reasons too. |
| Test cases | Partially complete | The repository has 15 synthetic cases and 35 fetched PR records. Confirm the labels and split; the fetched `actual_outcome` is merge/closed, not the hidden defect state needed to evaluate defect detection. |
| Hidden actual result | Missing | Add a defensible `actual_state` label such as Safe, Minor Defect, or Major Defect, using documented human labels or a reproducible proxy. Keep labels unavailable to the decision function until evaluation. |
| Baseline and two policies | Partially complete | The code defines a rule baseline, Bayesian Policy A, and cautious Policy B. Document what each policy tests and evaluate all three on the same labeled cases. |
| Metrics | Missing | Calculate confusion matrix, precision, recall, false-positive and false-negative quantities, human-review rate, decision cost, and calibration where labels support them. |
| Five wrong decisions | Missing | Select five misclassified cases, give each a failure-condition name, explain the cause, and calculate its cost. Identify the highest-cost error. |
| Reproducibility | Missing | Add a script or notebook that saves per-case evidence, hidden label, posterior, actions for all three policies, costs, and aggregate metrics. Add exact run instructions to `README.md`. |
| Probability decision record | Partially complete | Add the full posterior vector, audit metadata, source of estimates, and a second-evidence update with a new action. |
| AI reviews | Missing | Complete three reviews and record accepted/rejected comments, changes, and evidence in `review-record.md`. |
| Preprint and publication | Missing | Create and compile the LaTeX paper, add references/figures, AI-use and contribution statements, and prepare the required LinkedIn and X materials. |

## Current policy definitions

| Policy | Rule | Purpose |
| :--- | :--- | :--- |
| Baseline | Block failed CI; otherwise review high-sensitivity or large changes; merge the rest. | A simple operational rule for comparison. |
| Policy A | Use the Bayesian major-defect posterior: merge below 8%, human review from 8% through 45%, and block above 45%. | Test whether calibrated risk and asymmetric costs improve decisions. |
| Policy B | Use the same posterior: merge below 2%, human review from 2% through 20%, and block above 20%. | Test a more cautious policy that should reduce unsafe merges at the cost of more human work. |

These policies are not enough by themselves: the experiment must show their predictions against hidden labels. Actions without labeled comparison cannot produce precision, recall, false positives, false negatives, or decision cost.