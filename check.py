import sqlite3
import json
con = sqlite3.connect("mybd.sqlite",check_same_thread=False)

cur = con.cursor()


# q="CREATE TABLE consult(Cons_id INTEGER PRIMARY KEY,Join_id INTEGER,Consult_name VARCHAR,Category VARCHAR,Price INTEGER,DESC VARCHAR,Author VARCHAR)"
# data= cur.execute(q)
# con.commit()
    

import course
name=course.user_first_name(id)