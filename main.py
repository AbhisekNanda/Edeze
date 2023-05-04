from fastapi import FastAPI,Body,Request,Form,File,UploadFile
from starlette.responses import RedirectResponse, Response
import user
import joinus
import database
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import base64
import starlette.status as status
import shutil


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

   
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request })


@app.post('/Profile')
async def login(request:Request):
    form_data = await request.form()
    
    data=database.login(form_data["email"],form_data["password"])
    
    import json
    data1=json.loads(data)
    print(data1)
    if data1["status"] == "login":
        if data1["type"] == "user":
            data = database.course()
            import json
            final_data=json.loads(data)
            import course
            lst=course.unique_category()
            print("ok",lst)
            name=course.user_first_name(data1['User_id'])
            print("ooo",lst)
            url="/"+str(data1['User_id'])+"/home"
            return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)
            # return templates.TemplateResponse("training.html",{"request": request ,"datas":final_data,"filt1":lst,"id":data1['User_id'],"name":name})
        elif data1["type"] == "mentor":
            if data1["verify"]==0:
                import mentor
                cons=mentor.myconsult(data1["joinus_id"])
                return templates.TemplateResponse("mentor-profile.html",{"request": request ,"cons":json.loads(cons), "id": data1["joinus_id"]})
            else:
                return "not verified"
        elif data1["type"]=="individual_author":
            if data1["verify"]==0:
                url="/"+str(data1["joinus_id"])+"/IA"
                return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)
            else:
                return "not verified"
        
        else:
            if data1["verify"]==0:
                url="/"+str(data1["joinus_id"])+"/University"
                return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)
            else:
                return "not verified"
                
    elif data1["status"] == "User is deactivated" :
        return "User is deactivated"
    else:
        return data1
    

@app.get('/{id}/home')
def home(request:Request,id):
    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("home.html",{"request": request,"id":id ,"name":name})

@app.get('/display_login')
def display_login(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

class signup(BaseModel):
    First_name: str
    Second_name: str
    Email: str
    Password: str

@app.post('/signup')
def signup(data: signup):
    #status 1- deactivate 0- activate -1-block
    status = database.signup(data.First_name,data.Second_name,data.Email,data.Password,1)
    return {"status":status}

class sendotp(BaseModel):
    email: str

@app.post('/sendotp')
def send_otp(data: sendotp):
    status = database.create_otp(data.email)
    return {"status":status}

@app.post('/verifyotp')
def send_otp(email,otp):
    status = database.verify_otp(email,otp)
    return {"status":status}

@app.get('/Course')
def course(request: Request):
    data = database.course()
    import json
    final_data=json.loads(data)
    import course
    lst=course.unique_category()
    
    return templates.TemplateResponse("training.html",{"request": request ,"datas":final_data,"filt1":lst,"noid":1})

@app.get('/{id}/Course')
def course(request: Request,id:int):
    data = database.course()
    import json
    final_data=json.loads(data)
    import course
    lst=course.unique_category()

    import course
    name=course.user_first_name(id)
    
    return templates.TemplateResponse("training.html",{"request": request ,"datas":final_data,"filt1":lst,"id":id,"name":name})

@app.get('/Mentor')
def course():
    data = database.mentor()
    import json
    final_data=json.loads(data)
    return final_data

class MyCourse(BaseModel):
    id : int

class MyMentor(BaseModel):
    id : int

@app.post('/MyMentor')
def id_mentor(data : MyMentor):
    data= user.user_mentor(data.id)
    import json
    final_data=json.loads(data)
    return final_data

class BuyMentor(BaseModel):
    userid : int
    joinid : int

@app.post('/BuyMentor')
def EnrollMentor(data : BuyMentor):
    data= user.buy_mentor(data.userid,data.joinid)
    return {'status':data}

class BuyCourse(BaseModel):
    userid : int
    courseid : int

@app.post('/BuyCourse')
def EnrollMentor(data : BuyCourse):
    data= user.buy_course(data.userid,data.courseid)
    return {'status':data}

@app.post('/joinus/Individual_Author')
async def joinus(request:Request):
    #First_name,Last_name,Email,Raw_Password,IDCard,About,Qualification
    data= await request.form()
    import joinus
    data=joinus.signup_individual_author(data["firstName"],data["lastName"],data["email"],data["password"],1000111,data["about"],1000011)
    url="/display_login"

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.post('/joinus/Mentor')
async def mentor(request:Request):
    #First_Name,Last_Name,Email,Password,IDCard,Qualification,About,Session_Price
    data= await request.form()
    import joinus
    data=joinus.signup_mentor(data["firstName"],data["lastName"],data["email"],data["password"],1000111,10001111,data["price"],data["about"])
    url="/display_login"

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.post('/addcourse')
def addcourse(Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration):
    import course
    data=course.AddCouse(Course_name,Join_id,Catgory,Price_enroll,Price_course,Desc,Author,Rating,Date,classs,Pendrive,cd,Type,Start_date,Duration)
    return {'status':data}

@app.post('/joinus/University')
async def University(request:Request):
    #University_Name,Department_Name,About,Email,Password
    data=await request.form()
    import joinus
    data=joinus.signup_university(data["UniversityName"],data["departmentName"],data["about"],data["email"],data["password"])
    
    url="/display_login"

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.get('/{id}/blockuser')
def blockUser(id:int):
    import user
    data1 = user.block_user(id)
    import json
    return RedirectResponse('/AdminUserStatus')


@app.get('/{id}/activateuser')
def blockUser(id:int):
    import user
    data1 = user.activate_user(id)
    import json
    return RedirectResponse('/AdminUserStatus')



@app.get('/{id}/deactivateuser')
def blockUser(id:int):
    import user
    data1 = user.deactivate_user(id)
    import json
    return RedirectResponse('/AdminUserStatus')

@app.get('/{join_id}/verify')
def blockUser(join_id:int):
    import admin
    data1 = admin.verify(join_id)
    import json
    return RedirectResponse('/adminverifyjoinus')

@app.get('/alluser')
def user():
    import user
    data1 = user.user()
    import json
    return json.loads(data1)

@app.get('/webstore')
def webstore(request: Request):
    import database
    data1 = database.webstore()
    import json
    return templates.TemplateResponse("webstore.html",{"request": request ,"datas":json.loads(data1)})




@app.get('/ok')
def ok(request: Request):
    
    return templates.TemplateResponse("cart.html",{"request": request})



@app.post("/{id}/filter")
async def example(request: Request,id:int):
    form_data = await request.form()
    import course
    data1 = course.filter(form_data['course'],form_data['price'])
    lst=course.unique_category()
    
    import json
    print(json.loads(data1))
    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("training.html",{"request": request ,"datas":json.loads(data1),"filt1":lst,"id":id,"name":name})
    # return json.loads(data1)

@app.post("/exmple")
def exmple():
    return "hi"

# @app.get('/cart/{user_id}/{course_id}')
# def training_cart(request: Request ,user_id :int , course_id : int):
#     import course
#     data=course.AddToCart(user_id,course_id)

#     import course
#     data1 = course.cart(id)
#     import json
#     data2=json.loads(data1)
    
#     return templates.TemplateResponse("cart.html",{"request": request ,"id":user_id,"data":data2})
    
@app.get('/cart/{user_id}/{course_id}')
def mycart(request: Request,user_id :int , course_id : int):
    import course
    data=course.AddToCart(user_id,course_id)
    url="/"+str(user_id)+"/cart"
    return RedirectResponse(url)

@app.get('/{user_id}/cart')
def cart(request:Request ,user_id):

    import course
    data1 = course.cart(user_id)
    import json
    data2=json.loads(data1)
    
    import course
    data3 = course.total_price(str(user_id))
    total_price=json.loads(data3)

    import course
    ws_data = course.cartWebstore(user_id)
    data_ws=json.loads(ws_data)
    ws_amount=course.total_price_webstore(user_id)
    amount_ws=json.loads(ws_amount)

    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))
    # pay=(total_price[0]["Total_price"])*100
    pay=100
    data5 = { "amount": pay , "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data5)

    import course
    name=course.user_first_name(user_id)
    # return total_price
    return templates.TemplateResponse("cart.html",{"request": request ,"id":user_id,"datas":data2,"t":total_price,"payment":payment,"ws_data":data_ws,"amount_ws":amount_ws,"name":name})

@app.get('/{cart_id}/RemoveFromCart/{user_id}')
def removefromcart(request:Request ,cart_id:int ,user_id: int):

    import course
    data1=course.remove_from_cart(cart_id)

    url="/"+str(user_id)+"/cart"
    return RedirectResponse(url)

# @app.get('/pay')
# def pay(request:Request):
#     import razorpay
#     client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))

#     data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
#     payment = client.order.create(data=data)
#     print(payment)
#     print(payment['id'])

    return templates.TemplateResponse("paymentDemo.html",{"request": request ,"payment":payment})

@app.get('/trainingdetails/{user_id}/{id}')
def trainig_details(request: Request,user_id ,id :str):
    import course
    data1 = course.course_details(id)
    import json
    data=json.loads(data1)
    # related_course=course.related_course(data[0]["Category"])
    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))

    data2 = { "amount": data[0]["selling_price"], "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data2)
    #,"rels":json.loads(related_course)
    # return payment

    import course
    name=course.user_first_name(user_id)
    return templates.TemplateResponse("training-detail.html",{"request": request ,"datas":data,"id":user_id,"payment":payment,"name":name})

@app.get('/AddOrder/{id}/{Order_id}/{Payment_id}')
def AddOrder(request: Request,id ,Order_id,Payment_id):
    import course
    data=course.cart(id)
    import json
    data_josn= json.loads(data)
    for i in data_josn:
        res = course.AddToOrder(id,i["Course_id"],i["Course_name"],i["Price"],Payment_id,Order_id)

    res1=course.ClearCart(id)
    
    url="/"+str(id)+"/Course"
    return RedirectResponse(url)

@app.get('/{id}/webstore')
def webstore(request: Request, id :int):
    import database
    data1 = database.webstore()
    import course
    lst=course.unique_category_webstore()
    import json
    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("webstore.html",{"request": request ,"datas":json.loads(data1), "id":id,"filt1":lst,"name":name})

@app.post("/{id}/filterWebstore")
async def example(request: Request,id:int):
    form_data = await request.form()
    import course
    data1 = course.filterWebstore(form_data['course'],form_data['price'])
    lst=course.unique_category_webstore()
    import json
    print(json.loads(data1))
    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("webstore.html",{"request": request ,"datas":json.loads(data1),"filt1":lst,"id":id,"name":name})

@app.get('/paywebstoredetails/{id}/{item_id}')
def paywebstore(request:Request,id,item_id):

    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))
    #data[0]["selling_price"]
    data2 = { "amount": 10000, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data2)

    return templates.TemplateResponse("webstore-pay-details.html",{"request": request,"payment":payment })

@app.get('/cartwebstore/{user_id}/{Item_id}')
def mycart(request: Request,user_id :int , Item_id : int):
    import course
    data=course.AddToCartWebstore(user_id,Item_id)
    url="/"+str(user_id)+"/cart"
    return RedirectResponse(url)

@app.get('/{cart_id}/RemoveFromCartWebstore/{user_id}')
def removefromcart(request:Request ,cart_id:int ,user_id: int):

    import course
    data1=course.remove_from_cart_webstore(cart_id)

    url="/"+str(user_id)+"/cart"
    return RedirectResponse(url)


@app.get('/paywebstore/{user_id}')
def pay(request:Request,user_id):
    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))
    import course
    ws_amount=course.total_price_webstore(user_id)
    amount_ws=json.loads(ws_amount)
    print(amount_ws)
    if amount_ws[0]['Total_price'] == None:
        print("okey")
        amt=0
        url="/"+str(id)+"/cart"
        return RedirectResponse(url)
    else:
        data = { "amount": amount_ws[0]['Total_price']*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print("hi")
        return templates.TemplateResponse("paymentDemo.html",{"request": request ,"id":user_id,"payment":payment})
    
@app.get('/paytraining/{user_id}/{course_id}')
def pay(request:Request,user_id,course_id):
    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))
    import course
    amount=course.price_of_course(course_id)
    data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    print("hi")
    return templates.TemplateResponse("paytraining.html",{"request": request ,"id":user_id,"payment":payment,"course_id":course_id})

@app.get('/AddToEnrollWebstore/{id}/{course_id}/{Order_id}/{Payment_id}')
def AddToEnrollWebstore(request:Request,id,course_id,Order_id,Payment_id):
    import course
    data=json.loads(course.webstore_details(course_id))
    res = course.AddToOrderWebstore(id,data[0]["Item_id"],data[0]["Course_name"],data["Price"],Payment_id,Order_id)
    res2=course.AddToEnroll(id,data[0]["Item_id"])

    url="/"+str(id)+"/webstore"

    return RedirectResponse(url)

@app.get('/AddToOrderHistory/{id}/{Order_id}/{Payment_id}')
def AddToOrderHistory(request:Request,id,Order_id,Payment_id):
    import course
    data=json.loads(course.training())
    
@app.get('/AddOrderWebstore/{id}/{Order_id}/{Payment_id}')
def AddOrder(request: Request,id ,Order_id,Payment_id):
    import course
    data=course.cartWebstore(id)
    import json
    data_josn= json.loads(data)
    for i in data_josn:
        res = course.AddToOrderWebstore(id,i["Item_id"],i["Course_name"],i["Price"],Payment_id,Order_id)
        res2=course.AddToEnroll(id,i["Item_id"])

    res1=course.ClearCartWebstore(id)
    
    
    url="/"+str(id)+"/webstore"
    return RedirectResponse(url)

@app.get('/webstoredetails/{userid}/{itemid}')
def webstoredetails(request:Request,userid,itemid):

    import course
    ws=course.webstore_details(itemid)
    ws1=json.loads(ws)
    import course
    name=course.user_first_name(userid)
    return templates.TemplateResponse("webstore-clicked.html",{"request": request ,"id":userid ,"ws":ws1,"name":name})

@app.get('/AddToEnroll/{id}/{{Item_id}}/{Order_id}/{Payment_id}')
def AddToEnroll(request:Request,id,Item_id,Order_id,Payment_id):
    import course
    data=course.webstore_details(Item_id)
    
    import json
    data_josn= json.loads(data)
    # return data_josn
    
    res = course.AddToOrderWebstore(id,data_josn[0]["Item_id"],data_josn[0]["Course_name"],data_josn[0]["Price"],Payment_id,Order_id)
    res2=course.AddToEnroll(id,data_josn[0]["Item_id"])
    url="/webstoredetails/"+id+"/"+Item_id
    return RedirectResponse(url)

@app.get('/{id}/consulting')
def consulting(request:Request,id):

    import course
    cons=course.consulting()
    cons_json=json.loads(cons)
    lst1=course.unique_category_consulting()

    import course
    name=course.user_first_name(id)

    return templates.TemplateResponse("consulting.html",{"request": request,"cons":cons_json,"id":id,"filt1":lst1,"name":name})

@app.get('/consultingdetails/{user_id}/{cons_id}')
def consultingdetails(request:Request,user_id,cons_id):

    import course
    cons=course.consulting_details(cons_id)
    cons_json = json.loads(cons)
    lst=course.unique_category_consulting()
    print(lst)
    import course
    name=course.user_first_name(user_id)
    
    return templates.TemplateResponse("consulting-detail.html",{"request": request, "co":cons_json,"id":user_id,"filt1":lst,"name":name})

@app.post("/{user_id}/filterConsulting")
async def example(request: Request,user_id:int):
    form_data = await request.form()

    import course
    cons = course.filterconsulting(form_data['course'],form_data['price'])
    cons_json = json.loads(cons)
    lst1=course.unique_category_consulting()
    print(lst1)
    print(cons_json)

    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("consulting.html",{"request": request, "cons":cons_json,"filt1":lst1,"id":user_id,"name":name})

@app.get('/{id}/OrderHistory')
def orderhistory(request:Request ,id):

    import course
    oe=course.allorderenroll(id)
    oe_json=json.loads(oe)

    ow=course.allorderwebstore(id)
    ow_json=json.loads(ow)

    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("order-history.html",{"request": request, "oes":oe_json,"ows":ow_json,"id":id,"name":name})

@app.get('/{id}/OrderDetails/{Order_id}')
def orderdetails(request:Request,id,Order_id):
    
    import course
    ord=course.order_details_enroll(Order_id)
    price_ord=course.order_details_enroll_price(Order_id)

    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("order-details.html",{"request": request,"order_id":Order_id,"ords":json.loads(ord),"price_ord":json.loads(price_ord),"id":id,"name":name})

@app.get('/{id}/MyCourse')
def mycourse(request:Request,id):
    import course
    mycrs=course.allmycourse(id)
    import course
    name=course.user_first_name(id)
    return templates.TemplateResponse("video-gallery.html",{"request":request,"mycrs":json.loads(mycrs),"name":name,"id":id})

# @app.get('/{Join_id}/MentorProfile')
# def mentorprofile(request:Request,Join_id):

#     import course

#     return templates.TemplateResponse("mentor-profile.html",{"request":request})

class AddConsult(BaseModel):
    join_id : int
    Consult_name : str
    Category : str
    Price : str
    DESC : str
    Author : str

@app.post('/AddConsult')
async def AddConsult(request:Request,data:AddConsult):
    # form_data = await request.form()
    
    import mentor
    add=mentor.AddConuslting(data.join_id,data.Consult_name,data.Category,data.Price,data.DESC,data.Author)

    return add

# @app.get('')
# def register(request:Request):

#     return templates.TemplateResponse("register.html",{"request":Request})

@app.get('/Register')
def mycourse(request:Request):
    # import course
    # mycrs=course.allmycourse(id)
    return templates.TemplateResponse("register.html",{"request":request})


@app.get('/joinus')
def joinus(request:Request):

    return templates.TemplateResponse("joinus.html",{"request":request})

@app.get('/MentorRegister')
def mentorregister(request:Request):

    return templates.TemplateResponse("mentor-registration.html",{"request":request})

# class AddConsult(BaseModel):
#     First_name : str
#     Last_name : str
#     Email : str
#     Password : str
#     idcard : File
#     Qualification : File
#     About : str

@app.post('/RegisterMentor')
async def RegisterMentor(email:str = Form(...),password:str =Form(...),firstName:str = Form(...),lastName:str = Form(...),uploadID:UploadFile = Form(...),uploadQualification:UploadFile = Form(...),price:int = Form(...),about:str = Form(...)):
    # x= await file.read()
    return "ok"

@app.get('/{q}/search')
def search(request:Request,q):
    import course
    ta = course.search_training(q)
    wb = course.search_webstore(q)
    cons = course.search_consult(q)
    
    import json
    final_ta=json.loads(ta)
    final_wb=json.loads(wb)
    final_cons=json.loads(cons)

    return templates.TemplateResponse("search-result.html",{"request":request,"tas":final_ta,"wbs":final_wb,"cons":final_cons})

class Enquire(BaseModel):
    Full_name : str
    Email : str
    Telephone : str
    Query : str

@app.post('/{id}/{course_id}/enquiretrainingdetails')
async def enquire(request:Request,id,course_id):
    data = await request.form()
    print(data["email"])
    msg=data["full_name"]+"\n"+data["email"]+"\n"+data["telephone"]+"\n"+data["Query"]
    
    import mail
    x=mail.enquire("nandaabhisek31@gmail.com",msg)
    url="/trainingdetails/"+id+"/"+course_id

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.post('/{id}/{Cons_id}/enquireconsultingdetails')
async def enquire(request:Request,id,Cons_id):
    data = await request.form()
    print(data)
    msg=data["full_name"]+"\n"+data["email"]+"\n"+data["telephone"]+"\n"+data["subject"]+"\n"+data["Query"]
    
    import mail
    x=mail.enquire("nandaabhisek31@gmail.com",msg)
    url="/consultingdetails/"+id+"/"+Cons_id

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.post('/{id}/{Item_id}/enquirewebstoredetails')
async def enquire(request:Request,id,Item_id):
    data = await request.form()
    print(data)
    msg=data["full_name"]+"\n"+data["email"]+"\n"+data["telephone"]+"\n"+data["subject"]+"\n"+data["Query"]
    
    import mail
    x=mail.enquire("nandaabhisek31@gmail.com",msg)
    url="/webstoredetails/"+id+"/"+Item_id

    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

# @app.get('/{Full_name}/{Email}/{Telephone}/{Query}/enquire')
# def enquire(request:Request,Full_name:str,Email:str,Telephone:str,Query:str):
#     msg=Full_name+"\n"+Email+"\n"+Telephone+"\n"+Query
#     import mail
#     x=mail.enquire("bikashkumarnayak807@gmail.com",msg)

#     return RedirectResponse

@app.get('/{cart_id}/RemoveFromCartWebstore/{user_id}')
def removefromcart(request:Request ,cart_id:int ,user_id: int):

    import course
    data1=course.remove_from_cart_webstore(cart_id)

    url="/"+str(user_id)+"/cart"
    return RedirectResponse(url)


@app.get('/paytrainingdetails/{user_id}/{item_id}')
def pay(request:Request,user_id,item_id):
    import razorpay
    client = razorpay.Client(auth=("rzp_test_kElfgGUB6qKo1e", "P6Myq5EUWcBCOwsYzv2FAGg5"))
    import course
    amount=(course.price_of_course(item_id))*100
    
    data2 = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data2)
    
    print("hi")
    return templates.TemplateResponse("training-details-pay.html",{"request": request ,"id":user_id,"payment":payment,"Item_id":item_id})

@app.get('/AddOrdertrainingdetails/{id}/{Order_id}/{Payment_id}')
def AddOrder(request: Request,id ,Order_id,Payment_id):
    import course
    data=course.cartWebstore(id)
    import json
    data_josn= json.loads(data)
    for i in data_josn:
        res = course.AddToOrderWebstore(id,i["Item_id"],i["Course_name"],i["Price"],Payment_id,Order_id)
        res2=course.AddToEnroll(id,i["Item_id"])

    res1=course.ClearCartWebstore(id)
    
    
    url="/"+str(id)+"/webstore"
    return RedirectResponse(url)

@app.get('/aboutus')
def removefromcart(request:Request):

    return templates.TemplateResponse("about_us_page.html",{"request": request })

@app.get('/ourteam')
def removefromcart(request:Request):

    return templates.TemplateResponse("our_team_page.html",{"request": request })




############################ Admin ####################################
#######################################################################

@app.get('/admin')
def admin(request:Request):
    import admin
    t_user=admin.total_user()
    t_mentor=admin.total_mentor()
    t_university=admin.total_university()
    t_ia = admin.total_ia()

    import json
    recent_order=admin.recent_order()
    rec_json=json.loads(recent_order)

    user=admin.all_user()
    user_json=json.loads(user)

    return templates.TemplateResponse("admin(home).html",{"request":request,"t_user":t_user,"t_mentor":t_mentor,"t_university":t_university,"t_ia":t_ia,"recs":rec_json,"users":user_json})

@app.get('/AdminUserStatus')
def userstatus(request:Request):

    import admin
    user=admin.all_user()
    user_json=json.loads(user)

    return templates.TemplateResponse("admin(user-status).html",{"request":request,"users":user_json})

@app.get('/adminverifyjoinus')
def verifyjoinus(request:Request):
    import admin
    IA=json.loads(admin.verifyIA())
    mentor=json.loads(admin.verifymentor())
    university=json.loads(admin.verifyuni())
    return templates.TemplateResponse("admin(verify-service-providers).html",{"request":request , "datas":IA,"ments":mentor,"unis":university})

@app.get('/adminorderhistory')
def orderhistory(request:Request):
    import admin
    orders=admin.recent_order()
    orders_json=json.loads(orders)
    return templates.TemplateResponse("admin(order-history).html",{"request":request,"ords":orders_json})

@app.get('/AdminAllCourse')
def allcourse(request:Request):

    import admin
    hists=admin.all_course()
    import json
    hists_json=json.loads(hists)
    web=admin.all_course_webstore()
    import json
    web_json=json.loads(web)
    mentor=admin.all_course_mentor()
    mentor_json=json.loads(mentor)
    return templates.TemplateResponse("admin(all-course).html",{"request":request,"hists":hists_json,"webs":web_json,"ments":mentor_json})



@app.get("/video/{Item_id}/{video_id}")
def video(request:Request,Item_id,video_id):

    
    import video
    x=json.loads(video.x(Item_id,video_id))
    videos=json.loads(video.videosall(Item_id))
    print("ok")
    print(video)
    
    return templates.TemplateResponse("video-player.html",{"request":request,"videos":videos,"vido":x,"Item_id":Item_id})


############################## joinus profile ######################
####################################################################

@app.get('/{join_id}/IA')
def IA(request:Request,join_id):
    import joinus
    course=json.loads(joinus.IA_all_course(join_id))
    
    return templates.TemplateResponse("individual-profile.html",{"request":request,"course":course,"id":join_id})

@app.post('/{join_id}/AddCourseWebstore')
async def AddCourseWebstore(request:Request,join_id):
    data = await request.form()
    print(data["courseName"])
    import joinus
    x=joinus.AddCourseWebstore(join_id,data["courseName"],data["category"],data["price"],data["sellingPrice"],data["description"],data["authorName"])
    
    url="/"+str(join_id)+"/IA"
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)

@app.get('/{join_id}/University')
def IA(request:Request,join_id):
    import joinus
    course=json.loads(joinus.University_all_course(join_id))
    print(course)
    return templates.TemplateResponse("university-profile.html",{"request":request,"course":course,"id":join_id})

@app.post('/{join_id}/AddCourseTraining')
async def AddCourseTraining(request:Request,join_id):
    data = await request.form()
    print(data)
    import joinus
    x=joinus.AddCourseTraining(join_id,data["courseName"],data["category"],data["price"],data["sellingPrice"],data["description"],data["authorName"],data["startingDate"],data["duration"])
    
    url="/"+str(join_id)+"/University"
    return RedirectResponse(url,status_code=status.HTTP_303_SEE_OTHER)


############################### JOINUS REGISTATION ##############################
#################################################################################

@app.get('/registerUniversity')
def reguni(request:Request):

    return templates.TemplateResponse("university-registration.html",{"request":request})

@app.post('/UniversityRegister')
async def UniversityRegister(request:Request):
    data= await request.form()
    import joinus
    # join_id=joinus.create_joinid()
    join_id=4

    # data["UniversityAccreditation"].filename=join_id\

    with open(data["UniversityAccreditation"].filename, "wb") as buffer:
        shutil.copyfileobj(data["UniversityAccreditation"].file, buffer)
    buffer.close()
    import os
    ext=((data["UniversityAccreditation"].filename).split("."))[1]
    new_name=str(join_id)+"."+ext
    os.rename(data["UniversityAccreditation"].filename, str(join_id)+"."+ext)
    scr="C:/Users/chint/OneDrive/Desktop/edeze full project/Edeze"+"/"+new_name
    desc="C:/Users/chint/OneDrive/Desktop/edeze full project/Edeze/static/UniAcc/"+new_name
    shutil.move(scr, desc)




    # with open(data["DepartmentCertification"].filename, "wb") as buffer:
    #     shutil.copyfileobj(data["DepartmentCertification"].file, buffer)
    # buffer.close()
    # import os
    # ext=((data["DepartmentCertification"].filename).split("."))[1]
    new_name1=str(join_id)+"cert"+"."+ext
    # os.rename(data["DepartmentCertification"].filename, new_name1)
    # scr="C:/Users/chint/OneDrive/Desktop/edeze full project/Edeze"+"/"+new_name1
    # desc="C:/Users/chint/OneDrive/Desktop/edeze full project/Edeze/static/UniCerf/"+new_name1
    # shutil.move(scr, desc)

    UniversityAccreditation = "/static/UniAcc/"+new_name
    DepartmentCertification = "/static/UniCerf/"+new_name1

    x=joinus.registerUniversity(join_id,data['UniversityName'],data["email"],data["password"],data["departmentName"],UniversityAccreditation,DepartmentCertification,data["about"])


    print(data)

    return "hi"

@app.get('/registerIA')
def reguni(request:Request):

    return templates.TemplateResponse("individual-registration.html",{"request":request})

@app.get('/registerMentor')
def reguni(request:Request):

    return templates.TemplateResponse("mentor-registration.html",{"request":request})

@app.get('/contactus')
def contactus(request:Request):

    return templates.TemplateResponse("contactus.html",{"request":request})

@app.get("/forgotpassword")
def forgetpassword(request:Request):

    return templates.TemplateResponse("forgot-pass.html",{"request":request})
