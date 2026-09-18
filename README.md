# Fraud Risk Intelligence Engine

A transaction risk & fraud scoring engine. Classical ML, built to learn data/ML fundamentals.

![CI](https://github.com/thearyangupta/fraud-risk-intelligence-engine/actions/workflows/ci.yml/badge.svg)

## Data

This project uses a Sparkov-style synthetic credit card transaction dataset.

The raw dataset is stored locally under `data/` and is not committed to the repository.

Dataset source: https://www.kaggle.com/datasets/kartik2112/fraud-detection/data

## Problem Framing & Dataset Understanding

Focused on understanding the fraud-detection problem before building any model.

Completed work:

- Defined what the system is trying to predict and documented the prediction-time information boundary.
- Evaluated multiple fraud datasets using criteria such as timestamps, account identity, transaction amount, merchant information, labels, size, and license.
- Selected a Sparkov-style synthetic credit-card transaction dataset because it supports interpretable behavioural analysis using timestamps, account identity, transaction amounts, merchant/category information, and geographic data.
- Performed an initial exploratory analysis of the dataset, including structure, missing values, class imbalance, transaction-amount distributions, and time-based fraud patterns.
- Wrote behavioural feature hypotheses covering transaction velocity, amount deviation, unusual timing, new merchant/category behaviour, and geographic anomalies.
- Reviewed each hypothesis for prediction-time availability to avoid future-information leakage.

No machine-learning model has been trained yet. The focus was problem framing, data understanding, and building a point-in-time-correct foundation for later feature engineering and modeling.

## Splitting, Preprocessing & Validation

It's focused on preventing data leakage and making the data pipeline reproducible and testable before any machine-learning model is introduced.

Completed work:

- Implemented a temporal train/validation/test split so the model will always learn from earlier transactions and be evaluated on later transactions.
- Kept preprocessing leak-free by fitting categorical preprocessing only on the training split and applying the learned mappings unchanged to validation and test data.
- Added data-validation checks for schema, value ranges, required null constraints, and fraud-label sanity.
- Added pytest coverage for both valid and deliberately invalid inputs using small controlled DataFrames.
- Added a temporal-order test that protects against accidental future-information leakage.
- Added GitHub Actions CI to run pytest and Ruff automatically on every push.

The split is ordered by time rather than randomly because the production problem is inherently temporal: the system must use information available in the past to score future transactions. A random split could allow later transactions to influence training while earlier transactions appear in evaluation, producing an unrealistically optimistic result.

No machine-learning model has been trained yet. The project is still focused on building a point-in-time-correct, reproducible foundation for later feature engineering and modeling.


## PostgreSQL & Temporal SQL

This week focused on moving the transaction dataset into PostgreSQL and learning temporal SQL window functions while preserving the temporal train/validation/test boundaries created in Week 2.

### Completed work

* Designed a PostgreSQL schema with `customers` and `transactions` tables.
* Preserved the temporal `train`, `val`, and `test` split inside the database using a `split` column.
* Added an index on `(customer_id, timestamp)` for customer-history queries.
* Loaded the full transaction dataset into PostgreSQL.
* Verified row counts, timestamps, required null checks, and customer transaction aggregation.
* Practised SQL window functions using real transaction histories.
* Hand-verified temporal query outputs against one customer's ordered transactions.

### Temporal signals I can now compute

* Previous transaction amount using `LAG(amount)`.
* Previous transaction timestamp using `LAG(timestamp)`.
* Transaction sequence number using `ROW_NUMBER()`.
* Historical rolling average amount over previous transactions.
* Historical recent transaction count over a fixed row window.

### Important temporal boundary

A key lesson from this week is that a historical SQL window must stop **before the current transaction** when calculating past behaviour.

For example:

* `ROWS BETWEEN 3 PRECEDING AND CURRENT ROW` includes the current transaction.
* `ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING` excludes the current transaction and represents only prior history.



No machine-learning model has been trained yet, and no LLM has been used. The project remains focused on building a correct temporal data foundation before modeling.


## Point-in-Time Feature Engineering

Built a production-style behavioral feature engineering pipeline with strict temporal correctness.

### Feature Families

**Velocity Features**
- Previous 10-minute transaction count
- Previous 1-hour transaction count
- Previous 24-hour transaction count
- Seconds since previous transaction

**Amount-Deviation Features**
- Prior transaction count
- Prior historical average amount
- Prior historical standard deviation
- Current amount / prior average ratio
- Z-score versus prior spending behavior
- Explicit insufficient-history handling

**Novelty Features**
- New merchant flag
- New category flag

### Temporal Leakage Protection

All historical features are computed using only information available **before** the current transaction.

Implemented protections include:

- chronological customer ordering
- historical window calculations
- current transaction exclusion
- split-local feature generation
- automated leakage regression tests

### Engineering Structure

```text
build_features()
    ├── velocity
    ├── amount deviation
    └── novelty
```

The feature builder produces one feature table per temporal split (`train`, `val`, `test`) while preserving point-in-time correctness.

### Testing

- 13 automated pytest tests
- Temporal split validation
- Data validation
- Point-in-time leakage guard
- Ruff static analysis


## Rule-Based Fraud Baseline

Built the project's first deliberately simple fraud detector using point-in-time features

### v1 Rules

A transaction is flagged when:

- its amount is more than 5x the customer's prior average and the merchant is new, or
- more than 3 prior transactions occurred within the previous hour.

Thresholds were checked using a few sensible validation-only passes rather than exhaustive optimization. The test split remained untouched.

### Validation Metrics

| Metric | v1 |
|---|---:|
| Precision | 0.1357 |
| Recall | 0.4137 |
| F1 | 0.2044 |
| Accuracy | 0.9793 |

Accuracy is included to demonstrate the class-imbalance problem rather than as the primary model-selection metric.

The v1 confusion matrix contains 518 true positives, 3,299 false positives, 189,950 true negatives, and 734 false negatives.

### Model Versioning

Model experiment tracking begins with `v1`.

`metrics.csv` records:

- model version
- model type
- features used
- precision
- recall
- F1
- experiment notes

The lightweight metrics log provides a baseline against which later models can be compared.

### Error Costs

False positives create legitimate-customer and operational friction, while false negatives allow fraud to pass undetected.

For this project, false negatives are treated as having a higher direct per-event cost, while recognizing that false positives can also become expensive at scale.

This cost asymmetry will later inform decision thresholds and the allow / review / block policy.