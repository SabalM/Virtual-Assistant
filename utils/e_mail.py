import os
import smtplib
from email.message import EmailMessage
# from vosk import Model, KaldiRecognizer
# import pyaudio

# model_path = '/home/saugat/Desktop/mj1/vosk-model-small-en-in-0.4'
# model = Model(model_path)
# recognizer = KaldiRecognizer(model, 16000)
# mic = pyaudio.PyAudio()

# def listen():
#     stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)
    
#     print('Program is listening...')
#     audio_data = b''
    
#     while True:
#         data = stream.read(4096)
#         audio_data += data
        
#         if recognizer.AcceptWaveform(data):
#             result = recognizer.Result()[14:-3]
#             stream.stop_stream()
#             stream.close()
#             mic.terminate()
#             return result.lower()

dict = {
    'saugat': 'saugat@gmail.com',
    'neema': 'neema@gmail.com',
    'sachin': 'shashinmhrzn@gmail.com',
    'sabal': 'sabal@gmail.com'
}

def send_mail(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('shashinmhrzn@gmail.com', '')
    email = EmailMessage()
    email['from'] = "shashinmhrzn@gmail.com"
    email['to'] = receiver
    email['subject'] = subject
    email.set_content(message)
    server.send_message(email)

def main_function_code():
    print("Whom to send?")
    name = input("Enter name: ")
    print("Received name:", name)

    if name in dict:
        receiver = dict[name]
        print("What is the subject?")
        # subject = listen()
        subject = input("Enter subject: ")
        print("Received subject:", subject)

        print("What is the message?")
        # message = listen()
        message = input("Enter message: ")
        print("Received message:", message)

        send_mail(receiver, subject, message)
        print("Email is sent")
    else:
        print("Name not found in the dictionary.")

main_function_code()  # calling the main function