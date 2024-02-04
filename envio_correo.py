import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

remitente = os.getenv('USER')
destinatario = 'Alvaroandres1829@hotmail.com'
asunto = 'Test'

msg = MIMEMultipart()
msg['Subject'] = asunto
msg['From'] = remitente
msg['To'] = destinatario

with open('email.html','r') as archivo:
    html = archivo.read()

#Adjuntar contenido HTML
msg.attach(MIMEText(html,'html'))

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(remitente,os.getenv('PASS'))

server.sendmail(remitente,
                destinatario,
                msg.as_string())
server.quit()