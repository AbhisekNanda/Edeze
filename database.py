import sqlite3
import json

# Create a SQL connection to our SQLite database
con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row

cur = con.cursor()

def check_table():
    for i in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        print(i)
    if "user" not in i  :
        table = """ CREATE TABLE user (
                    User_id INTEGER NOT NULL Primary key,
                    First_Name CHAR(25) NOT NULL,
                    Last_Name CHAR(25) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    Phone INTEGER NOT NULL, 
                    Password CHAR(25) NOT NULL,
                    DOB CHAR(25)
            );"""
        cur.execute(table)
    if "course_online" not in i:
        table=""" CREATE TABLE course_online(
            Course_id INTEGER NOT NULL Primary key,
            Course_name CHAR(100) NOT NULL,
            Duration CHAR(25) NOT NULL,
            Category CHAR(10) NOT NULL,
            Price INTEGER NOT NULL,
            DESC CHAR(100) NOT NULL,
            Author CHAR(50),
            Rating Integer NOT NULL,
            Time CHAR(20)
        );"""
        cur.execute(table)
    if "enroll" not in i:
        table="""CREATE TABLE enroll(
            User_id INTEGER NOT NULL Primary key,
            Course_id INTEGER NOT NULL
        )"""
        cur.execute(table)

def check_email(signup_email):
    emails=[]
    q1="SELECT Email FROM user;"
    for email in cur.execute(q1):
        emails.append(email[0])
    if signup_email in emails:
        return True
    else :
        return False
    
def login(login_email,login_password):
    if check_email(login_email):
        q='SELECT Password from user WHERE Email=?'
        data=cur.execute(q,(login_email,)).fetchall()
        con.commit()
        check_password=login_password.encode()
        import bcrypt
        result = bcrypt.checkpw(check_password, data[0][0])
        if result:
            q='SELECT * from user WHERE Email=?'
            login_data=cur.execute(q,(login_email,)).fetchall()
            con.commit()
            l=[]
            for i in login_data[0] :
                l.append(i)
            import json
            return json.dumps({"User_id":l[0],"First_name":l[1],"Last_name":l[2],"Email":l[3],"Phone":l[4],"DOB":l[6]})
        else:
            return "Invalid Password"
    else:
        return "Invalid Email"
print(login('abhisk11@gamil.com',"1234"))
def create_userid():
    for i in cur.execute("SELECT MAX(User_id) from user"):
        pass
    return i[0]+1

def create_otp(rec_email):
    import random
    import mail

    otp=random.randint(1111,9999)
    status = {"status":mail.send_otp(rec_email,otp)}
    q='INSERT INTO otp(Email,Otp) VALUES(?,?)'
    cur.execute(q,(rec_email,otp))
    con.commit()
    return json.dumps(status)

def verify_otp(rec_email,check_otp):
    q='SELECT Otp FROM otp WHERE Email=?'
    data=cur.execute(q,(rec_email,))
    con.commit()
    otp=[]
    for i in data:
        otp.append(i[0])
    
    if otp[0]==check_otp:
        q='DELETE FROM otp WHERE Email=?'
        data=cur.execute(q,(rec_email,))
        con.commit()
        return json.dumps({"status":"OTP is correct"})
    else:
        return json.dumps({"status":"OTP is incorrect"})

def signup(First_name,Last_name,Email,Phone,Password,DOB):
    q="""INSERT INTO user(User_id,First_name,Last_name,Email,Phone,Password,DOB) 
    VALUES(?,?,?,?,?,?,?);"""
    import bcrypt
    Password=Password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(Password, salt)
    data=(create_userid(),First_name,Last_name,Email,Phone,hashed,DOB)
    if check_email:
        cur.execute(q,data)
        con.commit()
        return "User created"
    else :
        return "user already exist"

def course(json_str = True):
    # Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration
    q="SELECT Course_name,Catgory,Price_enroll,Desc,Author,Rating,Date,Type,Start_date,Duration from course_online WHERE class=1"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def user_course(id):
    q='SELECT * from course_online where Course_id=1'
    data_new=cur.execute(q).fetchall()
    con.commit()
    # data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_new

def mentor(json_str = True):
    q="SELECT * from mentor"
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json
