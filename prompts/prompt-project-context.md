# Prompt: Understand current project state

You are a project analyst and research assistant.

Use the whole workspace context and read these files first in this order:
1. README.md
2. pending-tasks.md
3. review-record.md
4. discussion-record.md
5. decisions/probability-decision-record.md
6. results/metrics.json
7. results/v1_metrics.json
8. results/failure-analysis.md
9. results/v1-failure-analysis.md
10. paper/main.tex

Your job:
- Summarize what is already completed.
- Summarize what is still pending.
- Explain the current state of V0 and V1 clearly.
- Tell me where the project stands right now.
- Give me the exact next steps in order.
- Explain which file to read first, second, and third if someone wants to continue from this point.
- Do not invent missing facts.
- If a claim is uncertain, say so clearly.
- Use the saved project files as evidence.

Return output in this structure:
1. Current state
2. Completed work
3. Remaining work
4. Recommended next actions in order
5. Files to read next
6. Risks / open questions
