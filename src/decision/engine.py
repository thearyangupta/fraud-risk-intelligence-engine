REVIEW_THRESHOLD = 0.50
BLOCK_THRESHOLD = 0.80


def make_decision(risk_score: float) -> str:
    """Convert a fraud risk score into an operational decision."""

    if not 0.0 <= risk_score <= 1.0:
        raise ValueError(
            "risk_score must be between 0.0 and 1.0"
        )

    if risk_score >= BLOCK_THRESHOLD:
        return "block"

    if risk_score >= REVIEW_THRESHOLD:
        return "review"

    return "allow"