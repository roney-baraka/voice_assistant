import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config 


def send_email(to_address, subject, message):
    server = smtplib.SMTP(host="smt.gmail.com", port=587) 
    server.starttls()

    #Login to your emmail
    server.login(config.EMAIL_ADDRESS,config.EMAIL_PASSWORD)


    msg = MIMEMultipart()
    msg ['From'] = config.EMAIL_ADDRESS
    msg ['To'] = to_address
    msg ['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server.send_message(msg)
    server.quit()