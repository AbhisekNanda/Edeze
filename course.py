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
    q='SELECT * FROM training WHERE Course_id=?'
    data= cur.execute(q,(Course_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def webstore_details(Item_id):
    q='SELECT * FROM webstore WHERE Item_id=?'
    data= cur.execute(q,(Item_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def search_training(s):
    q='SELECT * FROM training WHERE Course_name LIKE ? OR Desc LIKE ?'
    x='%'+s+'%'
    data= cur.execute(q,(x,x)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def search_webstore(s):
    q='SELECT * FROM webstore WHERE Course_name LIKE ? OR Desc LIKE ?'
    x='%'+s+'%'
    data= cur.execute(q,(x,x)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def search_consult(s):
    q='SELECT * FROM consult WHERE Consult_name LIKE ? OR Desc LIKE ?'
    x='%'+s+'%'
    data= cur.execute(q,(x,x)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def unique_category():
    q='SELECT DISTINCT Category FROM training '
    data= cur.execute(q).fetchall()
    con.commit()
    lst=[]
    for i in data:
        lst.append(i[0])
    return lst

def filter(course,price):
    price=int(price)
    q='SELECT * FROM training WHERE selling_price<? AND Category=?'
    data= cur.execute(q,(price,course)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def related_course(category):
    q='SELECT * FROM course_online WHERE class=1 AND Catgory=?'
    data= cur.execute(q,(category,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def create_cartid():
    for i in cur.execute("SELECT MAX(Cart_id) from training_cart"):
        pass
    return i[0]+1


def AddToCart(user_id,course_id):
    q="INSERT INTO training_cart(Cart_id,User_id,Course_id) VALUES(?,?,?)"
    data= cur.execute(q,(create_cartid(),user_id,course_id)).fetchall()
    con.commit()
    return "added"



def cart(id:int):
    # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="""SELECT training_cart.Cart_id, training_cart.User_id, training_cart.Course_id,training.Course_name,training.Price,training.selling_price
    FROM training_cart
    INNER JOIN training ON training_cart.Course_id = training.Course_id WHERE training_cart.User_id=?"""
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def total_price(id:int):
    # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="""SELECT SUM(training.selling_price) as Total_price
    FROM training_cart
    INNER JOIN training ON training_cart.Course_id = training.Course_id WHERE training_cart.User_id=?"""
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def remove_from_cart(Cart_id):
    q="DELETE FROM training_cart WHERE Cart_id=?;"
    cur.execute(q,(Cart_id,))
    con.commit()

    return "done"

def CreateOrderId():
    for i in cur.execute("SELECT MAX(id) from order_enroll"):
        pass
    return i[0]+1

def AddToOrder(User_id,Course_id,Course_name,Price,Payment_id,Order_id):
    q= ''' INSERT INTO order_enroll(id,User_id,Course_id,Course_name,Price,Payment_id,Order_id)
              VALUES(?,?,?,?,?,?,?) '''
    cur.execute(q,(CreateOrderId(),User_id,Course_id,Course_name,Price,Payment_id,Order_id))
    con.commit()

    return "added"

def ClearCart(id):
    q="DELETE FROM training_cart WHERE User_id=?"
    cur.execute(q,(id,))
    con.commit()

    return "removed"


def filterWebstore(course,price):
    price=int(price)
    q='SELECT * FROM webstore WHERE selling_price<? AND Category=?'
    data= cur.execute(q,(price,course)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def unique_category_webstore():
    q='SELECT DISTINCT Category FROM webstore '
    data= cur.execute(q).fetchall()
    con.commit()
    lst=[]
    for i in data:
        lst.append(i[0])
    return lst


def create_cartid_webstore():
    for i in cur.execute("SELECT MAX(Cart_id) from webstore_cart"):
        pass
    return i[0]+1


def AddToCartWebstore(user_id,Item_id):
    q="INSERT INTO webstore_cart(Cart_id,User_id,Item_id) VALUES(?,?,?)"
    data= cur.execute(q,(create_cartid_webstore(),user_id,Item_id)).fetchall()
    con.commit()
    return "added"

def cartWebstore(id:int):
    # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="""SELECT webstore_cart.Cart_id, webstore_cart.User_id, webstore_cart.Item_id,webstore.Course_name,webstore.Price,webstore.selling_price
    FROM webstore_cart
    INNER JOIN webstore ON webstore_cart.Item_id = webstore.Item_id WHERE webstore_cart.User_id=?"""
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json



def remove_from_cart_webstore(Cart_id):
    q="DELETE FROM webstore_cart WHERE Cart_id=?;"
    cur.execute(q,(Cart_id,))
    con.commit()

    return "done"

def total_price_webstore(id:int):
    # q="SELECT * FROM training_cart WHERE User_id = ?"
    q="""SELECT SUM(webstore.selling_price) as Total_price
    FROM webstore_cart
    INNER JOIN webstore ON webstore_cart.Item_id = webstore.Item_id WHERE webstore_cart.User_id=?"""
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def CreateOrderIdWebstore():
    for i in cur.execute("SELECT MAX(id) from order_webstore"):
        pass
    return i[0]+1

def AddToOrderWebstore(User_id,Item_id,Course_name,Price,Payment_id,Order_id):
    q= ''' INSERT INTO order_webstore(id,User_id,Item_id,Course_name,Price,Payment_id,Order_id)
              VALUES(?,?,?,?,?,?,?) '''
    cur.execute(q,(CreateOrderIdWebstore(),User_id,Item_id,Course_name,Price,Payment_id,Order_id))
    con.commit()

    return "added"

def ClearCartWebstore(id):
    q="DELETE FROM webstore_cart WHERE User_id=?"
    cur.execute(q,(id,))
    con.commit()

    return "removed"

def webstore_details(Course_id):
    q='SELECT * FROM webstore WHERE Item_id=?'
    data= cur.execute(q,(Course_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json




def AddToEnroll(user_id,item_id):

    # data=webstore_details(id)
    # data_json=json.loads(data)

    q= ''' INSERT INTO enroll(User_id,Item_id)
              VALUES(?,?) '''
    cur.execute(q,(user_id,item_id))
    con.commit()

    return "added"

##########################################################
############## consulting ################################

def consulting():
    q='SELECT * FROM consult'
    data= cur.execute(q).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def consulting_details(Cons_id):
    q='SELECT * FROM consult WHERE Cons_id=?'
    data= cur.execute(q,(Cons_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def filterconsulting(course,price):
    price=int(price)
    q='SELECT * FROM consult WHERE Price <? AND Category=?'
    data= cur.execute(q,(price,course)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def unique_category_consulting():
    q='SELECT DISTINCT Category FROM consult '
    data= cur.execute(q).fetchall()
    con.commit()
    lst=[]
    for i in data:
        lst.append(i[0])
    return lst



def allorderenroll(id):
    
    q='SELECT * FROM order_enroll where User_id=?'
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def allorderwebstore(id):
    
    q='SELECT * FROM order_webstore where User_id=?'
    data= cur.execute(q,(id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

def order_details_enroll(Order_id):

    q="""SELECT order_enroll.Course_name,training.Price,training.selling_price,order_enroll.Course_id,order_enroll.Order_id,order_enroll.Price as p
    FROM order_enroll
    INNER JOIN training ON training.Course_id = order_enroll.Course_id WHERE order_enroll.Order_id=?"""

    
    data= cur.execute(q,(Order_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

# print(order_details_enroll("order_LgYZ1GcyAmZ7od"))

def order_details_enroll_price(Order_id):
    q="""SELECT sum(training.selling_price) as p
    FROM order_enroll
    INNER JOIN training ON training.Course_id = order_enroll.Course_id WHERE order_enroll.Order_id=?"""

    data= cur.execute(q,(Order_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json

# print(order_details_enroll_price("order_LgYZ1GcyAmZ7od"))

def allmycourse(user_id):

    q="""SELECT webstore.Course_name,webstore.Item_id
    FROM enroll
    INNER JOIN webstore ON webstore.Item_id = enroll.Item_id WHERE enroll.User_id=?"""

    data= cur.execute(q,(user_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json
    
def user_first_name(user_id):
    q="SELECT First_name FROM user WHERE User_id=?"

    data= cur.execute(q,(user_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data[0][0]

def price_of_course(course_id):
    q="SELECT selling_price FROM training WHERE Course_id=?"
    data= cur.execute(q,(course_id,)).fetchall()
    con.commit()
    return data[0][0]

def training(course_id):
    q="SELECT * FROM training WHERE course_id=?"

    data= cur.execute(q,(course_id,)).fetchall()
    con.commit()
    data_json = json.dumps([dict(ix) for ix in data ],separators=(',', ':'))
    return data_json