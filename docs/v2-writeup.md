### Logistic Regression v2

## Objective

this v2 introduced the first learned machine-learning baseline for the fraud-risk engine.

The goal was to understand logistic regression mechanics before using the library implementation, handle the severe class imbalance explicitly, evaluate the model on the untouched validation split, and compare it with the Week 5 rule baseline.

The temporal test split remained untouched.

## Logistic Regression Mechanics

Logistic regression follows the chain:

features → linear score → sigmoid → probability → decision threshold

The model learns a weighted linear score from the input features. The sigmoid converts that score into a value between 0 and 1, and a separate decision threshold converts the probability into a binary prediction.

The threshold is therefore a decision layer rather than part of the learned logistic-regression coefficients.

## Class-Imbalance Handling

Two imbalance strategies were tested:

1. balanced class weighting
2. random oversampling of the minority fraud class

Random oversampling was performed on the training split only. Validation and test data were not resampled.

The two approaches produced nearly identical validation probability distributions in the experiment.

The class-weighted approach was selected for v2 because it achieved similar observed probability behavior without duplicating minority observations or nearly doubling the effective training dataset.

This selection is an engineering choice based on the current experiment, not a claim that class weighting universally outperforms oversampling.

## Validation Results

| Metric | v1 Rule Baseline | v2 Logistic Regression |
|---|---:|---:|
| Precision | 0.1357 | 0.0406 |
| Recall | 0.4137 | 0.8786 |
| F1 | 0.2044 | 0.0776 |
| ROC-AUC | — | 0.9161 |
| PR-AUC / Average Precision | — | 0.1611 |

At the default 0.5 threshold, v2 substantially increased recall but reduced precision and F1 relative to v1.

Therefore v2 does not uniformly outperform the rule baseline. It represents a different operating trade-off: substantially more fraud is detected, but many more legitimate transactions are also flagged.

The high ROC-AUC alongside much weaker threshold-level precision/F1 also demonstrates why ranking quality and the final operating threshold must be considered separately.

For this highly imbalanced fraud problem, PR-based evaluation remains especially important.

## Learned Coefficients

The largest positive standardized coefficient was `amount_to_prior_avg_ratio`, supporting the hypothesis that unusually large transactions relative to a customer's previous behavior can carry useful fraud signal.

`txn_count_1h_before` also received a positive coefficient, providing support for the transaction-velocity hypothesis.

The learned coefficients for `is_new_merchant` and `is_new_category` were small and slightly negative. This does not imply that novelty prevents fraud. It means that, conditional on the other features in this fitted linear model, these features contributed little positive linear signal.

Coefficient direction and magnitude describe the fitted model and should not be interpreted as causal effects.

## Next Lever

The next lever to investigate is decision-threshold tuning.

The current evaluation uses the default threshold of 0.5. Because v2 achieves high recall but low precision at this operating point, a later threshold study can examine whether another operating point provides a more useful precision-recall trade-off.

No threshold tuning was performed during Week 6.

## Leakage and Evaluation Discipline

Feature construction remained point-in-time safe.

Training-only operations, including scaling and imbalance handling, were fitted using training data.

Model comparison used the validation split.

The temporal test split remained untouched during Week 6.