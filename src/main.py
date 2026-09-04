import json
import os

# --- 1. DEFINITIONS & LIKELIHOOD TABLES ---
PRIORS = {
    "S1_Safe": 0.80,
    "S2_Minor": 0.15,
    "S3_Major": 0.05
}

LIKELIHOODS = {
    "CI": {
        "Pass": {"S1": 0.95, "S2": 0.85, "S3": 0.30},
        "Fail": {"S1": 0.05, "S2": 0.15, "S3": 0.70}
    },
    "Scope": {
        "Small":  {"S1": 0.60, "S2": 0.30, "S3": 0.10},
        "Medium": {"S1": 0.30, "S2": 0.50, "S3": 0.40},
        "Large":  {"S1": 0.10, "S2": 0.20, "S3": 0.50}
    },
    "Sensitivity": {
        "Low":  {"S1": 0.75, "S2": 0.60, "S3": 0.15},
        "High": {"S1": 0.25, "S2": 0.40, "S3": 0.85}
    },
    "Author": {
        "High": {"S1": 0.80, "S2": 0.50, "S3": 0.20},
        "Low":  {"S1": 0.20, "S2": 0.50, "S3": 0.80}
    }
}

VALID_EVIDENCE = {
    "CI": {"Pass", "Fail"},
    "Scope": {"Small", "Medium", "Large"},
    "Sensitivity": {"Low", "High"},
    "Author": {"High", "Low"},
}

def validate_evidence(evidence):
    """Reject evidence values outside the project specification."""
    for field, allowed_values in VALID_EVIDENCE.items():
        if evidence.get(field) not in allowed_values:
            raise ValueError(f"Invalid {field} evidence: {evidence.get(field)}")

def record_human_feedback(feedback_log, case_id, selected_action, observed_state):
    """Store post-decision human or test feedback for later policy review."""
    feedback_log.append({
        "case_id": case_id,
        "selected_action": selected_action,
        "observed_state": observed_state,
    })

# --- 2. BAYESIAN ENGINE ---
def compute_posterior(evidence):
    """Calculates posterior probability P(S3 | E) using Bayes' Theorem."""
    validate_evidence(evidence)
    e_ci = evidence["CI"]
    e_scope = evidence["Scope"]
    e_sens = evidence["Sensitivity"]
    e_auth = evidence["Author"]

    # Calculate joint likelihood P(E | Si)
    p_e_s1 = LIKELIHOODS["CI"][e_ci]["S1"] * LIKELIHOODS["Scope"][e_scope]["S1"] * LIKELIHOODS["Sensitivity"][e_sens]["S1"] * LIKELIHOODS["Author"][e_auth]["S1"]
    p_e_s2 = LIKELIHOODS["CI"][e_ci]["S2"] * LIKELIHOODS["Scope"][e_scope]["S2"] * LIKELIHOODS["Sensitivity"][e_sens]["S2"] * LIKELIHOODS["Author"][e_auth]["S2"]
    p_e_s3 = LIKELIHOODS["CI"][e_ci]["S3"] * LIKELIHOODS["Scope"][e_scope]["S3"] * LIKELIHOODS["Sensitivity"][e_sens]["S3"] * LIKELIHOODS["Author"][e_auth]["S3"]

    # Multiply by priors P(Si)
    numerator_s1 = p_e_s1 * PRIORS["S1_Safe"]
    numerator_s2 = p_e_s2 * PRIORS["S2_Minor"]
    numerator_s3 = p_e_s3 * PRIORS["S3_Major"]

    # Normalizer P(E)
    p_e = numerator_s1 + numerator_s2 + numerator_s3

    # Posterior probabilities
    p_s3_given_e = numerator_s3 / p_e
    return round(p_s3_given_e * 100, 2)  # Return as percentage

# --- 3. POLICIES ---
def evaluate_baseline(evidence):
    """Rule-based baseline."""
    validate_evidence(evidence)
    if evidence["CI"] == "Fail":
        return "Decline / Block"
    elif evidence["Sensitivity"] == "High" or evidence["Scope"] == "Large":
        return "Request Human Review"
    else:
        return "Merge"

def evaluate_policy_a(p_s3):
    """Calibrated Bayesian Policy A (Our Agent)."""
    if p_s3 < 8.0:
        return "Merge"
    elif 8.0 <= p_s3 <= 45.0:
        return "Request Human Review"
    else:
        return "Decline / Block"

def evaluate_policy_b(p_s3):
    """Aggressive Cautious Policy B."""
    if p_s3 < 2.0:
        return "Merge"
    elif 2.0 <= p_s3 <= 20.0:
        return "Request Human Review"
    else:
        return "Decline / Block"

# --- 4. EXECUTION SAMPLE ---
if __name__ == "__main__":
    sample_evidence = {
        "CI": "Pass",
        "Scope": "Small",
        "Sensitivity": "High",
        "Author": "Low"
    }

    p_s3 = compute_posterior(sample_evidence)
    print(f"Posterior Risk P(S3 | E): {p_s3}%")
    print(f"Baseline Action: {evaluate_baseline(sample_evidence)}")
    print(f"Policy A (Calibrated Agent) Action: {evaluate_policy_a(p_s3)}")
    print(f"Policy B (Aggressive Agent) Action: {evaluate_policy_b(p_s3)}")