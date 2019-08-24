import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def emailtouser(email,subject,body):
    s=smtplib.SMTP(host="smtp.gmail.com",port=587)
    s.starttls()
    s.login(os.environ['EMAIL'],os.environ['PASS'])
    message = MIMEMultipart()
    message["From"]=os.environ['EMAIL']
    message["To"]=email
    message["Subject"]=subject
    body=body
    body=MIMEText(body,"html")
    message.attach(body)
    s.sendmail(os.environ['EMAIL'],email,message.as_string())
