# Feature Hypotheses

The goal of this document is to define the behavioural signals I expect may help distinguish fraudulent transactions from legitimate ones before implementing any feature engineering.

Each hypothesis must satisfy one rule:

> Features may only use information available strictly before the transaction timestamp.

---

## 1. Transaction Velocity

### Hypothesis

An unusually high number of transactions from the same account within a short period may be associated with fraud.

### Reasoning

A legitimate customer may normally make transactions with some spacing between them. If an account suddenly performs several transactions within a very short time window, it may indicate automated activity or an attacker attempting to use the account rapidly.

### Expected Relationship

Higher recent transaction counts within short time windows may correlate with a higher likelihood of fraud.

Potential future behavioural measures could include:

* transactions in the previous few minutes
* transactions in the previous hour
* time since the previous transaction

### Prediction-Time Availability

**Available at prediction time: Yes**

This feature can be computed using only transactions belonging to the same account that occurred before the current transaction.

Future transactions must not be included.

---

## 2. Amount Deviation From Historical Behaviour

### Hypothesis

A transaction amount that is significantly different from an account's previous spending behaviour may be associated with fraud.

### Reasoning

A transaction should not be considered suspicious only because its absolute amount is large.

The same amount may be normal for one customer but highly unusual for another.

The more useful question is:

> How unusual is the current transaction amount compared with this account's previous transactions?

### Expected Relationship

A large positive deviation from the account's historical transaction amount may correlate with a higher likelihood of fraud.

Potential future behavioural measures could compare the current amount with:

* the account's previous average amount
* the account's previous median amount
* recent transaction amounts

### Prediction-Time Availability

**Available at prediction time: Yes**

Historical statistics must be calculated using only transactions that occurred before the current transaction.

Using the full account history, including future transactions, would cause data leakage.

---

## 3. Unusual Transaction Timing

### Hypothesis

A transaction occurring at a time that is unusual relative to an account's previous behaviour may be associated with fraud.

### Reasoning

Customers may develop recurring transaction-time patterns.

For example, an account that normally transacts during daytime hours may behave unusually if a transaction suddenly occurs late at night.

The important comparison is not simply whether the transaction occurs at a globally unusual hour, but whether that hour is unusual for the specific account.

### Expected Relationship

Transactions occurring outside an account's normal historical activity hours may correlate with a higher likelihood of fraud.

Potential future behavioural measures could include:

* whether the transaction hour has been observed previously for the account
* deviation from normal transaction hours
* transaction activity during historically uncommon periods

### Prediction-Time Availability

**Available at prediction time: Yes**

The current timestamp and historical transaction timestamps are available when the transaction arrives.

Only previous transaction history may be used.

---

## 4. New Merchant or Merchant Category

### Hypothesis

A transaction with a merchant or merchant category that has not previously appeared in an account's history may be associated with fraud.

### Reasoning

Customers often develop recurring merchant and category patterns.

A first-time merchant or category may represent unusual behaviour, particularly when combined with other unusual signals such as a high amount.

However, a new merchant alone does not imply fraud because legitimate customers regularly purchase from new businesses.

### Expected Relationship

First-time merchant interactions or previously unseen merchant categories may correlate with increased fraud risk, especially when combined with other behavioural anomalies.

Potential future behavioural measures could include:

* whether the merchant has previously been used by the account
* whether the merchant category has previously been seen
* number of previous transactions with the merchant or category

### Prediction-Time Availability

**Available at prediction time: Yes**

The current merchant/category and previous transaction history are available when the transaction occurs.

Future merchant interactions must not be used.

---

## 5. Geographic Anomaly

### Hypothesis

A transaction occurring at a location that is unusual compared with an account's previous transaction locations may be associated with fraud.

### Reasoning

An account may normally transact within a relatively consistent geographic area.

A transaction occurring far from previously observed behaviour may represent unusual account activity.

However, geographic change alone does not imply fraud because legitimate customers may travel or make purchases from distant merchants.

### Expected Relationship

Large geographic deviations from an account's historical transaction behaviour may correlate with increased fraud risk.

Potential future behavioural measures could include:

* distance from previously observed transaction locations
* distance from the account's typical geographic area
* whether the current location is new for the account

### Prediction-Time Availability

**Available at prediction time: Yes**

The dataset contains geographic information for the current transaction and prior transactions.

Only historical locations from transactions before the current transaction may be used.

---

## 6. Device-Based Behaviour

### Hypothesis

A transaction from a previously unseen device could potentially be associated with fraud.

### Dataset Limitation

The selected dataset does not provide a usable device identifier.

Therefore, this hypothesis cannot currently be implemented with this dataset.

### Prediction-Time Availability

**Not computable with the selected dataset**

This hypothesis should be dropped rather than approximated using unrelated columns or fabricated information.

---

# Prediction-Time Review

| Hypothesis            | Computable at Prediction Time?     | Dataset Supports It? |
| --------------------- | ---------------------------------- | -------------------- |
| Transaction velocity  | Yes                                | Yes                  |
| Amount deviation      | Yes                                | Yes                  |
| Unusual timing        | Yes                                | Yes                  |
| New merchant/category | Yes                                | Yes                  |
| Geographic anomaly    | Yes                                | Yes                  |
| New device            | Potentially yes in another dataset | No                   |

---

# Core Principle

A feature is valid only if its value could have been calculated when the transaction being scored arrived.

For transaction **T**, only information from transactions before **T** may contribute to behavioural features.

Future transactions, investigation outcomes, chargeback information, or the fraud label itself must never be used as predictive inputs.

These hypotheses will be tested later rather than assumed to be true.