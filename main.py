import torch
import os
import json
import random

# import Speech Engine
from engine import *

# import Intent
from neuralnet.model import IntentModelClassifier
from neuralnet.nltk_utils import bag_of_words, tokenize

# import task automation functions
from utils.app_handler import *
from utils.weather import *
from utils.online_surf import *
from utils.device_control import *
from utils.application import *
from utils.volume_control import ActionHandler
from utils.brightness_control import BrightnessController


# Instantiate ActionHandler for volume control
action_handler = ActionHandler()

# Instantiate BrightnessController for brightness control
brightness_controller = BrightnessController()

# Load API keys from .env
from dotenv import load_dotenv
load_dotenv()

# Loading Application Paths JSON file 
with open('utils/app_paths.json', 'r') as f:
    application_paths = json.load(f)

# Setting device agnostic code
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loaded model on: {device}")

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

""" Load Intent_Classifier Trained Model """
MODEL_SAVE_PATH = "model/intent.pth"
model_info = torch.load(MODEL_SAVE_PATH)

input_size = model_info["input_size"]
hidden_size = model_info["hidden_size"]
output_size = model_info["output_size"]
all_words = model_info["all_words"]
tags = model_info["tags"]
model_state = model_info["model_state"]

# Instantiate IntentModelClassifier
model = IntentModelClassifier(
    input_size,
    hidden_size,
    output_size).to(device)

model.load_state_dict(model_state)
model.eval()


# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"


bot_name = "ByteBot"
recognizer, mic, stream = initialize_model()
print("-"*50)
print(f"{GREEN}Welcome to ByteBot!{RESET}\n{BLUE}To exit, simply say {RED}'quit'{BLUE}.\n{GREEN}Speech Recognition{BLUE} is now initialized.{RESET}")
print("-"*50)

while True:
    # sentence = input(f"{GREEN}You{RESET}: ")
    sentence = speech_recognize(recognizer, stream)
    print(f"{GREEN}You{RESET}: {sentence}")
    if sentence == "quit":
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    # print(X.shape[0])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    # print(f"Bot: {bot_name}, {tag}")

    # Assigns all proabability in range [0, 1]
    probs = torch.softmax(output, dim=1)
    prob = probs[0, predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                response = random.choice(intent['responses'])

                # Create Folder
                if tag == "Create":
                    # print(user_input)
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = speech_recognize(recognizer, stream)
                    print(f"{BLUE}Folder name: {RESET}{folder_name}")
                    create_folder(folder_name)

                # Delete Folder
                elif tag == "Delete":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = speech_recognize(recognizer, stream)
                    print(f"{BLUE}Folder name: {RESET}{folder_name}")
                    delete_folder(folder_name)
                
                # Rename Folder
                elif tag == "Rename":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    old_folder_name = speech_recognize(recognizer, stream)
                    print(f"{BLUE}Old Folder name: {RESET}{old_folder_name}")
                    print(f"{RED}{bot_name}{RESET}: Give new name for folder `{old_folder_name}`")
                    new_folder_name = speech_recognize(recognizer, stream)
                    print(f"{BLUE}New Folder name: {RESET}{new_folder_name}")
                    rename_folder(old_folder_name, new_folder_name)

                # Weather Forecast
                elif tag == "weather":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    city =  speech_recognize(recognizer, stream)
                    print(f"{BLUE}Location: {RESET}{city}")
                    city, description, temperature = weather_forecast(city)
                    print(
                        f"{RED}{bot_name}{RESET}: In {city}, the temperature is {temperature} degrees Celsius. The weather condition is {description}.")

                # Google Search
                elif tag == "google":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    query = speech_recognize(recognizer, stream)
                    print(f"{BLUE}Search Query: {RESET}{query}")
                    search_results = google_search(query)
                    if search_results:
                        print(
                            f"{RED}{bot_name}{RESET}: Here are the search results ->")
                        for result in search_results:
                            print(result)
                        print(
                            f"{BLUE}Opening{RESET}: {search_results[0]}")
                    else:
                        print(
                            f"{RED}{bot_name}{RESET}: No search results found for '{query}'.")

                # YouTube Search
                elif tag == "youtube":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    query = speech_recognize(recognizer, stream)
                    print(f"{BLUE}Search Query: {RESET}{query}")
                    video_url = youtube_search(query)
                    print(f"{RED}{bot_name}{RESET}: Opening YouTube -> {video_url}")

                # Device control
                elif tag == "Sleep" or tag == "Shutdown" or tag == "LogOff":
                    print(f"{RED}{bot_name}{RESET}: Enter device control mode once again to verify\n1. sleep\n2. shutdown\n3. logoff\n")
                    choice = speech_recognize(recognizer, stream).lower()
                    cmd = system_control(choice)
                    print(f"{BLUE}Running script: {cmd}{RESET}")
                    
                    # TODO: Exception for timer loop
                    for timer in range(5, 0, -1):  # Countdown from 5 to 1
                        print(f"{RED}{bot_name}{RESET}: {response} in {timer} sec{RESET}", end="\r")
                        time.sleep(1)  # 1-second delay between countdown messages
                    print(f"{RED}{bot_name}{RESET}: {response} now{RESET}")

                # TODO: Email 
                # Sending E_mail
                elif tag == "E_mail":
                    pass
                  
                # Volume Control
                elif tag == "Volume_Up":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    action_handler.volume_increase()

                elif tag == "Volume_Down":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    action_handler.volume_decrease()

                # Brightness Control
                elif tag == "Brightness_Up":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    brightness_controller.Brightness_Increase()

                elif tag == "Brightness_Down":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    brightness_controller.Brightness_Decrease()

                # Open Application 
                elif tag == "Open_Application":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    input_sentence = ' '.join(sentence)
                    # print(sentence, input_sentence)
                    application_name = extract_application_name(input_sentence)
                    if application_name:
                        open_application(application_name.lower(), application_paths)
                        print(f"Opened {application_name}")
                    else:
                        print("No application name found in the input sentence.")




                # TODO: Storing messages in txt or docx file
                # TODO: Reminder, Alarm, Events, To-do list
                # TODO: ChatGPT

                # TODO: Final Speech Transcription Integration

                else:
                    print(f"{RED}{bot_name}{RESET}: {response}")
                break

                
    else:
        print(f'{RED}{bot_name}{RESET}: I donot understand...')
