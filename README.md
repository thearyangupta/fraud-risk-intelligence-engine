# Fraud Risk Intelligence Engine

A transaction risk and fraud-detection engine built around point-in-time behavioral features, temporal evaluation, and multiple classical ML approaches.

![CI](https://github.com/thearyangupta/fraud-risk-intelligence-engine/actions/workflows/ci.yml/badge.svg)

## Overview

The project explores fraud detection as a temporal, highly imbalanced classification problem.

The pipeline currently covers:

* temporal train/validation/test splitting
* data validation and leakage protection
* behavioral feature engineering
* rule-based and supervised ML baselines
* tree-based modeling
* unsupervised anomaly detection
* model experiment tracking
* automated testing and CI

The final test split remains untouched during model development and model selection.

## Data

The project uses a Sparkov-style synthetic credit-card transaction dataset.

Raw data is stored locally under `data/` and is not committed to the repository.

Dataset source: https://www.kaggle.com/datasets/kartik2112/fraud-detection/data

## Pipeline

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
Point-in-Time Feature Engineering
       |
       +----------------------+
       |                      |
       v                      v
Supervised Models       Isolation Forest
       |                      |
       +----------+-----------+
                  |
                  v
             Evaluation
                  |
                  v
           Model Versioning
```

## Point-in-Time Feature Engineering

Behavioral features are computed using only information available before the transaction being scored.

### Velocity

* previous 10-minute transaction count
* previous 1-hour transaction count
* previous 24-hour transaction count
* seconds since previous transaction

### Amount Behavior

* prior transaction count
* prior average amount
* prior amount standard deviation
* amount-to-prior-average ratio
* amount z-score versus prior behavior
* insufficient-history flag

### Novelty

* new merchant flag
* new category flag

Historical windows exclude the current transaction to prevent future-information leakage.

A dedicated regression test protects this point-in-time boundary.

## Model Evolution

All model development and selection uses the validation split.

| Version | Model               | Precision | Recall |     F1 | ROC-AUC | PR-AUC |
| ------- | ------------------- | --------: | -----: | -----: | ------: | -----: |
| v1      | Rule Baseline       |    0.1357 | 0.4137 | 0.2044 |       — |      — |
| v2      | Logistic Regression |    0.0406 | 0.8786 | 0.0776 |  0.9161 | 0.1611 |
| v3      | XGBoost             |    0.0513 | 0.9305 | 0.0972 |  0.9721 | 0.5173 |
| v4      | Isolation Forest    |    0.0692 | 0.2907 | 0.1118 |       — | 0.0736 |

### v1 — Rule Baseline

The initial baseline flags transactions using interpretable behavioral rules based on unusually large amounts, new merchants, and recent transaction velocity.

It establishes a simple benchmark before learned models are introduced.

### v2 — Logistic Regression

The first learned baseline uses class-weighted logistic regression with standardized behavioral features.

It substantially increased recall over v1, while demonstrating the trade-off between fraud coverage and false positives in an imbalanced dataset.

### v3 — XGBoost

Random Forest and XGBoost were compared on the same validation period.

XGBoost was selected as v3 because it produced the strongest ranking performance:

* ROC-AUC: `0.9721`
* PR-AUC: `0.5173`
* Recall: `0.9305`

The strongest feature was `amount_to_prior_avg_ratio`, followed by prior spending behavior and amount-deviation signals.

### v4 — Isolation Forest

v4 introduces unsupervised anomaly detection.

Isolation Forest was trained on behavioral features **without using fraud labels**.

Validation results:

* Precision: `0.0692`
* Recall: `0.2907`
* F1: `0.1118`
* PR-AUC: `0.0736`

v3 remains substantially stronger at ranking labelled fraud. However, v4 caught **5 fraud transactions that v3 missed**, demonstrating a small complementary anomaly signal.

The intended architecture is therefore to use supervised fraud scoring as the primary signal and anomaly detection as a secondary review signal rather than treating the two approaches as interchangeable.

See `docs/supervised-vs-unsupervised.md` for the detailed trade-off analysis.

## Key Findings

**Class imbalance makes accuracy misleading.**
Fraud detection requires metrics such as precision, recall, F1, and especially PR-AUC rather than relying on accuracy alone.

**Temporal correctness matters.**
Historical features must stop before the transaction being scored. Including the current or future transaction would create leakage.

**Customer-relative amount behavior is highly informative.**
The strongest v3 features were dominated by amount deviation relative to prior customer behavior.

**Thresholds and ranking quality are different problems.**
Precision, recall, and F1 describe a particular operating threshold, while PR-AUC measures ranking quality across thresholds.

**Anomaly is not the same as fraud.**
Isolation Forest can identify unusual behavior without labels, but unusual legitimate activity also creates false positives.

**Supervised and unsupervised models can provide different signals.**
v4 performed substantially worse than v3 overall but still detected 5 fraud cases missed by v3.

## Data & Engineering Safeguards

The project includes:

* chronological train/validation/test boundaries
* split-local feature generation
* exclusion of the current transaction from historical windows
* schema and range validation
* fraud-label sanity checks
* automated leakage regression testing
* Ruff static analysis
* GitHub Actions CI

PostgreSQL was also used to practise and validate temporal transaction analysis with SQL window functions such as `LAG`, `ROW_NUMBER`, and historical rolling windows.

## Experiment Tracking

`metrics.csv` tracks model iterations with:

* version
* model
* features used
* precision
* recall
* F1
* experiment notes

Current progression:

```text
v1  Rules
 |
 v
v2  Logistic Regression
 |
 v
v3  XGBoost
 |
 v
v4  Isolation Forest
```

This keeps model changes and validation results explicit rather than relying on ad-hoc notebook comparisons.

## Testing

The project currently includes automated tests covering:

* temporal splitting
* schema validation
* value and null validation
* fraud-label sanity
* point-in-time feature leakage

Run locally with:

```bash
python -m pytest tests -q
ruff check src tests
```

CI runs the test and lint checks automatically on pushes.

## Current Architecture

```text
Transactions
     |
     v
Validation
     |
     v
Temporal Split
     |
     v
Behavioral Features
     |
     +---------------------+
     |                     |
     v                     v
XGBoost Risk Score   Isolation Forest
     |               Anomaly Signal
     +----------+----------+
                |
                v
       Future Decision Layer
       Allow / Review / Block
```