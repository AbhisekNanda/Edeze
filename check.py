import sqlite3
import datetime

con = sqlite3.connect("mybd.sqlite",check_same_thread=False)

cur = con.cursor()

q='CREATE TABLE otp (Email PRIMARY KEY,Otp)'
x=cur.execute(q)
con.commit()
