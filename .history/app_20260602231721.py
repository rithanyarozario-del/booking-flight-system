from flask import Flask, render_template, request
from main import login

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result=login(username,password)
        ret
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)

    