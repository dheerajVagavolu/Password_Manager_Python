# [CS3210] Computer Networks Laboratory - Lab 1

## I. Instructions for Running:
        1. To start the server: 
                        'make server host=<ipaddress> port=<port_number>'

        2. To start the application from the client: 
                        'make client host=<ipaddress> port=<port_number>'

        3. After running the server, the two database files are created in the folder. To remove them use 
                        'make clean'

## NOTE:
    1. Before running the application on the client/user computer, execute the following command:
                    For windows - 'pip install requirements.txt'
                    For linux - 'pip3 install requirements.txt'
    2. If there are any errors during installing packages, run 'sudo apt upgrade', 'sudo apt update' and then try again.
    3. The host and port arguments are not necessary as their default value is set to 127.0.0.1 and 9999. 
    4. To test them on same computer, 'make server' and 'make client' are sufficient


## II. Files invloved in the application:
        1. server.py – Contains code required to set up a server and serve the queries from multiple clients paralelly.
        2. client.py – Contains the code for user interface and making server requests.
        3. password.py – API for storing, retrieving, deleting the user passwords from database.
        4. user.py – API for storing the credentials of master accounts in the database.
        5. table.py – Creates the database 'passwords.db' and 'users.db'.
        6. requirements.txt - used to install the dependencies/packages required.