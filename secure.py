import sqlite3


conn = sqlite3.connect('nyondo_stock.db')

def validate_name(name):
    """Name must be string, at least 2 chars, no < > or ;"""
    if not isinstance(name, str):
        return False, "Name must be a string"
    if len(name) < 2:
        return False, "Name must be at least 2 characters"
    if '<' in name or '>' in name or ';' in name:
        return False, "Name cannot contain < > or ; characters"
    return True, ""

def validate_price(price):
    """Price must be positive number"""
    try:
        price_num = float(price)
        if price_num <= 0:
            return False, "Price must be greater than 0"
        return True, ""
    except (TypeError, ValueError):
        return False, "Price must be a number"

def validate_username(username):
    """Username: string, no spaces, not empty"""
    if not isinstance(username, str):
        return False, "Username must be a string"
    if len(username) == 0:
        return False, "Username cannot be empty"
    if ' ' in username:
        return False, "Username cannot contain spaces"
    return True, ""

def validate_password(password):
    """Password: string, at least 6 characters"""
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def search_product_safe(name):
    # INPUT VALIDATION
    is_valid, error = validate_name(name)
    if not is_valid:
        print(f"\n[VALIDATION ERROR] {error}")
        return []
    
    # PARAMETERISED QUERY
    query = "SELECT * FROM products WHERE name LIKE ?"
    param = f'%{name}%'
    print(f"\n[QUERY] {query} with parameter: '{param}'")
    rows = conn.execute(query, (param,)).fetchall()
    print(f"[RESULT] Found {len(rows)} products")
    return rows

def login_safe(username, password):
    # INPUT VALIDATION
    is_valid_user, user_error = validate_username(username)
    if not is_valid_user:
        print(f"\n[VALIDATION ERROR] {user_error}")
        return None
    
    is_valid_pass, pass_error = validate_password(password)
    if not is_valid_pass:
        print(f"\n[VALIDATION ERROR] {pass_error}")
        return None
    
    # PARAMETERISED QUERY
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"\n[QUERY] {query} with parameters: '{username}', '{password}'")
    row = conn.execute(query, (username, password)).fetchone()
    if row:
        print(f"[RESULT] LOGIN SUCCESS: {row[1]} (Role: {row[3]})")
    else:
        print("[RESULT] LOGIN FAILED")
    return row

def add_product_safe(name, description, price):
    """Bonus: Add new product with validation"""
    is_valid_name, name_error = validate_name(name)
    if not is_valid_name:
        print(f"[VALIDATION ERROR] {name_error}")
        return None
    
    is_valid_price, price_error = validate_price(price)
    if not is_valid_price:
        print(f"[VALIDATION ERROR] {price_error}")
        return None
    
    query = "INSERT INTO products (name, description, price) VALUES (?, ?, ?)"
    cursor = conn.execute(query, (name, description, float(price)))
    conn.commit()
    print(f"[SUCCESS] Added product: {name} at UGX {price:,}")
    return cursor.lastrowid

print("\n" + "=" * 70)
print("TASK 5 - INPUT VALIDATION TESTS")
print("=" * 70)

print("\n--- Test 1: search_product_safe('cement') - SHOULD WORK ---")
search_product_safe('cement')

print("\n--- Test 2: search_product_safe('') - SHOULD BE REJECTED ---")
search_product_safe('')

print("\n--- Test 3: search_product_safe('<script>') - SHOULD BE REJECTED ---")
search_product_safe('<script>')

print("\n--- Test 4: login_safe('admin', 'admin123') - SHOULD WORK ---")
login_safe('admin', 'admin123')

print("\n--- Test 5: login_safe('admin', 'ab') - SHOULD BE REJECTED (too short) ---")
login_safe('admin', 'ab')

print("\n--- Test 6: login_safe('ad min', 'pass123') - SHOULD BE REJECTED (space) ---")
login_safe('ad min', 'pass123')

print("\n" + "=" * 70)
print("BONUS: Attack tests on secure+validated functions")
print("=" * 70)

print("\n--- Attack test: OR 1=1 ---")
search_product_safe("' OR 1=1--")

print("\n--- Attack test: UNION ---")
search_product_safe("' UNION SELECT id,username,password,role FROM users--")

print("\n--- Attack test: Login bypass ---")
login_safe("admin'--", "anything")

print("\n--- Attack test: Always true ---")
login_safe("' OR '1'='1", "' OR '1'='1")

conn.close()