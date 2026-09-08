CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    city_population BIGINT,
    job TEXT,
    date_of_birth DATE
);


CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    merchant TEXT NOT NULL,
    category TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    merchant_latitude DOUBLE PRECISION,
    merchant_longitude DOUBLE PRECISION,
    fraud_label SMALLINT NOT NULL CHECK (fraud_label IN (0, 1)),
    split TEXT NOT NULL CHECK (split IN ('train', 'val', 'test')),

    CONSTRAINT fk_transactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


CREATE INDEX IF NOT EXISTS idx_transactions_customer_timestamp
    ON transactions (customer_id, timestamp);