import sqlite3
from sqlite3 import Error
from datetime import datetime

def connect_auth():
    try:
        con = sqlite3.connect('passwords.db')
        print("Connection Established to Password database")
        return con
    except Error:
        print(Error)


def table_auth(con, cursor):
    try:
        cursor.execute("CREATE TABLE Passwords(auth_key varchar, domain varchar, username varchar, password varchar)")
        con.commit()
    except:
        print("Password Table already Exists")

def new_account(con, cursor ,auth_key, domain, username, password):

    with con:
        cursor.execute("SELECT * FROM Passwords WHERE username = :username",{"username": username})
    
    queries_check = cursor.fetchall()

    if len(queries_check) == 0:
        with con:
            cursor.execute("INSERT INTO Passwords values(?, ?, ?, ?)", (auth_key, domain, username, password))
        print("Account Stored Successfully")
        return 1
    else:
        print("Account with this key already exists")
        return 0

def user_all_accounts(con, cursor, auth_key):
    with con:
        cursor.execute("SELECT * FROM Passwords WHERE auth_key = :auth_key",{"auth_key": auth_key})
    return cursor.fetchall()

def user_account(con, cursor, auth_key, username):
    with con:
        cursor.execute("SELECT * FROM Passwords WHERE username = :username AND auth_key = :auth_key" ,{"username": username,"auth_key": auth_key })
    return cursor.fetchall()



