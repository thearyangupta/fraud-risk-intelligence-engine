-- These queries demonstrate LAG and ROW_NUMBER.

-- 1. Previous transaction amount and timestamp for each customer.
SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,
    split,

    LAG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_amount,

    LAG(timestamp) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_timestamp

FROM transactions
ORDER BY customer_id, timestamp;


-- 2. Chronological transaction sequence for each customer.
SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,
    split,

    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS transaction_sequence

FROM transactions
ORDER BY customer_id, timestamp;


-- 3. Combined Day 3 window query.
SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,
    split,

    LAG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_amount,

    LAG(timestamp) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS previous_timestamp,

    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
    ) AS transaction_sequence

FROM transactions
ORDER BY customer_id, timestamp;

-- Rolling aggregate practice.
--
-- The frame ends at 1 PRECEDING so the current transaction
-- is excluded from its own historical calculation.


-- 4. Average amount over the previous 3 transactions.
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


-- 5. Count of the previous 3 transactions.
SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,

    COUNT(*) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ) AS previous_3_transaction_count

FROM transactions
ORDER BY customer_id, timestamp;


-- 6. Combined rolling-window query.
SELECT
    transaction_id,
    customer_id,
    timestamp,
    amount,

    AVG(amount) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ) AS previous_3_avg_amount,

    COUNT(*) OVER (
        PARTITION BY customer_id
        ORDER BY timestamp
        ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
    ) AS previous_3_transaction_count

FROM transactions
ORDER BY customer_id, timestamp;