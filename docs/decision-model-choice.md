# Decision-Layer Model Choice

## Selected Model

The decision layer will use **v3 XGBoost** as its primary risk-scoring model.

## Why v3

The model was selected using validation results only. The held-out test set has
not been used for this decision.

The relevant validation results are:

| Version | Model | Precision | Recall | F1 | PR-AUC |
|---|---|---:|---:|---:|---:|
| v1 | Rule baseline | 0.1357 | 0.4137 | 0.2044 | — |
| v2 | Logistic regression | 0.0406 | 0.8786 | 0.0776 | 0.1611 |
| v3 | XGBoost | 0.0513 | 0.9305 | 0.0972 | 0.5173 |
| v4 | Isolation Forest | 0.0692 | 0.2907 | 0.1118 | 0.0736 |

v3 has the strongest ranking performance among the learned models, with a
validation PR-AUC of 0.5173 and ROC-AUC of 0.9721.

At the previously evaluated 0.5 threshold it also achieved 0.9305 recall,
showing strong fraud coverage.

v1 has a higher F1 at its manually defined operating rule, but it does not
provide the learned probability-ranking model needed for the two-threshold
decision policy.

v4 provides a useful complementary anomaly signal and caught five fraud cases
that v3 missed. However, its overall fraud-ranking performance is substantially
weaker than v3.

For the final decision layer, v3 will therefore remain the single primary model.
This keeps the policy simple and avoids introducing an additional anomaly-score
threshold before final evaluation.

## Decision Shape

v3 outputs a fraud-risk probability.

Two thresholds will convert that score into three actions:

```text
risk score
0.0 ---------------------------------------------- 1.0

        review threshold       block threshold
               |                     |
               v                     v

     ALLOW          REVIEW             BLOCK