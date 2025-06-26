import sqlite3

def connect_db():
    conn = sqlite3.connect("models/shop.db")
    # Think of the cursor as your "messenger" that communicates with the database.
    cursor = conn.cursor()
    # Table 1: users_info
    cursor.execute('''CREATE TABLE IF NOT EXISTS users_info 
        (id integer primary key autoincrement, 
        name TEXT, 
        email TEXT, 
        password TEXT, 
        gender TEXT, 
        city TEXT,
        role TEXT DEFAULT 'user')''')
    
    # Table 2: products
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        price REAL, 
        description TEXT, 
        image_url TEXT
    )''')

    # Table 3: cart
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (user_id) REFERENCES users_info(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )''')
    conn.commit()  # Save the changes
    return conn

def get_db_connection():
    conn = connect_db()
    return conn

    
def add_user(name, email, password, gender, city):
    conn = connect_db()
    cursor = conn.cursor()

    admin_email = "doaahammad211@gmail.com"

    role = "admin" if email == admin_email else "user"

    cursor.execute('''
        INSERT INTO users_info (name, email, password, gender, city, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, password, gender, city, role))

    conn.commit()
    conn.close()
    
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users_info WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def add_product(name, price, description, image_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)', (name, price, description, image_url))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    products = cursor.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products