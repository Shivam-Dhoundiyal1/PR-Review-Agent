# Prompt: Create Agent V0 system design diagram

You are an expert system architect and technical writer.

Use the project context from these files:
- README.md
- decisions/probability-decision-record.md
- src/main.py
- src/evaluate.py
- data/labeled_test_cases.json
- results/metrics.json
- results/failure-analysis.md
- pending-tasks.md

Create a clear system design diagram for Agent V0.

Requirements:
1. Show the full end-to-end flow:
   - Inputs
   - Evidence preprocessing
   - Hidden-state modeling
   - Bayesian posterior computation
   - Policy decision layer (Baseline, Policy A, Policy B)
   - Action outputs
   - Evaluation and metrics
2. Label the hidden states clearly:
   - Safe
   - Minor Defect
   - Major Defect
3. Show how V0 uses synthetic labeled data and why it is a benchmark, not a production system.
4. Show the evaluation loop: predicted action -> actual hidden state -> metrics -> failure analysis.
5. Use Mermaid diagram syntax only.
6. Return the diagram in a single Mermaid code block.
7. Keep it neat, readable, and professional.

Output format:
```mermaid
...
```
