import os
import smtplib
import datetime
import yaml
from zipfile import ZipFile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st 


def send_email(toaddr, subject, body):

    fromaddr = "website@fotomo.fr"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.viaduc.fr', 587)
    server.starttls()
    server.login(fromaddr, st.secrets['email_pwd'])
    text = msg.as_string()
    print("Sending reports to", ", ".join(toaddr))
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    return 