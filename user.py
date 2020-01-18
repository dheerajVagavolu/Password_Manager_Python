import sqlite3
import uuid
import sqlite3
import socket
import sys
import threading
import time
from queue import Queue

def connect_user():
    try:
        con = sqlite3.connect('users.db')
        print("Connection Established to user database")
        return con
    except Error:
        print(Error)

# Log In
def get_user_by_email(c, Email, pas):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        print("No Account with the given E-mail exist!")
        return "error"
      

    c.execute("SELECT * FROM users WHERE Email = :Email AND Password = :Password", {'Email': Email, 'Password': pas})
    if(len(c.fetchall()) == 0):
        print("Incorrect Password!")
        return "error"


    c.execute("SELECT * FROM users WHERE Email = :Email AND Password = :Password", {'Email': Email, 'Password': pas})
    return c.fetchone()[0]

# Sign Up
def create_user(conn,c, Email, Password):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) > 0):
        print("Account with the given E-mail already exist!")
        exit(0)

    UserId = uuid.uuid4().hex
    with conn:
        c.execute("INSERT INTO users VALUES (:UserId, :Email, :Password)", {'UserId': UserId, 'Email': Email, 'Password': Password})


# Update password
def update_password(c, Email, OldPassword, NewPassword):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        print("No Account with the given E-mail exist!")
        exit(0)

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(c.fetchone()[2] != OldPassword):
        print("Password doesn't match with the current one!")
        exit(0)

    with conn:
        c.execute("""UPDATE users SET Password = :Password WHERE Email = :Email""", {'Password': NewPassword, 'Email': Email})

# Delete account
def remove_user(c, Email):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        print("No Account with the given E-mail exist!")
        exit(0)

    with conn:
        c.execute("DELETE from users WHERE Email = :Email", {'Email': Email})