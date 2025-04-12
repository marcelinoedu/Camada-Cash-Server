import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings


GMAIL_USER = settings.GMAIL_USER
GMAIL_PASSWORD = settings.GMAIL_PASSWORD

def send_email(email: str, content: str, subject="Cadastro realizado com sucesso"):
    try:
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = email
        msg["Subject"] = subject

        msg.attach(MIMEText(content, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)

        print(f"E-mail enviado para {email} com sucesso!")
    
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
