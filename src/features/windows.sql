-- Point-in-time window boundary.
--
-- Rule:
-- Historical feature windows must end at 1 PRECEDING.
-- The current transaction must never be included in its own
-- historical feature calculation.
--
-- First-ever transaction rule:
-- prior_avg_amount = NULL
-- is_first_transaction = TRUE


SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,

    AVG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
    ) AS prior_avg_amount,

    CASE
        WHEN ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY timestamp
        ) = 1
        THEN TRUE
        ELSE FALSE
    END AS is_first_transaction

FROM transactions
ORDER BY customer_id, timestamp;