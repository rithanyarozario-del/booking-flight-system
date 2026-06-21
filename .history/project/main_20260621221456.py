import os
import hashlib #Hashes users password
import sqlite3 #Allowing Pyhton to talk to my SQL database 
import re #Strong passwords for users to register or login
from datetime import datetime


USERFILE = "users.txt"
DB_FILE = "bookings.db" #SQLite database file for storing bookings per user.


#Secures the Password by hashing using SHA-256 algortihm to ensure the password is not exposed.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


#Python validate password using RegEx (strong security feature)
def is_valid_password(password):
    if len(password) < 8:
        return "Password must be aleast 8 characters long"
    
    if not re.search(r'[!@#$%&]', password):
        return "Password must contain atleast one special symbol"
    if not re.search('[A-Z]', password):
        return "Password must contain atleast one capital letter"
    return None




def init_db(): #Creates an booking table that does not already exist to stre users bookings seperatley. 
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    NOT NULL,
            departure  TEXT,
            arrival    TEXT,
            date       TEXT,
            passengers TEXT,
            adults     TEXT,
            children   TEXT,
            ticket     TEXT,
            UNIQUE(username, date)
        )
    """)
    conn.commit()
    conn.close()

init_db() #Initialises the database when the website first starts.



#SQL Table storing flight prices (Sqlite)
def init_flights_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_code    TEXT NOT NULL UNIQUE,
            departure      TEXT NOT NULL,
            arrival        TEXT NOT NULL,
            dep_time       TEXT,
            arr_time       TEXT,
            base_fare      REAL NOT NULL,
        )
    """)
    conn.commit()
    conn.close()

#Adds the flight routes and prices, but only once
def seed_flights():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM flights")
    if c.fetchone()[0] == 0:
    c.executemany("""
        INSERT INTO flights (flight_code, departure, arrival, dep_time, arr_time, base_fare)
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ("RY01", "Sydney", "Melbourne", "09:00", "10:30", 150.00),
        ("RY02", "Melbourne", "Sydney", "11:00", "12:30", 150.00),
        ("RY03", "Sydney", "Brisbane", "08:30", "10:30", 200.00),
        ("RY04", "Brisbane", "Sydney", "13:00", "15:00", 200.00),
        ("RY05", "Sydney", "Adelaide", "09:00", "12:00", 180.00),
        ("RY06", "Adelaide", "Sydney", "13:00", "16:00", 180.00),
        ("RY07", "Melbourne", "Brisbane", "10:00", "12:00", 190.00),
        ("RY08", "Brisbane", "Melbourne", "14:00", "16:00", 190.00),
        ("RY09", "Adelaide", "Melbourne", "09:30", "11:00", 160.00),
        ("RY010", "Melbourne", "Adelaide", "12:00", "01:30", 160.00),
        ("RY011", "Adelaide", "Brisbane", "10:00", "13:00", 220.00),  
        ("RY012", "Brisbane", "Adelaide", "14:00", "17:00", 220.00),    
    ])
    conn.commit()
    conn.close()

#Cost changes depending on how many baggage, adults and children are part of the booking
BAGGAGE_FEE = 30.00
CHILD_DISCOUNT = 0.5

def calculate_cost(departure, arrival, adults, children, bags)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT base_fare FROM flights WHERE departure = ? AND arrival = ?", (departure, arrival))
    row = c.fetchone()
    conn.close()
    if row is None: 
        return None
    base_fare = row[0]
    adult_cost = int(adults) * base_fare
    child_cost = int(children) * base_fare * CHILD_DISCOUNT
    baggage_cost = int(bags) * BAGGAGE_FEE
    return round()


#Increases price based on date and how closer depature and arrival dates are to today
def apply_date_surcharge(base_cost, departure_date_str):
    departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d")
    today = datetime.today()
    days_until_departure = (departure_date - today).days

    if days_until_departure <= 7:
        return base_cost * 1.20
    elif days_until_departure <= 14:
        return base_cost * 1.10
    else:
        return base_cost



def users_exist(username):
    #Returns to True ifthe username is already registred, otherwise False.
    if not os.path.exists(USERFILE):
        return False
    
    with open(USERFILE, "r") as f:
        return any(line.startswith(f"{username}:") for line in f)
    
    
def register(username, password, email):
    #Add a new user, rejecting duplicates.
    if users_exist(username):
        return "Username already exists"  
    error=is_valid_password(password)
    if error:
        return error   
    with open(USERFILE, "a") as f:
        f.write(f"{username}:{hash_password(password)}:{email}\n")
    return "Registration successful"


def login(username, password):
    #Returns Login as successful if the username and password match, otherwise Login Failed.
    if not os.path.exists(USERFILE):
        return "No Users Registered"
    hashed = hash_password(password)   
    with open(USERFILE, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if parts[0] == username and parts[1] == hashed:
                return "Login Successful"
    return "Login Failed"


def get_user_email(username):
    with open(USERFILE, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if parts[0] == username:
                return parts[2]
    return None


def send_eticket(to_email, booking):
    import smtplib
    from email.mime.text import MIMEText
    msg = MIMEText(f"Departure: {booking['departure']}\nArrival: {booking['arrival']}\nDate: {booking['date']}")
    msg["Subject"] = "Your E-Ticket"
    msg["From"] = "flightpath73@gmail.com"
    msg["To"] = to_email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("flightpath73@gmail.com", os.environ.get("EMAIL_APP_PASSWORD"))
        server.send_message(msg)




def save_bookings(username, booking):
    #Not allowing the same city input for departure and arrival
    if booking.get("departure") == booking.get("arrival"):
        return "Departure and Arrival cities can not be the same"
    #Only insert one booking row for the given user which will not affect other users bookings.
    conn = sqlite3.connect(DB_FILE)
    c    = conn.cursor() 
    #SQL Database that stores all bookings for all users   
    try:
        c.execute("""
            INSERT INTO bookings (username, departure, arrival, date, passengers, adults, children, ticket)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            booking.get ("departure"),
            booking.get ("arrival"),
            booking.get ("date"),
            booking.get ("passengers"),
            booking.get ("adults"),
            booking.get ("children"),
            booking.get ("ticket"),
        ))
        conn.commit()
        return "OK"
    except sqlite3.IntegrityError:
        return "You already have an booking on this date"
    finally:
        conn.close()

def get_bookings(username):
        #Returns a list of all the bookings for the given user only.
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("""
             SELECT id, departure, arrival, date, passengers, adults, children, ticket
             FROM   bookings
             WHERE  username = ?
             ORDER  BY id DESC
        """, (username,))
        rows = [dict(row) for row in c.fetchall()]
        conn.close()
        return rows

def delete_booking_by_id(username, booking_id):
    #Deletes Bookings for users based on the booking id that doesnt affect other users bookings.
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id = ? AND username = ?", (booking_id, username))
    conn.commit()
    conn.close()
