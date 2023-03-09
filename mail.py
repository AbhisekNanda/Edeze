import smtplib
import random

def send_otp(rec_email,otp):
    sender_email = "skillboostmanagment@gmail.com"
    password = "kvbdyjalmrihywme"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server. login(sender_email,password)

    msg = "Your signup OTP is "
    server.sendmail(sender_email,rec_email,msg+str(otp))
    server.quit()

    return "OTP send to "+rec_email

# print(send_otp("abhiseknanda11@gmail.com",1234))