import sqlite3

connection = sqlite3.connect('database/database.db')


with open('stockdb.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO users (Name, Address, Email, Budget) VALUES (?, ?, ?, ?)",
#            ('Hunter', '101 Main street Bozeman, MT', 'example1@gmail.com', 100.01)
#            )

#cur.execute("INSERT INTO users (Name, Address, Email, Budget) VALUES (?, ?, ?, ?)",
#            ('John Poxson', '102 Grent Chamberlain drive Bozeman, Mt', 'example2@gamil.com', 150)
#            )

connection.commit()
connection.close()
