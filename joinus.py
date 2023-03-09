import sqlite3
import json


con = sqlite3.connect("mybd.sqlite",check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

def join_id():
    for i in cur.execute("SELECT MAX(Join_id) from join_us"):
        pass
    return i[0]+1

def check_email(signup_email):
    emails=[]
    q1="SELECT Email FROM join_us;"
    for email in cur.execute(q1):
        emails.append(email[0])
    if signup_email in emails:
        return False
    else :
        return True

def signup_individual_author(First_name,Last_name,Email,Raw_Password,IDCard,About,Qualification):

    
    q="""INSERT INTO individual_author(Join_id,First_name,Last_name,Email,Password,IDCard,About,Qualification) 
    VALUES(?,?,?,?,?,?,?,?);"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type) 
    VALUES(?,?,?,?);"""
    if check_email(Email):
        import bcrypt
        Password=Raw_Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),First_name,Last_name,Email,str(hashed),IDCard,About,Qualification)
        join_data=(join_id(),Email,str(hashed),'individual_author')
        cur.execute(q,data)
        con.commit()
        cur.execute(r,join_data)
        con.commit()
        return "User is created"
    else:
        return "email alraedy exist"

def login(email,password):
    if check_email(email):
        q='SELECT Password from join_us WHERE Email=?'
        data=cur.execute(q,(email,)).fetchall()
        data_password= (data[0][0].split("'"))[1].encode("utf-8")
        check_password=password.encode()
        import bcrypt
        result = bcrypt.checkpw(check_password, data_password)
        
    else:
        return "Invalid Email"

def signup_mentor(First_Name,Last_Name,Email,Password,IDCard,Qualification,About,Session_Price):
    q="""INSERT INTO mentor(Join_id,First_name,Last_name,Email,Password,IDCard,Qualification,About,Session_Price) 
    VALUES(?,?,?,?,?,?,?,?,?);"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type) 
    VALUES(?,?,?,?);"""

    if check_email(Email):
        import bcrypt
        Password=Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),First_Name,Last_Name,Email,str(hashed),IDCard,Qualification,About,Session_Price)
        join_data=(join_id(),Email,str(hashed),'mentor')
        cur.execute(q,data)
        con.commit()
        cur.execute(r,join_data)
        con.commit()
        return "Mentor is created"
    else:
        return "email alraedy exist"

# def signup_university(University_Name,Department_Name,About,Email,Password):
    q="""INSERT INTO university(Join_id,University_Name,Department_Name,About,Email,Password) 
    VALUES(?,?,?,?,?,?,?,?,?);"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type) 
    VALUES(?,?,?,?);"""

    if check_email(Email):
        import bcrypt
        Password=Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),University_Name,Department_Name,About,Email,str(hashed))
        join_data=(join_id(),Email,str(hashed),'university')
        print(data)
        # cur.execute(q,data)
        # con.commit()
        # cur.execute(r,join_data)
        # con.commit()
        return "Mentor is created"
    else:
        return "email alraedy exist"
    
# print(signup_university('Utkal University','Integrated MCA','ok ok collage',"uu@gmail.com",'1234'))