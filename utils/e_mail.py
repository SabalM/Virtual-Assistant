import os
import smtplib
from email.message import EmailMessage

dict = {
    'saugat': 'saugat@gmail.com',
    'neema': 'neema@gmail.com',
    'searching': 'shashinmhrzn@gmail.com',
    'server': 'maharjansabal@gmail.com'
}

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"


bot_name = "ByteBot"

def send_mail(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('maharjansabal4@gmail.com', 'zdco oeix tuus pzna')
    email = EmailMessage()
    email['from'] = "maharjansabal4@gmail.com"
    email['to'] = receiver
    email['subject'] = subject
    email.set_content(message)
    server.send_message(email)

def email(send_mail_to,send_subject,send_message):
    name = send_mail_to
    print(f"{RED}{bot_name}{RESET}:Mail Details:-")
    print(f"{RED}{bot_name}{RESET}:Receiver name:", name)

    if name in dict:
        receiver = dict[name]
        # subject = listen()
        subject = send_subject
        print(f"{RED}{bot_name}{RESET}:Mail subject:", subject)

        # message = listen()
        message = send_message
        print(f"{RED}{bot_name}{RESET}:Mail message:", message)
        send_mail(receiver, subject, message)
        print("Email has been sent.")
        return receiver, subject, message
    else:
        print("Name not found in the dictionary.")
        # Returning None as a placeholder for error handling
        return None, None, None


# main_function_code()  # calling the main function