import socket
import argparse
import sqlite3
import uuid
import sys
import threading
import time
from database import *
from user import *
from tables import *


create_tables()
# con_pass = connect_auth()
# cursor_pass = con_pass.cursor()


parser = argparse.ArgumentParser(description = "This is server for mt socket")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sck.bind((args.host,args.port))
    sck.listen(5)
except Exception as e:
    raise SystemExit(e)

def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f"New connection was made from IP: {ip}, and port: {port}")
    con_user = connect_user()
    cursor_user = con_user.cursor()
    con_pass = connect_auth()
    cursor_pass = con_pass.cursor()
    
    while True:
        msg = client.recv(1024).decode()
        if msg == 'exit':
            break
        elif msg.split(' ')[0] == 'register':
            login = msg.split(' ')[1]
            pas = msg.split(' ')[2]
            create_user(con_user, cursor_user, login, pas)
            reply = 'New account created successfully'
            client.sendall(reply.encode('utf-8'))
        elif msg.split(' ')[0] == 'login':
            login = msg.split(' ')[1]
            pas = msg.split(' ')[2]
            auth_key = get_user_by_email(cursor_user,login, pas)
        # print(f"The client said: {msg.decode()}")
            if auth_key == "error":
                reply = auth_key+": Login Failed"
                client.sendall(reply.encode('utf-8'))
            else:
                reply = auth_key+": Login Successful"
                client.sendall(reply.encode('utf-8'))
        elif msg.split(' ')[0] == 'display':
            auth_key = msg.split(' ')[1]
            accounts = user_all_accounts(con_pass, cursor_pass, auth_key)
            if len(accounts) == 0:
                reply = "No accounts present to display"
                client.sendall(reply.encode('utf-8'))
            else:
                reply = ""
                for acc in accounts:
                    reply = reply + str(acc[2]) + ' '
                client.sendall(reply.encode('utf-8'))
        elif msg.split(' ')[0] == 'Add':
            user = msg.split(' ')[1]
            pas =  msg.split(' ')[2]
            domain = msg.split(' ')[3]
            auth_key = msg.split(' ')[4]
            num = new_account(con_pass,cursor_pass, auth_key, domain, user, pas)
            if num == 1:
                reply = "New account Successfully created"
            else:
                reply = "Account name already exists"
            client.sendall(reply.encode('utf-8'))
            
    print(f"The client from ip: {ip} and port: {port}, has disconnected")
    client.close()

while True:
    try:
        client, ip = sck.accept()
        threading._start_new_thread(on_new_client,(client,ip))
    except KeyboardInterrupt as e:
        print(f"Shutting down the server")
    except Exception as e:
        print(e)

sck.close()