# Dataset Options

The candidate datasets are evaluated against the selection criteria defined for this project. Scores are intentionally limited to **Yes / Partial / No**. No dataset is selected at this stage.

| Criterion | IEEE-CIS Fraud Detection | PaySim | Sparkov-style Credit Card Transactions |
|---|---|---|---|
| Timestamps / time ordering | Yes | Yes | Yes |
| Customer / account identity | Partial | Yes | Yes |
| Transaction amount | Yes | Yes | Yes |
| Merchant information | Partial | Partial | Yes |
| Device / location | Yes | No | Partial |
| Fraud labels | Yes | Yes | Yes |
| Manageable size | Partial | Yes | Yes |
| Usable license | Partial | Yes | Yes |

## Notes

### IEEE-CIS Fraud Detection

- Provides chronological information through `TransactionDT`, although it is elapsed time from an unspecified reference point rather than a real timestamp.
- Contains transaction amount and a binary `isFraud` target.
- Provides card, address, device, and identity-related information, but many fields are masked and there is no simple clean customer ID.
- Identity information is not available for every transaction.
- The dataset is relatively complex, with hundreds of columns and multiple files.
- Distribution is governed by the Kaggle competition rules.

### PaySim

- Provides chronological ordering through `step`, where one step represents one hour.
- `nameOrig` provides customer identity and `amount` provides the transaction value.
- `nameDest` provides recipient information, including merchant-like destinations, but rich merchant categories are unavailable.
- Device and geographic information are unavailable.
- `isFraud` provides the fraud target.
- The data is synthetic, so fraud patterns may be cleaner and less representative of real production behaviour.
- The dataset documentation warns against using post-transaction balance fields for fraud detection because fraudulent transactions are cancelled.

### Sparkov-style Credit Card Transactions

- Provides transaction timestamps and anonymized card/account identity.
- Contains transaction amount, merchant name, merchant category, and geographic information.
- Provides the binary `is_fraud` target.
- Geographic information is available, but device identity is not.
- The data is synthetic, which must be treated as a limitation if selected.