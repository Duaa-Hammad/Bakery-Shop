import sqlite3


def connect_db():
    conn = sqlite3.connect("models/shop.db")
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
        description TEXT, 
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


def get_db():
    db = sqlite3.connect("models/shop.db")
    db.row_factory = sqlite3.Row  # <--returns rows as sqlite3.Row objects (which act like both tuples and dicts)
    return db


def add_user(data):
    db = get_db()
    cur = db.cursor()
    name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    gender = data.get("gender")
    city = data.get("city")
    admin_email = "duaa@gmail.com"
    role = "admin" if email == admin_email else "user"
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


def add_product(name, price, description, image_url, conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)",
        (name, price, description, image_url),
    )
    conn.commit()
    conn.close()


def get_all_products(conn):
    cursor = conn.cursor()
    products = cursor.execute("SELECT * FROM products").fetchall()
    conn.close()
    return products
