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


## Logistic Regression v2

The first learned ML baseline uses logistic regression on the point-in-time behavioral features developed in Week 4.

Two class-imbalance strategies were tested: balanced class weighting and random minority oversampling. Their validation probability distributions were nearly identical, so class weighting was selected because it avoids duplicating observations and substantially increasing the effective training dataset.

Validation results at a 0.5 decision threshold:

| Metric | v1 Rules | v2 Logistic Regression |
|---|---:|---:|
| Precision | 0.1357 | 0.0406 |
| Recall | 0.4137 | 0.8786 |
| F1 | 0.2044 | 0.0776 |
| ROC-AUC | — | 0.9161 |
| PR-AUC / AP | — | 0.1611 |

v2 substantially improves recall at the default threshold, but precision and F1 are lower than the v1 rule baseline. The result demonstrates that model ranking quality and the final operating threshold are separate concerns.

The strongest positive standardized coefficient was `amount_to_prior_avg_ratio`, while `txn_count_1h_before` also contributed positively.

The next modeling lever to investigate is decision-threshold tuning.

See `v2-writeup.md` for the full v2 analysis.


## Model Evolution

The fraud-risk engine has progressed through three model versions. Model development and selection use the validation split; the final test split remains untouched during model selection.

| Version | Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| v1 | Rule Baseline | 0.1357 | 0.4137 | 0.2044 | — | — |
| v2 | Logistic Regression | 0.0406 | 0.8786 | 0.0776 | 0.9161 | 0.1611 |
| v3 | Gradient Boosting / XGBoost | 0.0513 | 0.9305 | 0.0972 | 0.9721 | 0.5173 |

### Model Selection

Random Forest and Gradient Boosting were compared against the v2 logistic-regression model using the same validation split.

Random Forest produced substantially higher precision and F1 at the default 0.5 threshold:

- Precision: 0.3477
- Recall: 0.5855
- F1: 0.4363
- ROC-AUC: 0.9633
- PR-AUC: 0.4136

Gradient Boosting produced:

- Precision: 0.0513
- Recall: 0.9305
- F1: 0.0972
- ROC-AUC: 0.9721
- PR-AUC: 0.5173

Gradient Boosting was selected as the v3 candidate because it produced the strongest validation PR-AUC and ROC-AUC and the highest recall among the compared learned models.

Random Forest demonstrated a different operating trade-off, with substantially stronger precision and F1 at the default 0.5 threshold.

Because precision, recall, and F1 depend on the classification threshold, performance at 0.5 is treated as one operating point rather than a complete measure of model ranking quality.

The final test set remains sealed during model development and selection.

### Feature-Importance Findings

The selected v3 model primarily relies on customer-relative amount behavior.

The four highest-ranked features were:

1. `amount_to_prior_avg_ratio` — 0.3721
2. `prior_avg_amount` — 0.1735
3. `amount_zscore_vs_prior` — 0.1390
4. `seconds_since_prev_txn` — 0.0794

The results strongly support the original amount-deviation hypothesis and also provide evidence for transaction velocity.

Merchant and category novelty contributed substantially less than initially hypothesized.

No obvious new leakage warning was identified from the feature-importance review. Point-in-time leakage guards remain part of the project.