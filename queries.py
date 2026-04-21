import sqlite3

conn = sqlite3.connect('nyondo_stock.db')
cursor = conn.cursor()

print("=" * 60)
print("TASK 2 - DATABASE QUERIES")
print("=" * 60)

# Query A - All columns of every product
print("\n--- QUERY A: All products (all columns) ---")
rows = cursor.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(f"ID:{row[0]} | {row[1]} | {row[2]} | UGX {row[3]:,}")

# Query B - Only name and price
print("\n--- QUERY B: Name and price only ---")
rows = cursor.execute('SELECT name, price FROM products').fetchall()
for row in rows:
    print(f"{row[0]} - UGX {row[1]:,}")

# Query C - Product with id = 3
print("\n--- QUERY C: Product with id = 3 ---")
row = cursor.execute('SELECT * FROM products WHERE id = 3').fetchone()
print(f"ID: {row[0]} | {row[1]} | {row[2]} | UGX {row[3]:,}")

# Query D - Products containing 'sheet' (case insensitive)
print("\n--- QUERY D: Products containing 'sheet' ---")
rows = cursor.execute("SELECT * FROM products WHERE name LIKE '%sheet%'").fetchall()
for row in rows:
    print(f"{row[1]} - UGX {row[3]:,}")

# Query E - Sorted by price highest first
print("\n--- QUERY E: Sorted by price (highest first) ---")
rows = cursor.execute('SELECT name, price FROM products ORDER BY price DESC').fetchall()
for row in rows:
    print(f"{row[0]} - UGX {row[1]:,}")

# Query F - 2 most expensive products
print("\n--- QUERY F: Top 2 most expensive ---")
rows = cursor.execute('SELECT name, price FROM products ORDER BY price DESC LIMIT 2').fetchall()
for row in rows:
    print(f"{row[0]} - UGX {row[1]:,}")

# Query G - Update Cement price to 38,000
print("\n--- QUERY G: Update Cement price to UGX 38,000 ---")
cursor.execute('UPDATE products SET price = 38000 WHERE id = 1')
conn.commit()

print("After update:")
rows = cursor.execute('SELECT * FROM products').fetchall()
for row in rows:
    print(f"ID:{row[0]} | {row[1]} | UGX {row[3]:,}")

conn.close()