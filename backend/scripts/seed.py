from app.database import get_connection
from app.utils.password import hash_password




conn = get_connection()
cur = conn.cursor()

# Categories
cur.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
)
""")

# Warehouses
cur.execute("""
CREATE TABLE IF NOT EXISTS warehouses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
)
""")

# Products
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    reorder_level INTEGER NOT NULL DEFAULT 10
)
""")

# Users
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

# Stock Movements
cur.execute("""
CREATE TABLE IF NOT EXISTS stock_movements (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    warehouse_id INTEGER REFERENCES warehouses(id),
    movement_type VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Seed category
cur.execute("""
INSERT INTO categories(name)
VALUES ('Electronics')
ON CONFLICT (name) DO NOTHING
""")

# Seed warehouse
cur.execute("""
INSERT INTO warehouses(name)
VALUES ('Main Warehouse')
ON CONFLICT (name) DO NOTHING
""")

# Seed product
cur.execute("""
INSERT INTO products(
    sku,
    name,
    category_id,
    reorder_level
)
SELECT
    'LAP001',
    'Laptop',
    1,
    20
WHERE NOT EXISTS (
    SELECT 1
    FROM products
    WHERE sku='LAP001'
)
""")

# Seed user with bcrypt hash
hashed_password = hash_password("TestPass123!")

cur.execute("""
INSERT INTO users(
    username,
    password_hash
)
SELECT
    %s,
    %s
WHERE NOT EXISTS (
    SELECT 1
    FROM users
    WHERE username=%s
)
""", (
    "testuser",
    hashed_password,
    "testuser"
))

conn.commit()

cur.close()
conn.close()

print("Database seeded successfully.")