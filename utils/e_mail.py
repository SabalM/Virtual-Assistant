import os
import smtplib
from email.message import EmailMessage
import json
from dotenv import load_dotenv

load_dotenv()

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"

bot_name = "ByteBot"

def send_mail(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    email_address = os.getenv('EMAIL_ADDRESS')
    email_secret_key = os.getenv('EMAIL_KEY')
    server.login(email_address, email_secret_key)
    email = EmailMessage()
    email['from'] = email_address
    email['to'] = receiver
    email['subject'] = subject
    email.set_content(message)
    server.send_message(email)

def email(send_mail_to, send_subject, send_message):
    name = send_mail_to
    print(f"{RED}{bot_name}{RESET}:Mail Details:-")
    print(f"{RED}{bot_name}{RESET}:Receiver name:", name)

    with open('data_archive/emails.json') as f:
        emails_dict = json.load(f)

    if name in emails_dict:
        receiver = emails_dict[name]
        subject = send_subject
        print(f"{RED}{bot_name}{RESET}:Mail subject:", subject)
        message = send_message
        print(f"{RED}{bot_name}{RESET}:Mail message:", message)
        send_mail(receiver, subject, message)
        print("Email has been sent.")
        return receiver, subject, message
    else:
        print("Name not found in the dictionary.")
        # Returning None as a placeholder for error handling
        return None, None, None

