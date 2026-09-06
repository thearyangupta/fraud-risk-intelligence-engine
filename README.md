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