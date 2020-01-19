import threading
import sqlite3
import socket
import uuid
import time
import sys
from password import *

def connect_user():
    try:
        con = sqlite3.connect('users.db')
        print("Connection Established to user database.")
        return con
    except Error:
        print(Error)

# Log In
def get_user_by_email(c, Email, pas):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        return "Error: No Account with the given E-mail exist."
      

    c.execute("SELECT * FROM users WHERE Email = :Email AND Password = :Password", {'Email': Email, 'Password': pas})
    if(len(c.fetchall()) == 0):
        return "Error: Incorrect Password."


    c.execute("SELECT * FROM users WHERE Email = :Email AND Password = :Password", {'Email': Email, 'Password': pas})
    return c.fetchone()[0]

# Sign Up
def create_user(conn, c, Email, Password):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) > 0):
        return "Account with the given E-mail already exist."

    UserId = uuid.uuid4().hex
    with conn:
        c.execute("INSERT INTO users VALUES (:UserId, :Email, :Password)", {'UserId': UserId, 'Email': Email, 'Password': Password})
        return "New account created successfully!"


# Update password
def update_password(conn, c, Email, OldPassword, NewPassword):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        return "Error: No Account with the given E-mail exist."

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(c.fetchone()[2] != OldPassword):
        return "Error: Password doesn't match with the current one."

    with conn:
        c.execute("""UPDATE users SET Password = :Password WHERE Email = :Email""", {'Password': NewPassword, 'Email': Email})
        return "Password updated successfully!"


# Delete account
def remove_user(conn, c, conn_pass, cursor_pass, Email, Password):

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(len(c.fetchall()) == 0):
        return "No Account with the given E-mail exist."

    c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
    if(c.fetchone()[2] != Password):
        return "Error: Incorrect password. Account removal failed!"

    with conn:
        c.execute("SELECT * FROM users WHERE Email = :Email", {'Email': Email})
        remove_user_accounts(conn_pass, cursor_pass, c.fetchone()[0])

        c.execute("DELETE from users WHERE Email = :Email", {'Email': Email})
        return "Account deleted successfully!"