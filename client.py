import socket 
import argparse

parser = argparse.ArgumentParser(description = "This is client for mt socket")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 9999)
args = parser.parse_args()

print(f"Connecting to server: {args.host} on port: {args.port}")

auth_key = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
    try:
        con.connect((args.host, args.port))
    except Exception as e:
        raise SystemExit(f"Failed to connect to host: {args.host} on port: {args.port}")

    while True:
        if auth_key == "":
            what = input("Options available: register login exit: ")
            if what == 'login':
                msg = input("Enter username: ")
                pas = input("Enter Password: ")
                message = what + ' ' + msg + ' ' + pas
                con.sendall(message.encode('utf-8'))
                data = con.recv(1024).decode()
                print(f"The server's response: {data}")
                if data != "error: Login Failed":
                    auth_key = data.split(' ')[0]
            elif what == 'register':
                msg = input("Enter username: ")
                pas = input("Enter Password: ")
                message = what + ' ' + msg + ' ' + pas
                con.sendall(message.encode('utf-8'))
                data = con.recv(1024)
                print(f"The server's response: {data.decode()}")
            elif what == 'exit':
                con.sendall(what.encode('utf-8'))
                print("Exiting ....")
                break

        else:
            # print("Successful login ")
            # print("UserID: "+auth_key)
            what = input("Options available: Add fetch display logout ")

            if what == "logout":
                auth_key = ""
            elif what == "display":
                whatt = what +" "+auth_key
                con.sendall(whatt.encode('utf-8'))
                data = con.recv(1024).decode()
                print(data) 
            elif what == "Add":
                user = input("Enter username: ")
                pas = input("Enter password: ")
                dom = input("Enter domain: ")
                whatt = what + ' ' + user+ ' '+pas + ' ' +dom+' '+auth_key
                # print(whatt)   
                con.sendall(whatt.encode('utf-8'))
                data = con.recv(1024).decode()
                print(data)
            else:
                print("Invalid option")
