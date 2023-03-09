import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def course_id():
    for i in cur.execute("SELECT MAX(Course_id) from course_online"):
        pass
    return i[0]+1

def AddCouse(Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration):
    #Price_enroll is course price
    #Price_course is cd and pendrive price
    q="""INSERT INTO course_online(Course_id,Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,class,Pendrive,cd,Type,Start_date,Duration) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    data=(course_id(),Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration)
    cur.execute(q,data)
    con.commit()

    return "Course Added"

def course_details(Course_id):
    q='SELECT * FROM course_online WHERE Course_id=?'
    data= cur.execute(q,(Course_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def search(s):
    q='SELECT * FROM course_online WHERE Course_name LIKE ? OR Desc LIKE ?'
    x='%'+s+'%'
    data= cur.execute(q,(x,x)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

