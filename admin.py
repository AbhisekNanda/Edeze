import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def total_user():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT count(user_id) as t FROM user"
    data= cur.execute(q).fetchall()
    con.commit()
    
    return data[0][0]

def total_mentor():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT count(Join_id) as t FROM mentor"
    data= cur.execute(q).fetchall()
    con.commit()
    
    return data[0][0]

def total_mentor():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT count(Join_id) as t FROM mentor"
    data= cur.execute(q).fetchall()
    con.commit()
    
    return data[0][0]

def total_university():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT count(Join_id) as t FROM university"
    data= cur.execute(q).fetchall()
    con.commit()
    
    return data[0][0]

def total_ia():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT count(Join_id) as t FROM individual_author"
    data= cur.execute(q).fetchall()
    con.commit()
    
    return data[0][0]

def recent_order():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT * FROM order_webstore"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json
    
def all_user():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT User_id,First_name,Last_name,Email,status FROM user"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def verifymentor():
    q='select '

def all_course():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT * FROM training"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def all_course_webstore():
     # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="SELECT * FROM webstore"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json


def all_course_mentor():
     # q="SELECT * FRM training_cart WHERE User_id = ?"
    q="SELECT * FROM consult"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def verifyIA():
    #q= "SELECT individual_author.First_name,individual_author.Last_name,individual_author.About FROM join_us WHERE verify=1"
    q="""SELECT individual_author.Join_id,individual_author.First_Name,individual_author.Last_name,individual_author.About FROM individual_author
    INNER JOIN join_us ON join_us.Join_id =individual_author.Join_id WHERE join_us.verify=1"""
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def verifymentor():
    q="""SELECT mentor.Join_id,mentor.First_Name,mentor.Last_name,mentor.About FROM mentor
    INNER JOIN join_us ON join_us.Join_id =mentor.Join_id WHERE join_us.verify=1"""
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def verifyuni():
    q="""SELECT university.Join_id,university.University_Name,university.Department_Name,university.About FROM university
    INNER JOIN join_us ON join_us.Join_id =university.Join_id WHERE join_us.verify=1"""
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json


def verify(Join_id):
    q="UPDATE join_us SET verify = 0 WHERE Join_id =?;"

    cur.execute(q,(Join_id,))
    con.commit()

    import json
    return json.dumps({"status" :"User blocked"})


