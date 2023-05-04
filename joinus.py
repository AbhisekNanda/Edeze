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
        return True
    else :
        return False

def signup_individual_author(First_name,Last_name,Email,Raw_Password,IDCard,About,Qualification):

    
    q="""INSERT INTO individual_author(Join_id,First_name,Last_name,Email,Password,IDCard,About,Qualification) 
    VALUES(?,?,?,?,?,?,?,?);"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type,verify) 
    VALUES(?,?,?,?,?);"""
    if check_email(Email)==False:
        import bcrypt
        Password=Raw_Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),First_name,Last_name,Email,str(hashed),IDCard,About,Qualification)
        join_data=(join_id(),Email,hashed,'individual_author',1)
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
        if result:
            print("welcome")
        else:
            print("invalid password")
        
    else:
        return "Invalid Email"
# print(login("abhiseknanda11@gmail.com","1234"))
def signup_mentor(First_Name,Last_Name,Email,Password,IDCard,Qualification,About,Session_Price):
    q="""INSERT INTO mentor(Join_id,First_name,Last_name,Email,Password,IDCard,Qualification,About,Session_Price) 
    VALUES(?,?,?,?,?,?,?,?,?)"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type,verify) 
    VALUES(?,?,?,?,?)"""

    if check_email(Email)==False:
        import bcrypt
        Password=Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),First_Name,Last_Name,Email,hashed,IDCard,Qualification,About,Session_Price)
        join_data=(join_id(),Email,hashed,'mentor',1)
        cur.execute(q,data)
        con.commit()
        cur.execute(r,join_data)
        con.commit()
        return "Mentor is created"
    else:
        return "email alraedy exist"

def signup_university(University_Name,Department_Name,About,Email,Password):
    q="""INSERT INTO university(Join_id,University_Name,Department_Name,About,Email,Password,university_document,department_document) 
    VALUES(?,?,?,?,?,?,?,?);"""
    r="""INSERT INTO join_us(Join_id,Email,Password,Type,verify) 
    VALUES(?,?,?,?,?);"""

    if check_email(Email)==False:
        import bcrypt
        Password=Password.encode()
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(Password, salt)
        data = (join_id(),University_Name,Department_Name,About,Email,str(hashed),100011,100011)
        join_data=(join_id(),Email,hashed,'university',1)
        print(data)
        cur.execute(q,data)
        con.commit()
        cur.execute(r,join_data)
        con.commit()
        return "University is created"
    else:
        return "email alraedy exist"
    
def IA_all_course(join_id):
    q="SELECT * FROM webstore WHERE Join_id=?"
    data= cur.execute(q,(join_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def createcourseid():
    for i in cur.execute("SELECT MAX(Item_id) from webstore"):
        pass
    return i[0]+1

def AddCourseWebstore(join_id,courseName,category,price,sellingPrice,description,authorName):

    q="""INSERT INTO webstore (Item_id, Course_name, Join_id,Category,Price,selling_price,Desc,Author,Rating)
    VALUES (?,?,?,?,?,?,?,?,?);"""
    data= cur.execute(q,(createcourseid(),courseName,join_id,category,price,sellingPrice,description,authorName,4)).fetchall()
    con.commit()
    return "added"

def University_all_course(join_id):
    q="SELECT * FROM training WHERE Join_id=?"
    data= cur.execute(q,(join_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def createcourseid2():
    for i in cur.execute("SELECT MAX(Course_id) from training"):
        pass
    return i[0]+1

def AddCourseTraining(join_id,courseName,category,price,sellingPrice,description,authorName,startingDate,duration):

    q="""INSERT INTO training (Course_id, Course_name, Join_id,Category,Price,selling_price,Desc,Author,Starting_date,Duration,Rating)
    VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    data= cur.execute(q,(createcourseid2(),courseName,join_id,category,price,sellingPrice,description,authorName,startingDate,duration,4)).fetchall()
    con.commit()
    return "added"

def create_joinid():
    for i in cur.execute("SELECT MAX(Join_id) from join_us"):
        pass
    return i[0]+1

def registerUniversity(join_id,UniversityName,email,password,departmentName,UniversityAccreditation,DepartmentCertification,about):
    q="""INSERT INTO university (Join_id, University_Name, Department_Name,About,Email,Password,university_document,department_document)
    VALUES (?,?,?,?,?,?,?,?);"""
    data= cur.execute(q,(join_id,UniversityName,departmentName,about,email,password,UniversityAccreditation,DepartmentCertification)).fetchall()
    con.commit()
    return "added"