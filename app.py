from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort
from datetime import timedelta
import os
from werkzeug.utils import secure_filename

from models import db_management

app = Flask(__name__)
app.secret_key = "supersecret"

app.permanent_session_lifetime = timedelta(days=5)

# Initialize database when app starts
db_management.connect_db()


@app.route("/")
def index():
    products = db_management.get_all_products()
    if "username" in session:
        role = session.get("role")
        username = session.get("username")
        email = session.get("email")
        user = db_management.get_user_by_email(email)
        cart_items = db_management.get_cart_items(user["id"])
        return render_template(
            "index.html", sentence=username, role=role, products=products, cart_items=cart_items)
    else:
        return render_template("index.html", sentence="Sign Up Now", username=None, products=products)
    
# ---------------------------------------------------------------------------

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        session["email"] = request.form["email"]
        db_management.add_user(request.form)
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # set the session to permanent, so it lasts for 5 days
        session.permanent = True
        email = request.form["email"]
        password = request.form["password"]
        user = db_management.get_user_by_email(email)
        if user and user["password"] == password:
            session["username"] = user["name"]
            session["password"] = user["password"]
            session["role"] = user["role"]
            session["email"] = user["email"]
            return redirect(url_for("index"))
        # return redirect(url_for("login", error="Invalid credentials"))
        return abort(401, "Invalid credentials")


@app.route("/logout")
def logout():
    # remove the username and password from the session
    session.pop("username", None)
    session.pop("password", None)
    session.pop("email", None)
    session.pop("role", None)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        products = db_management.get_all_products()
        return render_template("dashboard_pages/dashboard.html", sentence=username, products=products)
    else:
        return redirect(url_for("login"))

# -----------------------------------------------------------------------------
# User management routes
# -----------------------------------------------------------------------------
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    username = session["username"]
    if request.method == "POST":
        db_management.add_user(request.form)
        # Optionally, flash a message or redirect to the dashboard or add_user page
        return redirect(url_for("dashboard"))

    return render_template("dashboard_pages/add_user.html", sentence=username)

@app.route("/view_all_users")
def view_all_users():
        username = session["username"]
        users = db_management.get_all_users()
        return render_template("dashboard_pages/view_all_users.html", users=users, sentence=username)
    
@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db_management.delete_user(user_id)
    return redirect(url_for("view_all_users"))
# -----------------------------------------------------------------------------
# Product management routes
# -----------------------------------------------------------------------------
@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        image_file = request.files.get("image")
# ----------------------------------------------------------------
        # Handle image upload
        # Check if an image file was uploaded
        image_url = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename) #Sanitize the file name
            image_folder = os.path.join("static", "user_images") #Path where images will be saved
            os.makedirs(image_folder, exist_ok=True) #If the folder does not exists, Create one
            image_path = os.path.join(image_folder, filename) #Set the full path
            image_file.save(image_path) #Save the image on the server
            image_url = f"user_images/{filename}" #Set the image path that will be saved in the DB
# ----------------------------------------------------------------

        # Cannot modify request.form directly because it is immutable
        # Create a new dict to pass to add_product
        product_data = {"name": name, "price": price, "image": image_url}
        db_management.add_product(product_data)
        return redirect(url_for("dashboard"))
    else:
        if "username" in session:
            username = session["username"]
            return render_template(
                "dashboard_pages/add_product.html", sentence=username)
        else:
            return redirect(url_for("login"))


@app.route("/view_all_products")
def view_all_products():
    username = session["username"]
    products = db_management.get_all_products()
    return render_template("dashboard_pages/dashboard.html", products=products, sentence=username)

    
@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    db_management.delete_product(product_id)
    return redirect(url_for("view_all_products"))

# -----------------------------------------------------------------------------
# Cart management routes
# -----------------------------------------------------------------------------
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "email" not in session:
        return jsonify({"error": "not logged in"}), 401
    user = db_management.get_user_by_email(session["email"])
    if user is None:
        return jsonify({"error": "not logged in"}), 401
    user_id = user["id"]
    db_management.add_to_cart(product_id, user_id)
    cart_items = db_management.get_cart_items(user_id)
    cart_html = render_template("_cart_items.html", cart_items=cart_items)
    return jsonify({"cart_html": cart_html})

@app.route("/delete_cart_item/<int:cart_item_id>", methods=["POST"])
def delete_cart_item(cart_item_id):
    if "email" not in session:
        return jsonify({"error": "not logged in"}), 401
    user = db_management.get_user_by_email(session["email"])
    if user is None:
        return jsonify({"error": "not logged in"}), 401
    user_id = user["id"]
    db_management.delete_cart_item(cart_item_id)
    cart_items = db_management.get_cart_items(user_id)
    cart_html = render_template("_cart_items.html", cart_items=cart_items)
    return jsonify({"cart_html": cart_html})

if __name__ == "__main__":
    app.run(debug=True)
