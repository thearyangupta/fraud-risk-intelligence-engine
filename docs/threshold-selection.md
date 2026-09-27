# Decision Threshold Selection

## Scope

Decision thresholds were selected using the validation split only.

The held-out test split was not inspected or used during threshold selection.

The primary decision model is the previously selected v3 XGBoost model.

## Policy

The decision layer uses two thresholds:

- Review threshold: `0.50`
- Block threshold: `0.80`

The resulting policy is:

- `score < 0.50` → `ALLOW`
- `0.50 <= score < 0.80` → `REVIEW`
- `score >= 0.80` → `BLOCK`

## Block Threshold

A validation sweep showed the expected trade-off between fraud coverage and
false positives.

Selected points included:

| Threshold | Precision | Recall | Fraud Caught | Fraud Missed | Legitimate Flagged |
|---|---:|---:|---:|---:|---:|
| 0.70 | 0.0847 | 0.8938 | 1,119 | 133 | 12,087 |
| 0.75 | 0.0956 | 0.8754 | 1,096 | 156 | 10,373 |
| 0.80 | 0.1112 | 0.8554 | 1,071 | 181 | 8,561 |
| 0.85 | 0.1310 | 0.8227 | 1,030 | 222 | 6,830 |
| 0.90 | 0.1953 | 0.7604 | 952 | 300 | 3,922 |

`0.80` was selected as the block threshold.

Raising the threshold from 0.80 to 0.90 would avoid 4,639 legitimate block
flags but would miss an additional 119 fraud transactions.

Lowering it from 0.80 to 0.70 would catch 48 additional fraud transactions but
would add 3,526 legitimate block flags.

Given the project assumption that missed fraud is more costly than a false
positive, while automatic blocking should still remain selective, 0.80 was
chosen as a reasonable validation-based operating point.

## Review Threshold

With the block threshold fixed at 0.80, candidate review thresholds were
evaluated against the resulting review workload and fraud allowed through.

| Review Threshold | Review Count | Review Rate | Fraud Reviewed | Fraud Allowed |
|---|---:|---:|---:|---:|
| 0.30 | 31,933 | 16.42% | 138 | 43 |
| 0.40 | 21,014 | 10.80% | 115 | 66 |
| 0.50 | 13,088 | 6.73% | 94 | 87 |
| 0.60 | 7,636 | 3.93% | 72 | 109 |
| 0.70 | 3,574 | 1.84% | 48 | 133 |

`0.50` was selected as the review threshold.

Compared with 0.50, lowering the review threshold to 0.40 would require 7,926
additional reviews to move 21 additional fraud transactions out of ALLOW.

Raising it to 0.60 would save 5,452 reviews but allow 22 additional fraud
transactions through.

The selected threshold therefore represents a deliberate compromise between
fraud coverage and review workload.

## Validation Policy Result

With:

- review threshold = `0.50`
- block threshold = `0.80`

the validation population is divided as follows:

| Decision | Transactions | Rate | Fraud |
|---|---:|---:|---:|
| ALLOW | 171,781 | 88.32% | 87 |
| REVIEW | 13,088 | 6.73% | 94 |
| BLOCK | 9,632 | 4.95% | 1,071 |

Of 1,252 validation fraud transactions:

- 85.54% were assigned to BLOCK
- 7.51% were assigned to REVIEW
- 6.95% were assigned to ALLOW

Therefore 93.05% of validation fraud received either REVIEW or BLOCK.

## Threshold Lock

These thresholds are now frozen:

```text
REVIEW_THRESHOLD = 0.50
BLOCK_THRESHOLD = 0.80