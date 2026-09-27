# Fraud Risk Intelligence Engine

A fraud-risk scoring system built around point-in-time behavioral features, temporal evaluation, supervised and unsupervised modeling, and an operational **ALLOW / REVIEW / BLOCK** decision policy.

![CI](https://github.com/thearyangupta/fraud-risk-intelligence-engine/actions/workflows/ci.yml/badge.svg)

## Overview

Fraud detection is a highly imbalanced, time-dependent classification problem.

This project builds an end-to-end fraud-risk pipeline that:

- validates transaction data
- preserves chronological train/validation/test boundaries
- creates leakage-safe behavioral features
- compares rule-based, linear, tree-based, and anomaly-detection approaches
- converts model scores into operational decisions
- evaluates the locked system once on held-out test data
- exposes the final scoring pipeline through a local FastAPI endpoint

The focus is not only predictive performance, but also **temporal correctness, leakage prevention, reproducibility, and decision-oriented model evaluation**.

## Architecture

```text
Raw Transactions
       |
       v
Data Validation
       |
       v
Temporal Train / Validation / Test Split
       |
       v
Point-in-Time Behavioral Features
       |
       +-------------------------+
       |                         |
       v                         v
Supervised Models        Isolation Forest
       |
       v
Selected v3 XGBoost
       |
       v
Fraud Risk Score
       |
       v
Decision Engine
       |
  +----+----+
  |    |    |
ALLOW REVIEW BLOCK
       |
       v
Local FastAPI Interface
```

## Data

The project uses a Sparkov-style synthetic credit-card transaction dataset.

Raw data is stored locally under `data/` and is excluded from Git.

Dataset source: Kaggle â€” Fraud Detection by Kartik2112.

The data is split chronologically rather than randomly so evaluation better reflects scoring future transactions from historical behavior.

## Behavioral Features

Features are computed using only information available **before the transaction being scored**.

| Group | Features |
|---|---|
| Velocity | 10-minute, 1-hour and 24-hour prior transaction counts; seconds since previous transaction |
| Amount behavior | prior transaction count, prior mean/std amount, amount-to-prior-average ratio, historical z-score, insufficient-history flag |
| Novelty | new merchant and new category indicators |

The current transaction is excluded from its own historical statistics.

A regression test protects this point-in-time boundary.

## Model Comparison

Model development and selection were performed on the validation period.

| Version | Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| v1 | Rule Baseline | 0.1357 | 0.4137 | 0.2044 | - | - |
| v2 | Logistic Regression | 0.0406 | 0.8786 | 0.0776 | 0.9161 | 0.1611 |
| v3 | XGBoost | 0.0513 | 0.9305 | 0.0972 | 0.9721 | 0.5173 |
| v4 | Isolation Forest | 0.0692 | 0.2907 | 0.1118 | - | 0.0736 |

### Selected Model

**v3 XGBoost** was selected as the primary fraud-ranking model.

On validation:

- ROC-AUC: `0.9721`
- PR-AUC: `0.5173`
- Recall at threshold 0.50: `0.9305`

`amount_to_prior_avg_ratio` was the strongest model feature, highlighting the importance of evaluating transaction amounts relative to a customer's previous behavior.

Isolation Forest was retained as an experimental anomaly signal. It performed substantially worse overall but identified 5 validation fraud cases missed by v3, illustrating that anomaly detection and supervised fraud prediction capture different signals.

## Decision Policy

Validation data was used to select the operating policy before the test set was opened.

```text
risk_score < 0.50
    -> ALLOW

0.50 <= risk_score < 0.80
    -> REVIEW

risk_score >= 0.80
    -> BLOCK
```

This separates **risk estimation** from **business action**.

On validation:

| Decision | Transactions | Fraud |
|---|---:|---:|
| ALLOW | 171,781 | 87 |
| REVIEW | 13,088 | 94 |
| BLOCK | 9,632 | 1,071 |

After these thresholds were locked, they were not changed using test results.

## Final Held-Out Test

The held-out test set was opened once after model and policy selection were complete.

### Model Metrics

| Metric | Test Result |
|---|---:|
| Precision | 0.0449 |
| Recall | 0.9417 |
| F1 | 0.0857 |
| ROC-AUC | 0.9731 |
| PR-AUC | 0.4835 |

### Operational Results

| Decision | Transactions | Fraud | Transaction Rate | Fraud Share |
|---|---:|---:|---:|---:|
| ALLOW | 170,736 | 66 | 87.78% | 5.83% |
| REVIEW | 14,067 | 80 | 7.23% | 7.06% |
| BLOCK | 9,699 | 987 | 4.99% | 87.11% |

Out of **1,133 fraud transactions**, the locked policy routed **1,067** to REVIEW or BLOCK and allowed **66**.

The test ROC-AUC (`0.9731`) remained close to validation (`0.9721`), while test PR-AUC decreased from `0.5173` to `0.4835`.

No model or threshold changes were made after observing the held-out test results.

## Local API

A thin FastAPI layer demonstrates how the existing fraud pipeline can be exposed to an application.

Start locally:

```bash
uvicorn src.api.app:app --reload
```

Health check:

```text
GET /health
```

Prediction:

```text
POST /predict
```

Example request:

```json
{
  "cc_num": 2703186189652095,
  "trans_date_trans_time": "2020-06-22 12:00:00",
  "merchant": "example_merchant",
  "category": "shopping_net",
  "amt": 500.0
}
```

Example response shape:

```json
{
  "risk_score": 0.75,
  "decision": "review"
}
```

The API reuses the same feature engineering, XGBoost scoring, and decision logic used by the offline pipeline.

It is intentionally a local demonstration rather than a production serving architecture.

## Repository Structure

```text
fraud-risk-intelligence-engine/
|
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ api/          # local FastAPI interface
â”‚   â”œâ”€â”€ data/         # validation, preprocessing, temporal split
â”‚   â”œâ”€â”€ db/           # SQL schema and temporal analysis
â”‚   â”œâ”€â”€ decision/     # threshold selection and decision engine
â”‚   â”œâ”€â”€ eval/         # model and final test evaluation
â”‚   â”œâ”€â”€ features/     # behavioral feature engineering
â”‚   â””â”€â”€ models/       # rules, logistic regression, trees, anomaly detection
â”‚
â”œâ”€â”€ tests/            # regression and correctness tests
â”œâ”€â”€ notebooks/        # exploration history
â”œâ”€â”€ reports/          # generated evaluation artifacts
â”œâ”€â”€ metrics.csv       # model experiment history
â””â”€â”€ requirements.txt
```

## Run Locally

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

The raw dataset must be available locally at:

```text
data/fraudTrain.csv
```

Run tests:

```bash
python -m pytest tests -q
```

Run linting:

```bash
ruff check src tests
```

GitHub Actions runs automated import, test, and lint checks on pushes.

## Engineering Safeguards

The project includes:

- chronological train/validation/test separation
- point-in-time historical feature construction
- current-transaction exclusion from historical windows
- schema, range, null, and label validation
- dedicated leakage regression testing
- frozen validation-selected decision thresholds
- one-time held-out test evaluation
- explicit model experiment tracking
- automated tests and CI

## Limitations

This is a portfolio-scale fraud-risk system, not a production payment platform.

Current limitations include:

- synthetic rather than real financial transaction data
- static historical context in the local API
- model training at API startup instead of loading a versioned model artifact
- no persistent online feature store
- no probability calibration
- no cost-sensitive optimization using real fraud-loss/review costs
- no production monitoring or drift detection
- no authentication or deployment infrastructure

## Future Improvements

A production-oriented extension could add:

- persisted and versioned model artifacts
- online point-in-time feature storage
- calibrated probabilities
- cost-aware threshold optimization
- drift and performance monitoring
- model registry and reproducible training pipelines
- authenticated deployment and observability

## Key Takeaway

The project demonstrates that fraud detection is more than fitting a classifier.

A useful fraud-risk system requires:

**time-correct data -> leakage-safe behavioral features -> appropriate evaluation -> frozen model selection -> operational thresholds -> reproducible serving logic**

The final system combines those pieces into a testable fraud-risk pipeline rather than treating model accuracy as the entire problem.
