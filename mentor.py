import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def myconsult(join_id):
    q="SELECT * FROM consult WHERE Join_id=?"
    data= cur.execute(q,(join_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def create_consid():
    for i in cur.execute("SELECT MAX(Cons_id) from consult"):
        pass
    return i[0]+1

print(create_consid())

def AddConuslting(join_id,courseName,category,price,description,authorName):
    q="INSERT INTO consult (Cons_id, Join_id, Consult_name,Category,Price,DESC,Author)VALUES (?,?,?,?,?,?,?)"
    data= cur.execute(q,(create_consid(),join_id,courseName,category,price,description,authorName)).fetchall()
    con.commit()

    return "consult added"