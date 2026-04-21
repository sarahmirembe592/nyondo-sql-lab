import sqlite3

conn = sqlite3.connect('nyondo_stock.db')

def search_product_safe(name):
    # SAFE: Using ? placeholder - SQL and data are separate
    query = "SELECT * FROM products WHERE name LIKE ?"
    param = f'%{name}%'
    print(f"\n[QUERY] {query}")
    print(f"[PARAMETER] '{param}'")
    rows = conn.execute(query, (param,)).fetchall()
    print(f"[RESULT] Found {len(rows)} products")
    for row in rows:
        print(f"  - ID:{row[0]} | {row[1]} | UGX {row[3]:,.0f}")
    return rows

def login_safe(username, password):
    # SAFE: Using ? placeholders
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"\n[QUERY] {query}")
    print(f"[PARAMETERS] username='{username}', password='{password}'")
    row = conn.execute(query, (username, password)).fetchone()
    if row:
        print(f"[RESULT] LOGIN SUCCESS: {row[1]} (Role: {row[3]})")
    else:
        print("[RESULT] LOGIN FAILED")
    return row

print("\n" + "="*70)
print("TESTING SECURE FUNCTIONS - ALL ATTACKS SHOULD FAIL")
print("="*70)

print("\n--- Test 1: OR 1=1 attack on search ---")
result = search_product_safe("' OR 1=1--")
print(f"Returned {len(result)} products (should be 0 - safe)")

print("\n--- Test 2: UNION attack on search ---")
result = search_product_safe("' UNION SELECT id,username,password,role FROM users--")
print(f"Returned {len(result)} products (should be 0 - safe)")

print("\n--- Test 3: Login bypass with comment ---")
result = login_safe("admin'--", "anything")
print(f"Returned: {result} (should be None - safe)")

print("\n--- Test 4: Always true login ---")
result = login_safe("' OR '1'='1", "' OR '1'='1")
print(f"Returned: {result} (should be None - safe)")

print("\n" + "="*70)
print("VERIFY NORMAL FUNCTIONALITY STILL WORKS")
print("="*70)

print("\n--- Normal search: 'cement' ---")
search_product_safe("cement")

print("\n--- Normal login: correct credentials ---")
login_safe("admin", "admin123")

print("\n--- Normal login: wrong password ---")
login_safe("admin", "wrongpass")

conn.close()