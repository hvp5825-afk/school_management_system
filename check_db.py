import sqlite3
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("SELECT username, role FROM authentication_user WHERE username='admin'")
print(c.fetchall())
