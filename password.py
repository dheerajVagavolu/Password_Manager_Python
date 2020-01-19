import sqlite3
from sqlite3 import Error
from datetime import datetime

def connect_auth():
    try:
        conn = sqlite3.connect('passwords.db')
        print("Connection Established to Password database")
        return conn
    except Error:
        print(Error)


def table_auth(conn, cursor):
    try:
        cursor.execute("CREATE TABLE Passwords(auth_key varchar, domain varchar, username varchar, password varchar)")
        conn.commit()
    except:
        print("Password Table already Exists")


def new_account(conn, cursor, auth_key, domain, username, password):
    cursor.execute("SELECT * FROM Passwords WHERE username = :username", {"username": username})

    if len(cursor.fetchall()) > 0:
        #print("Account with this key already exists")
        return 0
    else:
        with conn:
            cursor.execute("INSERT INTO Passwords values(?, ?, ?, ?)", (auth_key, domain, username, password))
            #print("Account Stored Successfully")
            return 1


def get_all_user_accounts(conn, cursor, auth_key):
    cursor.execute("SELECT * FROM Passwords WHERE auth_key = :auth_key", {"auth_key": auth_key})
    return cursor.fetchall()


def get_user_account(conn, cursor, auth_key, username):
    cursor.execute("SELECT * FROM Passwords WHERE username = :username AND auth_key = :auth_key" ,{"username": username,"auth_key": auth_key })
    return cursor.fetchone()


def remove_user_accounts(conn, cursor, auth_key):
    with conn:
        cursor.execute("DELETE FROM passwords WHERE auth_key = :auth_key", {'auth_key': auth_key})