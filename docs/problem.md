# Problem Definition

## What Counts as Fraud?
Fraud is a transaction identified by the dataset's ground-truth fraud label as fraudulent.

The exact operational meaning of the fraud label will be finalized after the dataset is selected and its documentation is reviewed. Depending on the dataset, the label may represent a confirmed fraudulent transaction, chargeback, or another documented fraud outcome.
## Target Variable

The target is whether a transaction is fraudulent or legitimate.

This is intended to be a binary classification problem:

- Positive class: fraud
- Negative class: legitimate transaction

The exact target column name, encoding, and meaning of the positive label will be documented after the dataset is selected.

## Information Available at Prediction Time

Only information that exists when the transaction arrives may be used for prediction.

Potential prediction-time information includes:

- transaction amount
- transaction timestamp
- customer or account identifier
- merchant information
- device information, if available
- location information, if available
- historical information from transactions that occurred before the current transaction

The exact list will be finalized after the dataset is selected and its columns are inspected.

## Information NOT Available at Prediction Time

Information that becomes known only after the transaction must not be used as a prediction feature.

Examples include:

- the fraud label itself
- chargeback information determined after the transaction
- investigation results
- future transactions
- any other information generated after the prediction point

Using such information would cause data leakage.

## Cost of Prediction Errors

### False Positive

A false positive occurs when a legitimate transaction is predicted as fraudulent.

Possible costs include blocking or delaying a legitimate payment, frustrating the customer, creating unnecessary manual review work, and potentially losing a legitimate transaction.

### False Negative

A false negative occurs when a fraudulent transaction is predicted as legitimate.

Possible costs include allowing fraud to succeed, financial loss, chargebacks, and investigation or operational costs.

The costs of false positives and false negatives are not equal. The eventual decision threshold must consider the trade-off between catching fraud and disrupting legitimate customers.

## Point-in-Time Rule

**Features may only use information available strictly before the transaction timestamp.**