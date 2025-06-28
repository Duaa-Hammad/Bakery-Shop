import sqlite3

def get_db():
    db = sqlite3.connect("models/shop.db")
    db.row_factory = sqlite3.Row  # <--returns rows as sqlite3.Row objects (which act like both tuples and dicts)
    return db

def connect_db():
    conn = get_db()  # This function is defined in the same file, models/db_management.py
    
    # Think of the cursor as your "messenger" that communicates with the database.
    cursor = conn.cursor()
    # Table 1: users_info
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users_info 
        (id integer primary key autoincrement, 
        name TEXT, 
        email TEXT UNIQUE, 
        password TEXT, 
        gender TEXT, 
        city TEXT,
        role TEXT DEFAULT 'user')"""
    )

    # Table 2: products
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        price REAL, 
        image_url TEXT
    )"""
    )

    # Table 3: cart
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (user_id) REFERENCES users_info(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )"""
    )
    conn.commit()  # Save the changes
    return conn

def add_user(data):
    db = get_db()
    cur = db.cursor()
    name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    gender = data.get("gender")
    city = data.get("city")
    role = data.get("role")
    user_data = [name, email, password, gender, city, role]
    cur.execute(
        "INSERT INTO users_info (name, email, password, gender, city, role) VALUES (?, ?, ?, ?, ?, ?)",
        user_data,
    )
    db.commit()
    db.close()


def get_user_by_email(email):
    db = get_db()
    cur = db.cursor()
    user = cur.execute("SELECT * FROM users_info WHERE email = ?", (email,)).fetchone()
    db.close()
    return user

def get_all_users():
    db = get_db()
    cur = db.cursor()
    users = cur.execute("SELECT * FROM users_info").fetchall()
    db.close()
    return users

def delete_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users_info WHERE id = ?", (user_id,))
    db.commit()
    db.close()
# --------------------------------------------------------------------------------------

def add_product(data):
    db = get_db()
    cur = db.cursor()
    name = data.get("name")
    price = data.get("price")
    image_url = data.get("image")
    cur.execute(
        "INSERT INTO products (name, price, image_url) VALUES (?, ?, ?)",
        (name, price, image_url),
    )
    db.commit()
    db.close()

def delete_product(product_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    db.close()

def get_product_by_id(product_id):
    db = get_db()
    cur = db.cursor()
    product = cur.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    db.close()
    return product

def get_all_products():
    db = get_db()
    cur = db.cursor()
    products = cur.execute("SELECT * FROM products").fetchall()
    db.close()
    return products
# ------------------------------------------------------------------------
def add_to_cart(product_id, user_id):
    db = get_db()
    cur = db.cursor()
    quantity = 1  # Default quantity for simplicity
    cur.execute(
        "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (user_id, product_id, quantity),
    )
    db.commit()
    db.close()
    
    
def get_cart_items(user_id):
    db = get_db()
    cur = db.cursor()
    cart_items = cur.execute(
        """SELECT c.id, p.name, p.price, c.quantity, p.image_url
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = ?""",
        (user_id,)
    ).fetchall()
    db.close()
    return cart_items

def delete_cart_item(cart_item_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM cart WHERE id = ?", (cart_item_id,))
    db.commit()
    db.close()

