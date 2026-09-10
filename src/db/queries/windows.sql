-- Verified temporal SQL queries.


-- ============================================================
-- Signal 1: Previous transaction amount
-- Fraud signal: compare the current amount with the customer's
-- immediately previous transaction.
-- ============================================================

SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,

    LAG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_amount

FROM transactions
ORDER BY customer_id, timestamp;



-- ============================================================
-- Signal 2: Previous transaction timestamp
-- Fraud signal: supports calculating time since the customer's
-- previous transaction.
-- ============================================================

SELECT
    transaction_id,
    customer_id,
    timestamp,

    LAG(timestamp) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_timestamp

FROM transactions
ORDER BY customer_id, timestamp;



-- ============================================================
-- Signal 3: Transaction sequence number
-- Fraud signal: identifies whether this is the customer's first
-- observed transaction or a later transaction.
-- ============================================================

SELECT
    transaction_id,
    customer_id,
    timestamp,

    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS transaction_sequence

FROM transactions
ORDER BY customer_id, timestamp;



-- ============================================================
-- Signal 4: Rolling historical average amount
-- Fraud signal: compare the current amount against the customer's
-- previous three transactions.
--
-- Important:
-- The frame ends at 1 PRECEDING so the current transaction
-- is excluded from its own historical average.
-- ============================================================

SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,

    AVG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ) AS previous_3_avg_amount

FROM transactions
ORDER BY customer_id, timestamp;



-- ============================================================
-- Signal 5: Recent transaction count
-- Fraud signal: measures how many transactions exist in the
-- previous three observed transactions.
--
-- This is a fixed-row window, not a time-based window.
-- ============================================================

SELECT
    transaction_id,
    customer_id,
    timestamp,

    COUNT(*) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ) AS previous_3_transaction_count

FROM transactions
ORDER BY customer_id, timestamp;