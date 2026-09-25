# v3 Feature Importance Review

## Selected v3 Model

Gradient Boosting (XGBoost) was selected as the v3 candidate using validation performance.

The final test set remains untouched.

## Feature Importance

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | amount_to_prior_avg_ratio | 0.372093 |
| 2 | prior_avg_amount | 0.173477 |
| 3 | amount_zscore_vs_prior | 0.139034 |
| 4 | seconds_since_prev_txn | 0.079444 |
| 5 | txn_count_1h_before | 0.064186 |
| 6 | prior_txn_count | 0.053697 |
| 7 | txn_count_24h_before | 0.041743 |
| 8 | prior_std_amount | 0.036660 |
| 9 | insufficient_amount_history | 0.021619 |
| 10 | is_new_merchant | 0.011258 |
| 11 | is_new_category | 0.003523 |
| 12 | txn_count_10m_before | 0.003265 |

## Top Feature Review

### 1. amount_to_prior_avg_ratio

This feature measures the current transaction amount relative to the customer's prior average transaction amount.

It is consistent with the Week 1 amount-deviation hypothesis: a transaction that is unusually large relative to a customer's own historical behavior may carry useful fraud signal.

This feature also had the largest absolute logistic-regression coefficient in v2, so both the linear and tree-based models found it useful.

### 2. prior_avg_amount

This feature represents the customer's historical spending baseline before the current transaction.

It provides context for interpreting the current amount because the same transaction amount can have different behavioral meaning for customers with different historical spending patterns.

It also had a relatively large coefficient in v2, providing agreement between the two model families.

### 3. amount_zscore_vs_prior

This feature measures how unusual the current amount is relative to both the customer's prior average and prior amount variability.

It strongly supports the amount-deviation hypothesis in v3.

Its v2 logistic-regression coefficient was very small, while its v3 tree importance is high. This divergence may indicate that the feature is more useful through nonlinear thresholds or interactions than through one global linear relationship.

### 4. seconds_since_prev_txn

This feature measures the time elapsed since the customer's previous transaction.

It supports the Week 1 velocity hypothesis because unusually short transaction gaps can represent abnormal transaction activity.

Other velocity features, including txn_count_1h_before and txn_count_24h_before, also received meaningful importance.

## Comparison With Hypotheses

### Amount deviation

Strongly supported.

The three highest-ranked v3 features are all related to the customer's historical amount behavior:

- amount_to_prior_avg_ratio
- prior_avg_amount
- amount_zscore_vs_prior

### Velocity

Supported.

seconds_since_prev_txn, txn_count_1h_before, and txn_count_24h_before all contribute to v3.

### Merchant/category novelty

Weakly supported by the current model.

is_new_merchant and is_new_category have relatively low v3 importance. They also had small coefficients in v2.

The evidence therefore suggests that the current novelty features are less informative than amount-deviation and velocity features for this dataset.

## Comparison With v2 Logistic Regression

There is strong agreement around amount_to_prior_avg_ratio and prior_avg_amount.

Both models also find transaction velocity useful.

A notable divergence is amount_zscore_vs_prior: it had a very small v2 coefficient but is the third-highest v3 feature importance. This is consistent with the possibility that the tree model can use the feature through nonlinear thresholds or interactions that a global linear coefficient does not represent directly.

Feature importance and logistic-regression coefficients are different quantities and should not be compared numerically.

## Leakage Review

No obvious new leakage warning was identified from the importance ranking.

The dominant features are behavioral features constructed from information available before the current transaction, following the Week 4 point-in-time feature-engineering rules.

Feature importance does not prove that leakage is absent, so the existing leakage tests and prediction-time boundary remain necessary.