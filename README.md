# Fraud Risk Intelligence Engine

Fraud-risk scoring system built on point-in-time behavioral features, temporal evaluation, and an operational ALLOW / REVIEW / BLOCK decision policy.

![CI](https://github.com/thearyangupta/fraud-risk-intelligence-engine/actions/workflows/ci.yml/badge.svg)

## Overview

An end-to-end fraud-risk pipeline that validates transaction data, preserves chronological train/validation/test boundaries, builds leakage-safe behavioral features, compares rule-based/linear/tree/anomaly-detection models, converts scores into operational decisions, and evaluates the locked system once on held-out test data — exposed via a local FastAPI endpoint.

Focus: **temporal correctness, leakage prevention, and decision-oriented evaluation** — not just predictive accuracy.

## Architecture

```text
Raw Transactions -> Validation -> Temporal Split (train/val/test)
    -> Point-in-Time Features
        -> Supervised Models (rules, logistic regression, XGBoost)
        -> Isolation Forest (anomaly signal)
    -> Selected Model (v3 XGBoost) -> Risk Score
    -> Decision Engine -> ALLOW / REVIEW / BLOCK
    -> Local FastAPI Interface
```

## Data

Sparkov-style synthetic credit-card transactions (Kaggle, Kartik2112). Stored locally under `data/`, excluded from Git. Split **chronologically**, not randomly, so evaluation reflects scoring future transactions from historical behavior.

Dataset source: https://www.kaggle.com/datasets/kartik2112/fraud-detection/data

## Behavioral Features

Computed using only information available **before** the transaction being scored; the current transaction is excluded from its own historical stats. A regression test protects this boundary.

| Group | Features |
|---|---|
| Velocity | 10-min / 1-hr / 24-hr prior transaction counts; seconds since previous transaction |
| Amount behavior | prior count, prior mean/std, amount-to-prior-average ratio, historical z-score, insufficient-history flag |
| Novelty | new merchant / new category indicators |

## Model Comparison (validation)

| Version | Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| v1 | Rule Baseline | 0.1357 | 0.4137 | 0.2044 | – | – |
| v2 | Logistic Regression | 0.0406 | 0.8786 | 0.0776 | 0.9161 | 0.1611 |
| v3 | **XGBoost (selected)** | 0.0513 | 0.9305 | 0.0972 | 0.9721 | 0.5173 |
| v4 | Isolation Forest | 0.0692 | 0.2907 | 0.1118 | – | 0.0736 |

**v3 XGBoost** selected as primary model — best PR-AUC (0.5173) and recall (0.9305) at threshold 0.50. Strongest feature: `amount_to_prior_avg_ratio`.

Isolation Forest kept as a secondary signal — weaker overall, but caught 5 validation fraud cases v3 missed, confirming it captures different patterns.

## Decision Policy

Thresholds chosen on validation, before the test set was opened — and never changed afterward.

```text
risk_score < 0.50   -> ALLOW
0.50 <= score < 0.80 -> REVIEW
risk_score >= 0.80   -> BLOCK
```

## Final Held-Out Test (opened once)

| Metric | Result |
|---|---:|
| Precision | 0.0449 |
| Recall | 0.9417 |
| F1 | 0.0857 |
| ROC-AUC | 0.9731 |
| PR-AUC | 0.4835 |

| Decision | Transactions | Fraud | Fraud Share |
|---|---:|---:|---:|
| ALLOW | 170,736 | 66 | 5.83% |
| REVIEW | 14,067 | 80 | 7.06% |
| BLOCK | 9,699 | 987 | 87.11% |

Of 1,133 fraud transactions, the locked policy routed **1,067** to REVIEW/BLOCK. Test ROC-AUC (0.9731) held close to validation (0.9721); PR-AUC dropped modestly (0.5173 → 0.4835). No changes were made after seeing these results.

## Local API

```bash
uvicorn src.api.app:app --reload
```

- `GET /health`
- `POST /predict` → `{"risk_score": 0.75, "decision": "review"}`

Reuses the same feature engineering, XGBoost scoring, and decision logic as the offline pipeline. A local demonstration, not a production serving architecture.

## Repository Structure

```text
src/
  api/        local FastAPI interface
  data/       validation, preprocessing, temporal split
  db/         SQL schema and temporal analysis
  decision/   threshold selection and decision engine
  eval/       model and final test evaluation
  features/   behavioral feature engineering
  models/     rules, logistic regression, trees, anomaly detection
tests/        regression and correctness tests
notebooks/    exploration history
reports/      generated evaluation artifacts
metrics.csv   model experiment history
```

## Run Locally

```bash
pip install -r requirements.txt
# dataset expected at data/fraudTrain.csv
python -m pytest tests -q
ruff check src tests
```

CI runs import, test, and lint checks on every push.

## Engineering Safeguards

Chronological data split · point-in-time feature construction · current-transaction exclusion · schema/range/null/label validation · dedicated leakage regression test · frozen validation-selected thresholds · one-time held-out evaluation · versioned experiment tracking (`metrics.csv`) · automated tests + CI.

## Limitations

Portfolio-scale, not production: synthetic data, model trained at API startup (no versioned artifact), no persistent feature store, no probability calibration, no cost-sensitive threshold optimization, no monitoring/drift detection, no auth or deployment infra.

## Key Takeaway

Fraud detection is more than fitting a classifier. This project demonstrates the full chain:

**time-correct data → leakage-safe features → appropriate evaluation → frozen model selection → operational thresholds → reproducible serving logic** — treated as one testable pipeline, not a single accuracy number.