# Supervised vs. Unsupervised Fraud Detection

## Context

This project now contains two fundamentally different approaches to fraud
detection.

The supervised models learn from historical fraud labels. The strongest
supervised model so far is v3, an XGBoost gradient-boosting classifier.

The unsupervised v4 model uses Isolation Forest. It is trained using transaction
features only and does not use the `is_fraud` label during fitting.

The purpose of v4 is not simply to outperform v3. It provides a structurally
different signal: whether a transaction is unusual relative to the feature
distribution rather than whether it resembles previously labelled fraud.

## Supervised Detection

Supervised models learn a relationship between transaction features and known
fraud labels.

In this project, v2 logistic regression and v3 XGBoost are supervised models.

### Strengths

Supervised learning is effective when future fraud resembles fraud represented
in the training data.

Because the model has access to known fraud outcomes during training, it can
directly learn which feature patterns are associated with fraud.

The current v3 model demonstrates this advantage clearly on validation:

- Precision: 0.0513
- Recall: 0.9305
- F1: 0.0972
- PR-AUC: 0.5173

Its high recall means that, at the current 0.5 decision threshold, it identifies
most labelled fraud transactions in the validation period.

Its PR-AUC also shows substantially stronger fraud-ranking ability than the
unsupervised model.

### Weaknesses

A supervised model depends on labelled historical examples.

If a genuinely new fraud strategy produces behavior unlike anything represented
in the labelled training data, the model may assign it a low fraud score.

The model is therefore strongest at learning relationships represented in its
historical labels, but those labels cannot guarantee coverage of future fraud
patterns.

## Unsupervised Detection

v4 uses Isolation Forest.

Unlike the supervised models, Isolation Forest was fitted using only the Week 4
behavioral features. The fraud target was not passed into model training.

Isolation Forest looks for observations that are relatively easy to isolate
through random feature splits.

Transactions requiring unusually short isolation paths are treated as more
anomalous.

### Strengths

The main advantage is that labelled fraud examples are not required for
training.

This makes anomaly detection useful when labels are unavailable, incomplete,
delayed, or when the goal is to surface unusual behavior that may not resemble
known fraud.

It therefore provides a different detection signal from a supervised
classifier.

### Weaknesses

Unusual behavior is not necessarily fraudulent.

A legitimate customer can make a rare large purchase, transact unusually
frequently, visit a new merchant, or otherwise behave differently from their
historical pattern.

An anomaly detector can therefore flag legitimate but unusual transactions.

The v4 validation results illustrate this limitation:

- Precision: 0.0692
- Recall: 0.2907
- F1: 0.1118
- PR-AUC: 0.0736
- Fraud caught: 364 of 1,252
- Legitimate transactions flagged: 4,897

Although threshold-dependent precision and F1 differ from v3, the clearest
ranking comparison is PR-AUC. v3 achieved 0.5173 compared with 0.0736 for v4,
showing that v3 is substantially stronger at ranking labelled fraud in this
validation period.

## v3 vs. v4 Overlap

The most useful comparison is not simply which model has the larger metric.

Among the 1,252 validation fraud transactions:

| Detection group | Fraud transactions |
| --- | ---: |
| Caught by both v3 and v4 | 359 |
| Caught by v3 only | 806 |
| Caught by v4 only | 5 |
| Caught by neither | 82 |

v3 therefore caught 1,165 fraud transactions, while v4 caught 364.

The important result is that Isolation Forest caught 5 fraud transactions that
v3 missed.

This does not prove that v4 should automatically be combined with v3. Isolation
Forest also generated many legitimate anomaly flags, so any combined strategy
would need to consider false-positive cost and review capacity.

However, the five v4-only fraud cases show that the anomaly detector provides
at least some complementary detection signal.

## How I Would Deploy Them

In a real fraud system, I would not treat the supervised and unsupervised
models as interchangeable.

The supervised model would be the primary fraud-risk signal because it has much
stronger performance against the available labelled validation data.

The unsupervised model would be a secondary anomaly signal.

For example, a transaction receiving a low supervised fraud score but a very
high anomaly score could be routed for additional review rather than
automatically treated as fraud.

Conceptually:

    transaction
        |
        +--> supervised fraud score
        |
        +--> anomaly score
        |
        v
    decision layer
        |
        +--> allow
        +--> review
        +--> block

The decision layer should consider the different meanings of the two scores,
along with false-positive and false-negative costs.

## Conclusion

Supervised fraud detection asks:

> Does this transaction resemble patterns associated with known fraud?

Unsupervised anomaly detection asks:

> Does this transaction look unusual relative to the learned feature
> distribution?

Those questions overlap, but they are not identical.

For this dataset, v3 is clearly stronger at ranking labelled fraud. v4 is not a
replacement for it.

The useful Week 8 finding is that v4 still identified 5 fraud cases missed by
v3, demonstrating a small but concrete complementary signal that could be
investigated further in a future decision layer.