import pytest

from src.decision.engine import make_decision


@pytest.mark.parametrize(
    ("risk_score", "expected"),
    [
        (0.00, "allow"),
        (0.20, "allow"),
        (0.4999, "allow"),
        (0.50, "review"),
        (0.65, "review"),
        (0.7999, "review"),
        (0.80, "block"),
        (0.95, "block"),
        (1.00, "block"),
    ],
)
def test_make_decision(
    risk_score: float,
    expected: str,
) -> None:
    assert make_decision(risk_score) == expected


@pytest.mark.parametrize(
    "risk_score",
    [
        -0.01,
        1.01,
    ],
)
def test_make_decision_rejects_invalid_scores(
    risk_score: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="risk_score must be between 0.0 and 1.0",
    ):
        make_decision(risk_score)