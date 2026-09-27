# Final Held-Out Test Evaluation

## Evaluation Protocol

The fraud-risk model and decision policy were frozen before the held-out test
set was opened.

Final configuration:

- Primary model: v3 XGBoost
- Review threshold: `0.50`
- Block threshold: `0.80`

The thresholds were selected using validation data only.

The held-out test set was evaluated once and was not used for model selection,
threshold selection, or further tuning.

## Final Test Metrics

The held-out test set contained:

- 194,502 transactions
- 1,133 fraud transactions

Binary intervention performance at the review threshold (`score >= 0.50`):

| Metric | Test |
|---|---:|
| Precision | 0.0449 |
| Recall | 0.9417 |
| F1 | 0.0857 |
| ROC-AUC | 0.9731 |
| PR-AUC / AP | 0.4835 |

## Validation vs Test

| Metric | Validation | Test |
|---|---:|---:|
| Precision | 0.0513 | 0.0449 |
| Recall | 0.9305 | 0.9417 |
| F1 | 0.0972 | 0.0857 |
| ROC-AUC | 0.9721 | 0.9731 |
| PR-AUC / AP | 0.5173 | 0.4835 |

The held-out period did not show a major ranking-performance collapse.

ROC-AUC remained approximately stable, while recall increased slightly.
PR-AUC decreased from 0.5173 to 0.4835, showing some degradation in
precision-recall performance on unseen future data.

No model or threshold changes were made in response to these results.

## Decision Distribution

The frozen policy produced:

| Decision | Transactions | Rate | Fraud | Fraud Share |
|---|---:|---:|---:|---:|
| ALLOW | 170,736 | 87.78% | 66 | 5.83% |
| REVIEW | 14,067 | 7.23% | 80 | 7.06% |
| BLOCK | 9,699 | 4.99% | 987 | 87.11% |

Total:

- Transactions: 194,502
- Fraud: 1,133

Fraud receiving intervention:

- REVIEW + BLOCK = 1,067
- Intervention recall = 94.17%

Fraud allowed:

- 66
- 5.83% of test fraud

## Operational Interpretation

The final policy routes approximately:

- 87.78% of transactions directly to ALLOW
- 7.23% to REVIEW
- 4.99% to BLOCK

Most fraud was concentrated in the BLOCK region:

- 87.11% of all test fraud was blocked
- another 7.06% was routed to review

Overall, 94.17% of held-out fraud received either REVIEW or BLOCK.

The policy therefore maintained high fraud coverage on the unseen temporal
test period while keeping the review queue substantially smaller than the
overall transaction population.

## Limitations

The selected thresholds are not claimed to be universally optimal.

They were chosen using validation performance and a simplified project
assumption that false negatives are more costly than false positives.

A production system would additionally consider:

- monetary fraud loss
- false-block customer impact
- manual-review capacity and cost
- transaction value
- probability calibration
- fraud prevalence changes
- model and feature drift
- segment-specific risk
- delayed fraud labels

The current evaluation demonstrates the offline behavior of the frozen
decision policy, not production profitability.

## Final Result

The project followed the intended evaluation discipline:

1. Train models on the training period.
2. Select the model using validation data.
3. Select review and block thresholds using validation data.
4. Freeze the model and decision policy.
5. Open the held-out temporal test set once.
6. Report the resulting performance without retuning.

Final frozen configuration:

```text
MODEL = v3 XGBoost
REVIEW_THRESHOLD = 0.50
BLOCK_THRESHOLD = 0.80