import sqlite3

conn = sqlite3.connect('nyondo_stock.db')
cursor = conn.cursor()

# Create products table
cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
)
''')

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'attendant'
)
''')

# Insert products (no OR IGNORE - table is fresh)
products = [
    ('Cement (bag)', 'Portland cement 50kg bag', 35000),
    ('Iron Sheet 3m', 'Gauge 30 roofing sheet 3m long', 110000),
    ('Paint 5L', 'Exterior wall paint white 5L', 60000),
    ('Nails 1kg', 'Common wire nails 1kg pack', 12000),
    ('Timber 2x4', 'Pine timber plank 2x4 per metre', 25000)
]

cursor.executemany('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', products)

# Insert users
users = [
    ('admin', 'admin123', 'admin'),
    ('fatuma', 'pass456', 'attendant'),
    ('wasswa', 'pass789', 'manager')
]

cursor.executemany('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', users)

conn.commit()

print("\n=== ALL PRODUCTS IN DATABASE ===")
rows = cursor.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(f"ID: {row[0]} | Name: {row[1]} | Price: UGX {row[3]:,.0f}")

print("\n=== ALL USERS ===")
users = cursor.execute('SELECT * FROM users').fetchall()
for user in users:
    print(f"ID: {user[0]} | Username: {user[1]} | Password: {user[2]} | Role: {user[3]}")

conn.close()