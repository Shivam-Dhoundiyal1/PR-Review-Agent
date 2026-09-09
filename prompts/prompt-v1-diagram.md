# Prompt: Create Agent V1 system design diagram

You are an expert system architect and technical writer.

Use the project context from these files:
- README.md
- discussion-record.md
- decisions/probability-decision-record.md
- src/main.py
- src/evaluate.py
- src/v1_main.py
- src/build_v1_dataset.py
- src/evaluate_v1.py
- src/metrics_v1.py
- data/v1_labeled_test_cases.json
- results/v1_metrics.json
- results/v1-failure-analysis.md
- review-record.md
- pending-tasks.md

Create a clear system design diagram for Agent V1.

Requirements:
1. Show how V1 extends V0.
2. Show the new dataset construction flow and expanded evidence.
3. Show the Bayesian decision pipeline for V1.
4. Show the difference between:
   - V0 baseline
   - V1 expanded evidence
   - V1 policy comparison
5. Include the hidden-state model:
   - Safe
   - Minor Defect
   - Major Defect
6. Show the evaluation and cost logic clearly.
7. Clearly note that V1 is exploratory and uses synthetic/provisional assumptions.
8. Use Mermaid diagram syntax only.
9. Return a single Mermaid code block.

Output format:
```mermaid
...
```
