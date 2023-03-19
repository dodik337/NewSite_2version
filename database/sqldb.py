import sqlite3 as sq

base = sq.connect('login.db')
cur = base.cursor()
if base:
    print('DATABASE WAS CONNECTED SUCCESSFUL')
base.execute("CREATE TABLE IF NOT EXISTS {}(user TEXT PRIMARY KEY, email TEXT PRIMARY KEY, password TEXT)".format("login"))
base.commit()


async def insert_data_command(state):
    cur.execute('INSERT INTO login VALUES(?, ?, ?)', (state))
    base.commit()