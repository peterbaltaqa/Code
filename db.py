import sqlite3
from usr import Usr
from os.path import isfile

name = "data.db"

def create():

    # Return early if database is already set up
    if isfile(name):
        return
    
    accounts = [Usr("admin", "admin", True).data,
                Usr("John Smith", "123456").data,
                Usr("Jane Doe", "qwerty").data,
                Usr("Mary", "111111").data,
                Usr("Sam Jones", "dragon").data,
                Usr("Jeremy Fox", "123123").data,
                Usr("Terry Jobs", "baseball").data,
                Usr("Muhammad Li", "abc123").data,
                Usr("J.M.", "football").data,
                Usr("Jerry Allen", "monkey").data,
                Usr("Sarah McGill", "letmein").data,]

    # Create database files
    con = sqlite3.connect(name)
    cur = con.cursor()

    # Create table for accounts and load them
    cur.execute("CREATE TABLE usrs (usr PRIMARY KEY, pw NOT NULL, isadmin NOT NULL)")
    cur.executemany("INSERT INTO usrs VALUES (?, ?, ?)", accounts)
    con.commit()

    # Create table to store tickets
    cur.execute("CREATE TABLE tickets (ticketno INT PRIMARY KEY, usr, subject, status, priority, dt, FOREIGN KEY (usr) REFERENCES usrs(usr))")
    con.commit()

    # Add placeholder data 
    tickets = [ (1,  "John Smith",   "Computer not working",       "Pending",   "Low",  "2024-09-15 12:22"),
                (2,  "Jane Doe",     "cannot send any e-mails",    "Assigned",  "Low",  "2024-09-16 14:00"),
                (3,  "Mary",         "PC encrypted by ransomware", "Assigned",  "High", "2024-09-13 16:55"),
                (4,  "Sam Jones",    "Lost my keyboard",           "Resolved",  "Low",  "2012-12-21 12:00"),
                (5,  "Jeremy Fox",   "Computer Slowness",          "Resolved",  "Low",  "2024-09-09 09:09"),
                (6,  "Terry Jobs",   "Require new laptop",         "Pending",   "Low",  "2024-09-15 13:30"),
                (7,  "Muhammad Li",  "Servers are down",           "Pending",   "High", "2024-10-01 13:37"),
                (8,  "J.M.",         "New Starter Onboarding",     "Assigned",  "Low",  "2024-09-10 21:00"),
                (9,  "Jerry Allen",  "monitor is cracked!",        "Resolved",  "Low",  "2024-09-13 17:38"),
                (10, "Sarah McGill", "Blue-screen when booting",   "Resolved",  "High", "2024-07-19 04:10")]
    
    cur.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?)", tickets)
    con.commit()

    con.close()

def table():

    if not isfile(name):
        create()

    con = sqlite3.connect(name)
    cur = con.cursor()   

    res = cur.execute("SELECT * FROM tickets").fetchall()
    con.close()

    return res

def usrs():

    con = sqlite3.connect(name)
    cur = con.cursor()   

    res = cur.execute("SELECT usr FROM usrs").fetchall()

    con.close()

    return res

def update(request):
    con = sqlite3.connect(name)
    cur = con.cursor()   

    request = request.form.to_dict()
    request.pop("save")

    columns = ["ticketno", "usr", "subject", "status", "priority", "dt"]

    if request.get("new 0") is not None:
        ticketno = request.get("new 0") 

    for i in request:
        field = i.split()

        if columns[int(field[1])] == "ticketno" and not request[i].isnumeric():
            con.close()
            return "Integer"

        if (field[1] == "del"):
            cur.execute(f"DELETE FROM tickets WHERE ticketno = {field[0]}")
        
        elif (columns[int(field[1])] == "ticketno" and field[0] == "new"):

            cur.execute(f"INSERT INTO tickets (ticketno) VALUES ({ticketno})")

        else:
            if request.get("new 0") is None:
                cur.execute(f"UPDATE tickets SET {columns[int(field[1])]} = '{request[i]}' WHERE ticketno = '{field[0]}'")
            else:
                cur.execute(f"UPDATE tickets SET {columns[int(field[1])]} = '{request[i]}' WHERE ticketno = '{ticketno}'")

    con.commit()
    con.close()

def chk_usr(usr):
    con = sqlite3.connect(name)
    cur = con.cursor()

    res = cur.execute(f"SELECT usr FROM usrs WHERE usr = '{usr}'").fetchall()

    con.close()
    return not res

def add_usr(usr, pw):
    con = sqlite3.connect(name)
    cur = con.cursor()
    
    NewUser = Usr(usr, pw)

    cur.execute(f"INSERT INTO usrs VALUES ('{NewUser.usrname}', '{NewUser.pw}', {False})")

    con.commit()
    con.close()