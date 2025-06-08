from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route("/")
def home():
    return render_template("index.html", sentence = "Sign Up Now", username = None)

# /index/duaahammad
@app.route("/index")
def index():
    if "username" in session:
        username = session["username"]
        return render_template("index.html", sentence = username)

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # dic key = value
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        return redirect(url_for("index"))
app.run(debug=True)
