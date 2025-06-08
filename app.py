from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecret"

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
        session["password"] = request.form["password"]
        return redirect(url_for("index"))
app.run(debug=True)
