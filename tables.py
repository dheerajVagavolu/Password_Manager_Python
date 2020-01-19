from password import *
from user import *


def create_tables():
    con = connect_auth()
    cursor = con.cursor()

    #Already created the table
    table_auth(con, cursor)
    con.close()

    con2 = connect_user()
    con_cur = con2.cursor()

    try:
        con_cur.execute("""CREATE TABLE users (
                    UserId text,
                    Email text,
                    Password text
                )""")
    except:
        print("User Table already exists")

    con2.close()
