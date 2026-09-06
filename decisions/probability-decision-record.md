# Probability Decision Record: PR Review Agent

## 1. System Setup

### Final Problem Statement

The agent observes pull-request evidence and selects **Merge**, **Request Human Review**, or **Decline / Block** because the true defect state is hidden until further testing or human review.

### Agent Contract

The agent observes CI status, diff scope, file sensitivity, and author history. It estimates beliefs over Safe, Minor Defect, and Major Defect, then selects one of the three actions. It requests human review when the posterior is uncertain or the cost of an incorrect merge is high. Human review or later testing supplies feedback that is recorded for future analysis of the model and policy. The hidden state is not supplied to the agent before its initial action.

### Design Versions

**Agent V0** is the evaluated design documented in this record: CI status, diff scope, file sensitivity, and author history feed the Bayesian model, while Baseline, Policy A, and Policy B select the action. The current benchmark results use V0.

**Agent V1** records accepted qualitative feedback from the Reddit discussions without changing the V0 benchmark policies:

- Author history should be conditioned on domain familiarity; general experience may not transfer to infrastructure or other high-risk work.
- CI should eventually include reliability or flaky-test history rather than treating every result as equally informative.
- Review latency, revert rate, and filtered review-comment signals are candidate features for future labeled experiments.
- An LLM may extract or explain evidence, but it must not rewrite the Bayesian posterior or final action.
- GitHub collection should use caching, ETag requests, `Retry-After` handling, and exponential backoff to reduce API-rate-limit risk. These safeguards concern data collection and are not probability evidence.

The V1 candidates are not assigned new likelihoods or priors yet because the discussion provides qualitative suggestions, not an independently labeled dataset. Baseline, Policy A, and Policy B remain unchanged for comparability.

### Hidden States ($S$)
We define three mutually exclusive hidden states representing the true quality of a Pull Request in production:
* **$S_1$ (Safe):** Code functions correctly, introduces no regressions, and meets security standards.
* **$S_2$ (Minor Defect):** Code contains non-breaking issues (e.g., style violations, minor tech debt, non-critical logging bug).
* **$S_3$ (Major Defect):** Code introduces a critical bug, security vulnerability, data corruption, or production outage.

$$\sum_{i=1}^{3} P(S_i) = 1.0$$

### Prior Probabilities $P(S)$
These are initial modeling assumptions for the simulated benchmark, not verified production statistics. They must be recalibrated when independently labeled historical cases become available:
* $P(S_1) = 0.80$ (80% of submitted PRs passing initial checks are safe)
* $P(S_2) = 0.15$ (15% contain minor defects)
* $P(S_3) = 0.05$ (5% contain major breaking defects)

---

## 2. Evidence Signals & Likelihood Tables

The agent observes four key evidence variables:
1. **$E_1$ (CI Build Status):** `Pass` or `Fail`
2. **$E_2$ (Diff Scope):** `Small` ($<50$ lines), `Medium` ($50-300$ lines), `Large` ($>300$ lines)
3. **$E_3$ (File Sensitivity):** `Low Risk` (UI/Docs) vs `High Risk` (Auth/DB/Payment APIs)
4. **$E_4$ (Author History):** `High Trust` ($>50$ merged PRs) vs `Low Trust` ($<50$ merged PRs)

### Likelihood Table $P(E \mid S)$

| Evidence Variable | Evidence State ($E$) | $P(E \mid S_1)$ (Safe) | $P(E \mid S_2)$ (Minor) | $P(E \mid S_3)$ (Major) |
| :--- | :--- | :---: | :---: | :---: |
| **$E_1$ (CI Status)** | `Pass` | 0.95 | 0.85 | 0.30 |
| | `Fail` | 0.05 | 0.15 | 0.70 |
| **$E_2$ (Diff Scope)** | `Small` ($<50$ loc) | 0.60 | 0.30 | 0.10 |
| | `Medium` ($50-300$ loc) | 0.30 | 0.50 | 0.40 |
| | `Large` ($>300$ loc) | 0.10 | 0.20 | 0.50 |
| **$E_3$ (File Sensitivity)** | `Low Risk` (UI/Docs) | 0.75 | 0.60 | 0.15 |
| | `High Risk` (Auth/DB) | 0.25 | 0.40 | 0.85 |
| **$E_4$ (Author History)** | `High Trust` ($>50$ PRs) | 0.80 | 0.50 | 0.20 |
| | `Low Trust` ($<50$ PRs) | 0.20 | 0.50 | 0.80 |

### Estimate Justification

The priors and likelihoods are controlled assumptions for this project benchmark. Their purpose is to create an explicit belief model that can be tested and revised. They were selected so that passing CI generally supports safety, failed CI supports defect risk, large diffs increase uncertainty, sensitive paths increase major-defect risk, and author history provides a weak trust signal. They are not claims about the actual defect rates of a repository.

---

## 3. Bayesian Updating Formula

When vector of evidence $E = \{E_1, E_2, E_3, E_4\}$ is observed, assuming conditional independence among evidence items given state $S_i$:

$$P(E \mid S_i) = \prod_{k=1}^{4} P(E_k \mid S_i)$$

The posterior probability for state $S_i$ is computed using Bayes' Theorem:

$$P(S_i \mid E) = \frac{P(E \mid S_i) \cdot P(S_i)}{\sum_{j=1}^{3} P(E \mid S_j) \cdot P(S_j)}$$

---

## 4. Error Cost Matrix & Action Thresholds

### Cost Matrix $C(\text{Action}, \text{State})$
Units represent relative developer hours & incident costs lost:

| Action ($A$) | $S_1$ (Safe) | $S_2$ (Minor Defect) | $S_3$ (Major Defect) |
| :--- | :---: | :---: | :---: |
| **$A_1$: Merge** | **0** | **2** | **100** (Production Outage) |
| **$A_2$: Request Human Review** | **1** (15 min dev time) | **1** | **5** (Caught in review) |
| **$A_3$: Decline / Block** | **5** (Dev frustration) | **2** | **0** (Prevented outage) |

### Decision Policy Thresholds
Because merging a $S_3$ (Major Defect) has an asymmetric cost ($100$), the policy is strictly calibrated around $P(S_3 \mid E)$, the posterior risk of a major defect:

| Policy | Rule | Purpose |
| :--- | :--- | :--- |
| Baseline | Block failed CI; otherwise review high-sensitivity or large changes; merge the rest. | A simple operational rule for comparison. |
| Policy A | Use the Bayesian major-defect posterior: merge below 8%, human review from 8% through 45%, and block above 45%. | Test whether calibrated risk and asymmetric costs improve decisions. |
| Policy B | Use the same posterior: merge below 2%, human review from 2% through 20%, and block above 20%. | Test a more cautious policy that should reduce unsafe merges at the cost of more human work. |

These policies must be evaluated against hidden labels. Actions without labeled comparison cannot produce precision, recall, false positives, false negatives, or decision cost.

$$\text{Action}(E) = \begin{cases}
\text{Merge } (A_1) & \text{if } P(S_3 \mid E) < 0.08 \\
\text{Request Human Review } (A_2) & \text{if } 0.08 \le P(S_3 \mid E) \le 0.45 \\
\text{Decline / Block } (A_3) & \text{if } P(S_3 \mid E) > 0.45
\end{cases}$$

---

## 5. Worked Example Step-by-Step

### Scenario
A new contributor submits a PR modifying the payment gateway config. CI passes.
* **Evidence Observed:** $E = \{\text{CI}=\text{Pass}, \text{Scope}=\text{Small}, \text{Sensitivity}=\text{High Risk}, \text{Author}=\text{Low Trust}\}$

### Step 1: Calculate Likelihoods for Each State
* **For $S_1$ (Safe):**  
  $$P(E \mid S_1) = 0.95 \times 0.60 \times 0.25 \times 0.20 = 0.0285$$
* **For $S_2$ (Minor Defect):**  
  $$P(E \mid S_2) = 0.85 \times 0.30 \times 0.40 \times 0.50 = 0.0510$$
* **For $S_3$ (Major Defect):**  
  $$P(E \mid S_3) = 0.30 \times 0.10 \times 0.85 \times 0.80 = 0.0204$$

### Step 2: Multiply by Prior Probabilities
* $P(E \mid S_1) \cdot P(S_1) = 0.0285 \times 0.80 = 0.0228$
* $P(E \mid S_2) \cdot P(S_2) = 0.0510 \times 0.15 = 0.00765$
* $P(E \mid S_3) \cdot P(S_3) = 0.0204 \times 0.05 = 0.00102$

**Total Evidence Likelihood $P(E)$:**  
$$0.0228 + 0.00765 + 0.00102 = 0.03147$$

### Step 3: Compute Posterior Probabilities
* **$P(S_1 \mid E)$ (Safe):** $0.0228 / 0.03147 = 72.45\%$
* **$P(S_2 \mid E)$ (Minor Defect):** $0.00765 / 0.03147 = 24.31\%$
* **$P(S_3 \mid E)$ (Major Defect):** $0.00102 / 0.03147 = 3.24\%$

### Step 4: Decision Execution
* Posterior risk $P(S_3 \mid E) = 3.24\%$.
* Since $3.24\% < 8\%$, the policy selects **Action $A_1$: Merge**.
* *Note:* Even though the PR touched a high-risk file with a new author, the small scope and passing CI keep the posterior risk below the $8\%$ escalation threshold.

---

## 6. Second-Evidence Update

### New Evidence

After the initial decision, the CI pipeline is rerun and fails. The other evidence remains unchanged:

$$E' = \{\text{CI}=\text{Fail},\ \text{Scope}=\text{Small},\ \text{Sensitivity}=\text{High Risk},\ \text{Author}=\text{Low Trust}\}$$

### Updated Unnormalized Beliefs

Using the same priors and likelihood table:

* $S_1$: $0.05 \times 0.60 \times 0.25 \times 0.20 \times 0.80 = 0.00120$
* $S_2$: $0.15 \times 0.30 \times 0.40 \times 0.50 \times 0.15 = 0.00135$
* $S_3$: $0.70 \times 0.10 \times 0.85 \times 0.80 \times 0.05 = 0.00238$

The normalizer is $0.00120 + 0.00135 + 0.00238 = 0.00493$.

### Updated Posterior

| Hidden state | Posterior probability |
| :--- | ---: |
| Safe ($S_1$) | 24.34% |
| Minor Defect ($S_2$) | 27.38% |
| Major Defect ($S_3$) | 48.28% |
| **Total** | **100.00%** |

The major-defect probability increases from 3.24% to 48.28%. Since 48.28% is above the Policy A block threshold of 45%, the updated action is **Decline / Block**. This demonstrates how new evidence can change both the belief and the action.

## 7. Audit Metadata

| Item | Value |
| :--- | :--- |
| Decision-record date | 2026-09-04 |
| Dataset version | `synthetic-pr-review-v1` |
| Model version | `bayesian-pr-agent-v1` |
| Policy version | `policy-a-v1` |
| Evidence used before initial action | CI, scope, sensitivity, author history |
| Hidden state available before initial action | No |
| Feedback event | CI failure observed after the initial decision |

---

## 8. V1 Expanded Evidence and Evaluation

V1 is a separate exploratory model. It keeps the V0 Baseline, Policy A, and Policy B thresholds unchanged while adding these evidence fields to the separate dataset `data/v1_labeled_test_cases.json`:

| Evidence field | Allowed values | Purpose |
| :--- | :--- | :--- |
| `CIReliability` | `Stable`, `Flaky` | Distinguishes reliable CI from a noisy test history. |
| `AuthorDomain` | `Match`, `Mismatch` | Prevents general author experience from automatically transferring across technical domains. |
| `ReviewLatency` | `Short`, `Long` | Represents how long prior changes typically remain under review. |
| `RevertRate` | `Low`, `High` | Represents the author's or change area's prior reversion pattern. |
| `ReviewComments` | `Clean`, `Actionable`, `Noisy` | Uses filtered review history rather than raw bot or resolved comment counts. |

The original V0 fields remain in the V1 evidence: `CI`, `Scope`, `Sensitivity`, and `Author`. V1 uses provisional likelihoods in `src/v1_main.py`; these are modeling assumptions, not recalibrated production probabilities. The V1 hidden labels are inherited from the synthetic V0 scenarios, so V1 is an exploratory comparison rather than independent validation.

### V1 Cost Matrix

| Action | Safe | Minor Defect | Major Defect |
| :--- | ---: | ---: | ---: |
| Merge | 0 | 3 | 120 |
| Request Human Review | 2 | 2 | 8 |
| Decline / Block | 6 | 3 | 0 |

The V1 matrix assigns a higher relative cost to merging a major defect and reflects the added cost assumptions for review and blocking. V0 and V1 total costs are not directly comparable because their matrices differ.

### V1 Results

| Policy | Precision | Recall | False positives | False negatives | Human-review rate | Decision cost |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline | 77.27% | 85.00% | 5 | 3 | 53.33% | 92 |
| Policy A | 100.00% | 40.00% | 0 | 12 | 16.67% | 421 |
| Policy B | 100.00% | 50.00% | 0 | 10 | 10.00% | 276 |

The full multiclass confusion matrices, binary confusion matrices, per-case posterior vectors, and major-defect Brier scores are saved in `results/v1_metrics.json` and `results/v1_policy_results.json`.