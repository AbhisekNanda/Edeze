import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def user_course(User_id):
    # Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration
    q="SELECT course_online.Course_name,course_online.Catgory,course_online.Price_enroll,course_online.Price_course,course_online.DESC,course_online.Author,course_online.Rating,course_online.Date,course_online.class,course_online.Pendrive,course_online.cd,course_online.Type,course_online.Start_date ,course_online.Duration FROM ((user INNER JOIN enroll ON user.User_id = enroll.User_id) INNER JOIN course_online ON course_online.Course_id = enroll.Course_id) WHERE user.User_id = ? "

    data=cur.execute(q,(User_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ': '))

    return data_json

def buy_course(user_id,course_id):
    q='INSERT INTO enroll(User_id,Course_id) VALUES(?,?);'
    data = (user_id,course_id)
    cur.execute(q,data)
    con.commit()

    return 'Course added'

def buy_mentor(user_id,join_id):
    q='INSERT INTO enroll_mentor(User_id,Join_id) VALUES(?,?);'
    data = (user_id,join_id)
    cur.execute(q,data)
    con.commit()

    return 'Mentor Added'

def user_mentor(User_id):
    
    q="SELECT mentor.First_Name,mentor.Last_Name,mentor.Email,mentor.IDCard,mentor.Qualification,mentor.About,mentor.Session_Price FROM ((user INNER JOIN enroll_mentor ON user.User_id = enroll_mentor.User_id) INNER JOIN mentor ON mentor.Join_id = enroll_mentor.Join_id) WHERE user.User_id = ? "

    data=cur.execute(q,(User_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ': '))

    return data_json

def block_user(user_id):
    q="UPDATE user SET status = -1 WHERE user_id =?;"

    cur.execute(q,(user_id,))
    con.commit()

    import json
    return json.dumps({"status" :"User blocked"})

def deactivate_user(user_id):
    q="UPDATE user SET status = 1 WHERE user_id =?;"

    cur.execute(q,(user_id,))
    con.commit()

    import json
    return json.dumps({"status" :"User deactivate"})

def activate_user(user_id):
    q="UPDATE user SET status = 0 WHERE user_id =?;"

    cur.execute(q,(user_id,))
    con.commit()

    import json
    return json.dumps({"status" :"User activate"})

def user(json_str = True):
    q="SELECT User_id,First_name,Last_name,email,status from user"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json



