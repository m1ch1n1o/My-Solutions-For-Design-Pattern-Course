drop table if exists receipts;
drop table if exists receipt_products;
drop table if exists products;
drop table if exists units;
drop table if exists sales;


CREATE TABLE IF NOT EXISTS receipts
(
    id     TEXT PRIMARY KEY,
    status TEXT,
    total  REAL
);

CREATE TABLE IF NOT EXISTS sales
(
    n_receipts INTEGER,
    revenue    REAL
);

CREATE TABLE IF NOT EXISTS receipt_products
(
    receipt_id TEXT,
    product_id TEXT,
    quantity   INTEGER,
    price      REAL,
    total      REAL,
    FOREIGN KEY (receipt_id) REFERENCES receipts (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products
(
    id      TEXT PRIMARY KEY,
    unit_id TEXT,
    barcode TEXT UNIQUE,
    name    TEXT,
    price   REAL,
    FOREIGN KEY (unit_id) REFERENCES units (id)
);

CREATE TABLE IF NOT EXISTS units
(
    id   TEXT PRIMARY KEY,
    name TEXT UNIQUE
);