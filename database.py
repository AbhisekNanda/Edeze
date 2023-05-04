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
    
def check_email_joinus(signup_email):
    emails=[]
    q1="SELECT Email FROM join_us;"
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
            
            if l[5] == 0:
                import json
                return json.dumps({"status":"login","User_id":l[0],"First_name":l[1],"Last_name":l[2],"Email":l[3],"status1":l[5],"type":"user"})
                
            elif l[5] == 1:
                import json
                return json.dumps({"status" :"User is deactivated"})
            else :
                import json
                return json.dumps({"status" :"User is blocked"})
        else:
            import json
            return json.dumps({"status" :"Invalid Password"})
        
    elif check_email_joinus(login_email):
        print("joinus")
        q='SELECT Password from join_us WHERE Email=?'
        data=cur.execute(q,(login_email,)).fetchall()
        con.commit()
        print(type(data[0][0]))
        check_password=login_password.encode('utf-8')
        print(type(check_password))
        import bcrypt
        result = bcrypt.checkpw(check_password, data[0][0])
        print(result)
        if result:
            q='SELECT Join_id,type,verify from join_us WHERE Email=?'
            data=cur.execute(q,(login_email,)).fetchall()
            con.commit()
            import json
            if data[0][2] == 0:

                return json.dumps({"type":data[0][1],"joinus_id":data[0][0],"verify":data[0][2],"status":"login"})
            else:
                return json.dumps({"type":data[0][1],"joinus_id":data[0][0],"verify":data[0][2],"status":"login"})
        else:
            import json
            return json.dumps({"status" :"Invalid Password"})
    else:
        import json
        return json.dumps({"status" :"Invalid Password"})
    

print(login("abhiseknanda@gmail.com","abhisek"))

def login_joinus(email):
    q='SELECT Password from join_us WHERE Email=?'
    data=cur.execute(q,(email,)).fetchall()
    con.commit()
    return type(data[0][0])

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

def signup(First_name,Last_name,Email,Password,status):
    q="""INSERT INTO user(User_id,First_name,Last_name,Email,Password,status) 
    VALUES(?,?,?,?,?,?);"""
    import bcrypt
    Password=Password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(Password, salt)
    data=(create_userid(),First_name,Last_name,Email,hashed,status)
    import joinus
    check=joinus.check_email(Email)
    print(check_email(Email))
    print(check)
    if check_email(Email) or check:
        return "User already exist"
    
    else :
        cur.execute(q,data)
        con.commit()
        return "User created"

def course(json_str = True):
    # Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration
    q="SELECT * from training"
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

def webstore():
    q="SELECT * from webstore"
    data= cur.execute(q).fetchall()
    con.commit()
    print(data)
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json


