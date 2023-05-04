import smtplib
import random

def send_otp(rec_email,otp):
    sender_email = "skillboostmanagment@gmail.com"
    password = "jkfrqqsmvtfiliyx"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server. login(sender_email,password)

    msg = "Your signup OTP is "
    server.sendmail(sender_email,rec_email,msg+str(otp))
    server.quit()

    return "OTP send to "+rec_email

# print(send_otp("abhiseknanda11@gmail.com",1234))

def enquire(rec_email,msg):
    sender_email = "skillboostmanagment@gmail.com"
    password = "jkfrqqsmvtfiliyx"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server. login(sender_email,password)

    
    server.sendmail(sender_email,rec_email,msg)
    server.sendmail(sender_email,"abhiseknanda11@gmail.com",msg)
    
    server.quit()

    return "Enquire Send"

