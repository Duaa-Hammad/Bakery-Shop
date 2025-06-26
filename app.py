from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import _sqlite3

app = Flask(__name__)
app.secret_key = "supersecret"

def connect_db():
    conn = _sqlite3.connect("users.db")
    conn.row_factory = _sqlite3.Row
    return conn

app.permanent_session_lifetime = timedelta(days=5)

@app.route("/")
def index():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", sentence = username)
    else:
        return render_template("index.html", sentence = "Sign Up Now", username = None)

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # set the session to permanent, so it lasts for 5 days
        session.permanent = True
        # store the username and password in the session
        # dic key = value
        session["username"] = request.form["username"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        return redirect(url_for("index"))
    
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
        return render_template("dashboard.html", sentence=username)
    else:
        return redirect(url_for("login"))


@app.route("/test")
def test():
    return render_template("test.html")
app.run(debug=True)
