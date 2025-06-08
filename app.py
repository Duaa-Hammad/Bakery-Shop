from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", sentence = "Sign Up Now", username = None)

# /index/duaahammad
@app.route("/index/<username>")
def index(username):
    return render_template("index.html", sentence=username)

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if username == "duaahammad" and password == "dpass":
            return redirect(url_for("index", username=username))
        else:
            return redirect(url_for("sign_up"))


app.run(debug=True)
