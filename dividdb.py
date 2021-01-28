import sqlite3

def set_dividdb():
    connection = sqlite3.connect('database/database.db')


    with open('dividend.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

#cur.execute("INSERT INTO users (Name, Address, Email, Budget) VALUES (?, ?, ?, ?)",
#            ('Hunter', '101 Main street Bozeman, MT', 'example1@gmail.com', 100.01)
#            )

    connection.commit()
    connection.close()
