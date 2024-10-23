import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config 


def send_email(recipient, subject, messsage):
    try:
        sender_email = config.EMAIL_SENDER
        sender_password = config.EMAIL_PASSWORD

        msg = MIMEMultipart()
        msg["From"] =  sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(messsage, "plain"))

        server =  smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient,text)
        server.quit()


        print("Email sent successfully.")
    except Exception as e:
        print (f"Failed to send :{str(e)}")

