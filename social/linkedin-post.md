# LinkedIn Post — PR Review Agent Preprint


---

A pull request could look safe at review time and still hide some potential breaking bugs, because the defect is hidden until testing or human review.

This is the problem I worked on.

I built and evaluated a Bayesian PR review agent that observes four signals in V0:
-CI status
-Diff size
-File sensitivity
-Author history

It also maintains probabilities over hidden states:
Safe / Minor Defect / Major Defect
and selects one of three actions:
Merge / Request Human Review / Decline or Block

A PR review is not a single yes/no decision. The system needs to observe the evidence — diff size, author history, file sensitivity, CI status — and reason about the hidden state before making a decision based on calculated risk.

The agent design separates these steps. It gathers the evidence, calculates the belief/likelihood over the hidden states, evaluates the cost of each possible action, and then decides between merge, human review, or decline/block.

I chose a probability model instead of an LLM heuristic because the decision needs to be auditable, especially when answering why this PR blocked?
The agent can look at the evidence, but if the LLM also updates the posterior or decides the final action, we lose the ability to clearly trace why the PR was actually blocked.The probability model keeps that decision trace intact.

I then compared my agent against three policies: a rule-based baseline, Policy 1 and Policy 2
On 30 synthetic cases, the policy 2 reduced false positives to 1 and the human-review rate to 33%, compared to 5 false positives and a 53% review rate for the baseline.

However, the same policy also missed 6 unsafe PRs that the baseline caught.
The failure that stood out to me was Policy 1: it automatically merged 4 Major Defects because passing CI and a trusted author pushed the posterior below the 8% merge threshold, even when the PR touched a sensitive or high-risk file.

A public discussion on Reddit also led to a design change. Treating all author experience as the same is not correct. A senior engineer with 100 PRs may have a lot of experience in frontend, but that doesn't necessarily make them equally trustworthy for an infrastructure or payment change. That led to a new design V1 agent where author history is considered along with the technical domain of the change and other things aswell.

The biggest limitation right now is the data.
All the test cases are synthetic, because a merged PR does not guarantee that it is safe, and a closed PR without a merge does not necessarily mean it contained a major defect.
So the results should be viewed as a comparison of decision trade-offs under simulation, rather than real-world performance.
If you are working with CI systems, code review pipelines, or release automation:
What signals would you actually trust for an automated merge decision?

---
