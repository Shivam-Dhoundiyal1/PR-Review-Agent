"""V1 PR review model with Reddit-informed evidence signals.

V1 is intentionally separate from the evaluated V0 model. It keeps the same
policy thresholds while adding evidence that can be tested independently.
"""

PRIORS = {
    "Safe": 0.80,
    "Minor Defect": 0.15,
    "Major Defect": 0.05,
}

LIKELIHOODS = {
    "CI": {
        "Pass": {"Safe": 0.95, "Minor Defect": 0.85, "Major Defect": 0.30},
        "Fail": {"Safe": 0.05, "Minor Defect": 0.15, "Major Defect": 0.70},
    },
    "CIReliability": {
        "Stable": {"Safe": 0.85, "Minor Defect": 0.75, "Major Defect": 0.45},
        "Flaky": {"Safe": 0.15, "Minor Defect": 0.25, "Major Defect": 0.55},
    },
    "Scope": {
        "Small": {"Safe": 0.60, "Minor Defect": 0.30, "Major Defect": 0.10},
        "Medium": {"Safe": 0.30, "Minor Defect": 0.50, "Major Defect": 0.40},
        "Large": {"Safe": 0.10, "Minor Defect": 0.20, "Major Defect": 0.50},
    },
    "Sensitivity": {
        "Low": {"Safe": 0.75, "Minor Defect": 0.60, "Major Defect": 0.15},
        "High": {"Safe": 0.25, "Minor Defect": 0.40, "Major Defect": 0.85},
    },
    "Author": {
        "High": {"Safe": 0.80, "Minor Defect": 0.50, "Major Defect": 0.20},
        "Low": {"Safe": 0.20, "Minor Defect": 0.50, "Major Defect": 0.80},
    },
    "AuthorDomain": {
        "Match": {"Safe": 0.80, "Minor Defect": 0.55, "Major Defect": 0.25},
        "Mismatch": {"Safe": 0.20, "Minor Defect": 0.45, "Major Defect": 0.75},
    },
    "ReviewLatency": {
        "Short": {"Safe": 0.70, "Minor Defect": 0.45, "Major Defect": 0.30},
        "Long": {"Safe": 0.30, "Minor Defect": 0.55, "Major Defect": 0.70},
    },
    "RevertRate": {
        "Low": {"Safe": 0.80, "Minor Defect": 0.55, "Major Defect": 0.30},
        "High": {"Safe": 0.20, "Minor Defect": 0.45, "Major Defect": 0.70},
    },
    "ReviewComments": {
        "Clean": {"Safe": 0.75, "Minor Defect": 0.45, "Major Defect": 0.25},
        "Actionable": {"Safe": 0.20, "Minor Defect": 0.40, "Major Defect": 0.45},
        "Noisy": {"Safe": 0.05, "Minor Defect": 0.15, "Major Defect": 0.30},
    },
}

VALID_EVIDENCE = {
    field: set(values) for field, values in {
        "CI": ("Pass", "Fail"),
        "CIReliability": ("Stable", "Flaky"),
        "Scope": ("Small", "Medium", "Large"),
        "Sensitivity": ("Low", "High"),
        "Author": ("High", "Low"),
        "AuthorDomain": ("Match", "Mismatch"),
        "ReviewLatency": ("Short", "Long"),
        "RevertRate": ("Low", "High"),
        "ReviewComments": ("Clean", "Actionable", "Noisy"),
    }.items()
}

ACTIONS = ("Merge", "Request Human Review", "Decline / Block")


def validate_evidence(evidence):
    for field, allowed_values in VALID_EVIDENCE.items():
        if evidence.get(field) not in allowed_values:
            raise ValueError(f"Invalid {field} evidence: {evidence.get(field)}")


def compute_posterior_distribution(evidence):
    """Return the full V1 posterior using evidence only."""
    validate_evidence(evidence)
    unnormalized = {}
    for state, prior in PRIORS.items():
        likelihood = prior
        for field, value in evidence.items():
            likelihood *= LIKELIHOODS[field][value][state]
        unnormalized[state] = likelihood

    normalizer = sum(unnormalized.values())
    return {
        state: round(value / normalizer * 100, 2)
        for state, value in unnormalized.items()
    }


def compute_posterior(evidence):
    return compute_posterior_distribution(evidence)["Major Defect"]


def evaluate_baseline(evidence):
    """Keep the V0 rule baseline unchanged for comparison."""
    validate_evidence(evidence)
    if evidence["CI"] == "Fail":
        return "Decline / Block"
    if evidence["Sensitivity"] == "High" or evidence["Scope"] == "Large":
        return "Request Human Review"
    return "Merge"


def evaluate_policy_a(posterior_major):
    """Keep V0 Policy A thresholds unchanged."""
    if posterior_major < 8.0:
        return "Merge"
    if posterior_major <= 45.0:
        return "Request Human Review"
    return "Decline / Block"


def evaluate_policy_b(posterior_major):
    """Keep V0 Policy B thresholds unchanged."""
    if posterior_major < 2.0:
        return "Merge"
    if posterior_major <= 20.0:
        return "Request Human Review"
    return "Decline / Block"
