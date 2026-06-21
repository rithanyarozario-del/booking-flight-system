from flask import Flask, render_template, request, redirect, url_for, session
from main import login, register, save_bookings, get_bookings, delete_booking_by_id, get_user_email, send_eticket

app = Flask(__name__) #To run the web server

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
            return redirect(url_for("registration_success", username=username))
        #Show the result message back on the registration page

        return render_template("register.html", message=message)
    return render_template("register.html")


@app.route("/eticket/int:booking_id", methods=["POST"])
def eticket(booking_id):
    if "username" not in session:
        return redirect(url_for)


@app.route("/register/success")
def registration_success():
    username = request.args.get("username")
    return render_template("register_success.html", username=username)



@app.route("/logout")
def logout():
    session.clear() #clears the session data that logs out the user
    return redirect(url_for('home'))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login_page"))
    
    username = session["username"]

    #Read arrival destinations from an file.
    with open("destinations.txt", "r") as f:
        destinations = [line.strip() for line in f.readlines()]

    if request.method == "POST":
        booking = {
            "departure":  request.form.get("departure"),
            "arrival":    request.form.get("arrival"),
            "date":       request.form.get("date"),
            "passengers": request.form.get("passengers"),
            "adults": request.form.get("adults"),
            "children": request.form.get("children"),
            "ticket":     request.form.get("ticket"),
        }
        if not save_bookings(username, booking):
            bookings = get_bookings(username)
            return render_template("dashboard.html", username=username, bookings=bookings, destinations=destinations, message="You already have a booking on this date")
        return redirect(url_for("dashboard"))
    
    bookings = get_bookings(username)
    return render_template("dashboard.html", username=username, bookings=bookings, destinations=destinations)

@app.route("/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):
    if "username" not in session:
        return redirect(url_for("login_page"))
    delete_booking_by_id(session ["username"], booking_id)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)

    