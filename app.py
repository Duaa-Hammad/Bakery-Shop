from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
from models import db_management

app = Flask(__name__)
app.secret_key = "supersecret"

app.permanent_session_lifetime = timedelta(days=5)

# Initialize database when app starts
db_management.connect_db()


@app.route("/")
def index():
    if "username" in session:
        role = session.get("role")
        username = session.get("username")
        return render_template("index.html", sentence=username, role=role)
    else:
        return render_template("index.html", sentence="Sign Up Now", username=None)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
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
            return redirect(url_for("index"))
        return redirect(url_for("login", error="Invalid credentials"))


@app.route("/logout")
def logout():
    # remove the username and password from the session
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard_pages/dashboard.html", sentence=username)
    else:
        return redirect(url_for("login"))


@app.route("/add_user")
def add_user():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard_pages/add_user.html", sentence=username)
    else:
        return redirect(url_for("login"))


@app.route("/add_product")
def add_product():
    if "username" in session:
        username = session["username"]
        return render_template("dashboard_pages/add_product.html", sentence=username)
    else:
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
