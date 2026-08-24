# Dataset Decision

## Selected Dataset

Sparkov-style synthetic credit card transaction dataset.

## Why This Dataset

### 1. Supports Point-in-Time Behavioural Features

The dataset provides transaction timestamps, an anonymized card/account identifier, and transaction amounts. These fields allow transaction history to be ordered in time and support behavioural features such as transaction velocity and amount deviation using only prior transactions.

### 2. Provides Interpretable Merchant Information

The dataset includes merchant and merchant-category information. This supports features such as whether an account is interacting with a new merchant or an unusual merchant category, rather than relying primarily on anonymized transformed variables.

### 3. Provides Geographic Information

Customer and merchant location information is available, allowing geographic behaviour to be investigated and potentially used for point-in-time fraud features.

## Known Limitations

### Synthetic Data

The dataset is synthetic rather than real production transaction data. Fraud patterns may therefore be cleaner or less complex than real-world fraud. Results from this project should not be interpreted as evidence of equivalent production performance.

### No Device Information

The dataset does not provide a device identifier. Device-based features such as whether a transaction originates from a previously unseen device cannot be built.

### Anonymized Account Identity

The card/account identifier allows transactions to be grouped into behavioural histories, but it should be treated as an anonymized account identifier rather than a real-world customer identity.

## Prediction-Time Constraint

Features built from transaction history must use only information available before the transaction being scored. Future transactions must never be included when computing historical behavioural features.