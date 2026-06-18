from flask import Flask, render_template, request, redirect, url_for, session
from main import login, register, save_bookings, get_bookings 

app = Flask(__name__)

#secret keyfor session cookies 
app.secret_key = "your_secret_key_here"

#Home route
@app.route("/")
def home():
    return render_template("home.html")


#Login route
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = login(username, password)

        if result == "Login Successful":
            session["username"] = username #stores your username in session so we know who is logged in
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", message="Invalid Username or Password")

    return render_template("login.html")


#Register route
@app.route("/register", methods=["GET", "POST"])
def register_page():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = register(username, password)

        if message == "Registration successful":
            return redirect(url_for"registration_success", username=username))
        #Show the result message back on the registration page

        return render_template("register.html", message=message)
    return render_template("register.html")

@app.route("/register/success")
def registration_success():
    username = request.args.get("username")
    return render_template("registration_success.html", username=username)



@app.route("/logout")
def logout():
    session.clear() #clears the session data that logs out the user
    return redirect(url_for('home'))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if 

    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        comment = request.form["comment"]
        #Simple Validation
        if not name or not email or not comment:
            return "Please fill in all fields.", 400
        return redirect(url_for('thank_you'))
    return render_template('booking.html')

@app.route("/thankyou")
def thank_you():
        return "Thank you for your feedback!"


if __name__ == "__main__":
    app.run(debug=True)

    