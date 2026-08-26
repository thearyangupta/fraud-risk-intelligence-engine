A transaction risk & fraud scoring engine. Classical ML, built to learn data/ML fundamentals.

## Data

This project uses a Sparkov-style synthetic credit card transaction dataset.

The raw dataset is stored locally under `data/` and is not committed to the repository.

Dataset source: https://www.kaggle.com/datasets/kartik2112/fraud-detection/data


## Problem Framing & Dataset Understanding

focused on understanding the fraud-detection problem before building any model.

Completed work:

- Defined what the system is trying to predict and documented the prediction-time information boundary.
- Evaluated multiple fraud datasets using criteria such as timestamps, account identity, transaction amount, merchant information, labels, size, and license.
- Selected a Sparkov-style synthetic credit-card transaction dataset because it supports interpretable behavioural analysis using timestamps, account identity, transaction amounts, merchant/category information, and geographic data.
- Performed an initial exploratory analysis of the dataset, including structure, missing values, class imbalance, transaction-amount distributions, and time-based fraud patterns.
- Wrote behavioural feature hypotheses covering transaction velocity, amount deviation, unusual timing, new merchant/category behaviour, and geographic anomalies.
- Reviewed each hypothesis for prediction-time availability to avoid future-information leakage.

No machine-learning model has been trained yet. The focus was problem framing, data understanding, and building a point-in-time-correct foundation for later feature engineering and modeling.