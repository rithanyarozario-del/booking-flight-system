from flask import Flask, render_template, request
from main import login, register

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        return login(username,password)
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        return register(username,password)

    return render_template("register.html")

@app.route("/submit", methods=['POST'])
def submit():

    name request.form == "POST":
        username = request.form["username"]
        password = request.form["password"]

        return register(username,password)

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)

    