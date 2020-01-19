import threading
import argparse
import socket
import time
import sys
from password import *
from tables import *
from user import *


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f"New connection was made from IP: {ip}, and port: {port}")

    conn_user = connect_user()
    cursor_user = conn_user.cursor()
    conn_pass = connect_auth()
    cursor_pass = conn_pass.cursor()
    
    while True:
        msg = client.recv(1024).decode()

        if msg.split(' ')[0] == 'Log':
            login = msg.split(' ')[1]
            pas = msg.split(' ')[2]
            auth_key = get_user_by_email(cursor_user, login, pas)

            if auth_key.split(' ')[0] == "Error:":
                reply = auth_key + ' Login Failed.'
                client.sendall(reply.encode('utf-8'))
            else:
                reply = auth_key
                client.sendall(reply.encode('utf-8'))

        elif msg.split(' ')[0] == 'Register':
            email = msg.split(' ')[1]
            pas = msg.split(' ')[2]
            reply = create_user(conn_user, cursor_user, email, pas)
            client.sendall(reply.encode('utf-8'))

        elif msg.split(' ')[0] == 'Update':
            email = msg.split(' ')[1]
            old_pas = msg.split(' ')[2]
            new_pas = msg.split(' ')[3]
            reply = update_password(conn_user, cursor_user, email, old_pas, new_pas)
            client.sendall(reply.encode('utf-8'))

        elif msg.split(' ')[0] == 'Delete':
            email = msg.split(' ')[1]
            pas = msg.split(' ')[2]
            reply = remove_user(conn_user, cursor_user, conn_pass, cursor_pass, email, pas)
            client.sendall(reply.encode('utf-8'))

        elif msg.split(' ')[0] == 'Add':
            user = msg.split(' ')[1]
            pas =  msg.split(' ')[2]
            domain = msg.split(' ')[3]
            auth_key = msg.split(' ')[4]
            num = new_account(conn_pass, cursor_pass, auth_key, domain, user, pas)
            if num == 1:
                reply = "New account Successfully stored!"
            else:
                reply = "Account name is already stored"
            client.sendall(reply.encode('utf-8'))

        elif msg.split(' ')[0] == 'Display':
            auth_key = msg.split(' ')[1]
            accounts = get_all_user_accounts(conn_pass, cursor_pass, auth_key)
            if len(accounts) == 0:
                reply = "Error: No accounts present to display."
                client.sendall(reply.encode('utf-8'))
            else:
                reply = ""
                for acc in accounts:
                    reply = reply + str(acc[2]) + ' '
                client.sendall(reply.encode('utf-8'))

                msg = client.recv(1024).decode()
                account = get_user_account(conn_pass, cursor_pass, auth_key, msg)
                reply = account[3]
                client.sendall(reply.encode('utf-8'))

        elif msg == 'exit':
            break
            
    print(f"The client from ip: {ip} and port: {port}, has disconnected")
    client.close()


create_tables()

parser = argparse.ArgumentParser(description = "This is server for mt socket")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sck.bind((args.host, args.port))
    sck.listen(5)
except Exception as e:
    raise SystemExit(e)

while True:
    try:
        client, ip = sck.accept()
        threading._start_new_thread(on_new_client, (client, ip))
    except KeyboardInterrupt as e:
        print(f"Shutting down the server")
    except Exception as e:
        print(e)

sck.close()