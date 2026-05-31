ALTER TABLE orders ADD COLUMN payment_status TEXT NOT NULL DEFAULT 'unpaid';
ALTER TABLE orders ADD COLUMN payment_provider TEXT;
ALTER TABLE orders ADD COLUMN payment_reference TEXT;

CREATE INDEX IF NOT EXISTS idx_orders_payment_status
    ON orders(payment_status);
