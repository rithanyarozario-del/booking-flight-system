import os
import hashlib #Hashes users password
import sqlite3 #Allowing Pyhton to talk to my SQL database 
import re #Strong passwords for users to register or login


USERFILE = "users.txt"
DB_FILE = "bookings.db" #SQLite database file for storing bookings per user.


#Secures the Password by hashing using SHA-256 algortihm to ensure the password is not exposed.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


#Python validate password using RegEx (strong security feature)
def is_valid_password(password):
    if len(password) < 8:
pattern=re.compile(r'')
while True:
    password=getpass.getpass('Enter the password:')
    if(len(password)<6):
        return('password must be aleast 8 characters long')
    elif re.search(r'[!@#$%&]', password) is None:
        return('password must contain atleast one special symbol')
    elif re.search(r'/d', password) is None:
        return('password must alteast contain one digit')
    elif re.search('[A-Z]', password) is None:
        print('password must contain atleast one capital letter')
    elif re.match(r'[a-z A-Z 0-9 !@#$%&]{6}', password)
        pattern=re.complier(r'[a-z A-Z 0-9 !@#$%&]{6}', password)
        result=pattern.match(password)
        print()
        break
    else:
        print('password is invlaid')




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
            ticket     TEXT,
            UNIQUE(username, date)
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
    #Only insert one booking row for the given user which will not affect other users bookings.
    conn = sqlite3.connect(DB_FILE)
    c    = conn.cursor() 
    #SQL Database that stores all bookings for all users   
    try:
        c.execute("""
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
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_bookings(username):
        #Returns a list of all the bookings for the given user only.
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute ("""
             SELECT id, departure, arrival, date, passengers, ticket
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
