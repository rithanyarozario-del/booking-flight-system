import os
import hashlib
import sqlite3

USERFILE = "users.txt"
DB_FILE = "bookings.db" #SQLite database file for storing bookings per user.


#Secures the Password by hashing using SHA-256 algortihm to ensure the password is not exposed.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db(): #Creates an booking table that does not already exist to stre users bookings seperatley. 
        conn = sqlite3.connect(DB_FILE)
    c    = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    NOT NULL,
            departure  TEXT,
            arrival    TEXT,
            date       TEXT,
            passengers TEXT,
            ticket     TEXT
        )
    """)
    conn.commit()
    conn.close()

    init_db() #Initialises the database when the website first starts.


def users_exist(username):
    #Returns to True ifthe username is already registred, otherwise False.
    if not os.path.exists(USERFILE):
        return False
    
    with open(USERFILE, "r") as f:
        return any(line.startswith(f"{username}:") for line in f)
    
    
def register(username, password):
    #Add a new user, rejecting duplicates.
    if users_exist(username):
        return "Username already exists"      
    with open(USERFILE, "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")
    return "Registration successful"


def login(username, password):
    #Returns Login as successful if the username and password match, otherwise Login Failed.
    if not os.path.exists(USERFILE):
        return "No Users Registered"
    hashed = hash_password(password)   
    with open(USERFILE, "r") as f:
        for line in f:
            if line.strip() == f"{username}:{hashed}":
                return "Login Successful"
    return "Login Failed"


def save_bookings(username, booking):
    #Only insert one bokign row for the given user which will not affect other users bookings.
    conn = sqlite3.connect(DB_FILE)
    c    = conn.cursor()    c.execute("""
        INSERT INTO bookings (username, departure, arrival, date, passengers, ticket)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        booking.get ("departure"),
        booking.get ("arrival"),
        booking.get ("date"),
        booking.get ("passengers"),
        booking.get ("ticket"),
    ))
    conn.commit()
    conn.close()

    def get_bookings(username):
        #Returns a list of all the bookings for the given user only.
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
