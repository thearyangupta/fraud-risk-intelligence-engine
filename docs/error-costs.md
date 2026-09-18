# Fraud Classification Error Costs

## Context

The v1 rule-based baseline is evaluated on the validation split.

Its confusion matrix is:

- True positives: 518
- False positives: 3,299
- True negatives: 189,950
- False negatives: 734

These errors do not have equal business consequences.

## False Positive Cost

A false positive occurs when a legitimate transaction is flagged as fraud.

If a fraud flag leads to intervention, possible costs include:

- customer friction
- unnecessary review or support work
- delayed or blocked legitimate purchases
- potential loss of customer trust or revenue

False positives therefore have both operational and customer-experience costs.

## False Negative Cost

A false negative occurs when a fraudulent transaction is not flagged.

Possible costs include:

- direct fraud loss
- investigation and recovery costs
- downstream operational impact
- customer or business harm associated with undetected fraud

For this project, false negatives are assumed to have a higher direct per-event cost than false positives because undetected fraud can produce direct financial loss.

However, false positives cannot be ignored because a large number of legitimate interventions can create substantial aggregate cost.

## Working Cost Assumption

As a starting modelling assumption, one false negative will be treated as several times more costly than one false positive.

This is a modelling assumption rather than a measured business cost. A production system should replace it with organization-specific estimates based on fraud losses, review costs, customer friction, and intervention outcomes.

## Threshold Implication

The unequal cost of false positives and false negatives means that model selection cannot rely on accuracy alone.

Later decision thresholds should consider the trade-off between:

- catching more fraud
- avoiding unnecessary intervention on legitimate transactions

This cost asymmetry will inform the later allow / review / block decision policy.