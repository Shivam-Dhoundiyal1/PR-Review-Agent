# Synthetic Test Cases: PR Review Agent

This dataset contains 15 representative test scenarios combining different evidence signals ($E$) to evaluate the Bayesian PR Review Agent's probability updates and action selections.

## Evidence Notation Legend
* **CI ($E_1$):** `Pass` / `Fail`
* **Scope ($E_2$):** `Small` ($<50$ LOC), `Medium` ($50-300$ LOC), `Large` ($>300$ LOC)
* **Sensitivity ($E_3$):** `Low` (UI / Docs / Styles), `High` (Auth / DB / Payment APIs / Core Infra)
* **Author ($E_4$):** `High` ($>50$ merged PRs), `Low` ($<50$ merged PRs)

## Action Threshold Policy
* **`Merge` ($A_1$):** $P(S_3 \mid E) < 8.0\%$
* **`Request Human Review` ($A_2$):** $8.0\% \le P(S_3 \mid E) \le 45.0\%$
* **`Decline / Block` ($A_3$):** $P(S_3 \mid E) > 45.0\%$

---

## Benchmark Test Cases Matrix

| Case ID | Scenario Description | CI ($E_1$) | Scope ($E_2$) | Sensitivity ($E_3$) | Author ($E_4$) | $P(S_1 \mid E)$ (Safe) | $P(S_2 \mid E)$ (Minor) | $P(S_3 \mid E)$ (Major) | Selected Action | Expected Rationale |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **TC-01** | Standard UI Bug Fix | Pass | Small | Low | High | 97.4% | 2.5% | **0.1%** | **Merge** | Routine, low-risk change by trusted author. |
| **TC-02** | New Contributor Payment Edit | Pass | Small | High | Low | 72.5% | 24.3% | **3.2%** | **Merge** | CI pass & small diff keep risk under 8% threshold. |
| **TC-03** | Core Auth Refactor by Senior | Pass | Large | High | High | 68.2% | 18.1% | **13.7%** | **Request Human Review** | Large diff in high-sensitivity path triggers review. |
| **TC-04** | Failed CI on UI Style Tweaks | Fail | Small | Low | High | 38.2% | 15.3% | **46.5%** | **Decline / Block** | Failing CI drives major bug risk above 45%. |
| **TC-05** | Massive Database Migration | Pass | Large | High | Low | 31.4% | 16.7% | **51.9%** | **Decline / Block** | New author + huge diff + DB sensitivity = high risk. |
| **TC-06** | Medium Doc Update by Junior | Pass | Medium | Low | Low | 81.2% | 17.5% | **1.3%** | **Merge** | Low sensitivity documentation keeps PR safe. |
| **TC-07** | Medium Payment API Fix | Pass | Medium | High | High | 77.8% | 17.1% | **5.1%** | **Merge** | High author trust counterbalances API risk. |
| **TC-08** | Failed CI on Small Auth Patch | Fail | Small | High | High | 21.0% | 11.2% | **67.8%** | **Decline / Block** | CI failure in critical path forces immediate block. |
| **TC-09** | Large Feature Addition (UI) | Pass | Large | Low | High | 88.5% | 9.8% | **1.7%** | **Merge** | Low sensitivity UI changes safe even if large. |
| **TC-10** | Medium DB Migration by Senior | Pass | Medium | High | High | 73.1% | 21.5% | **5.4%** | **Merge** | Moderate risk handled safely by trusted dev. |
| **TC-11** | Flaky CI Pass on Large Auth PR | Pass | Large | High | Low | 28.5% | 15.2% | **56.3%** | **Decline / Block** | High uncertainty across all risk factors. |
| **TC-12** | Small Fix on Core Billing Config | Pass | Small | High | High | 89.1% | 9.4% | **1.5%** | **Merge** | Minimal blast radius with passing CI. |
| **TC-13** | Failed CI on Large UI Refactor | Fail | Large | Low | Low | 18.6% | 14.8% | **66.6%** | **Decline / Block** | Large scope + failed CI requires rejection. |
| **TC-14** | Medium Auth Change by New Dev | Pass | Medium | High | Low | 49.3% | 26.3% | **24.4%** | **Request Human Review** | Unproven author touching auth needs escalation. |
| **TC-15** | Medium Non-Critical Refactor | Fail | Medium | Low | High | 42.1% | 22.2% | **35.7%** | **Request Human Review** | Failed CI on non-critical code needs review. |