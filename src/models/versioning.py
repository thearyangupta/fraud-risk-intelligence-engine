import csv
from pathlib import Path

METRICS_COLUMNS = [
    "version",
    "model",
    "features_used",
    "precision",
    "recall",
    "f1",
    "notes",
]


def log_model_metrics(
    metrics_path: str | Path,
    version: str,
    model: str,
    features_used: str,
    precision: float,
    recall: float,
    f1: float,
    notes: str,
) -> None:
    path = Path(metrics_path)

    file_exists = path.exists() and path.stat().st_size > 0

    with path.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=METRICS_COLUMNS,
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "version": version,
                "model": model,
                "features_used": features_used,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "notes": notes,
            }
        )