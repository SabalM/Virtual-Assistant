import torch
import os
import json
import random

# import Speech Engine
# from core.engine import *
# from core.intents import *

# import Intent
from neuralnet.model import IntentModelClassifier
from neuralnet.nltk_utils import bag_of_words, tokenize

# import task automation functions
from utils.directory import *
from utils.weather import *
from utils.online_surf import *
from utils.device_control import *

#for volume control
from utils.volume_control import ActionHandler
# Instantiate ActionHandler for volume control
action_handler = ActionHandler()

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
RESET = "\033[0m"


bot_name = "ByteBot"
print("Let's chat! (type 'quit' to exit)")
while True:
    sentence = input(f"{GREEN}You{RESET}: ")
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
                    # recognizer, mic, stream = initialize_model()
                    # print(user_input)
                    # folder_name = speech_recognize(recognizer, stream)
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = input(f"{GREEN}Name your folder{RESET}: ")
                    create_folder(folder_name)

                # Delete Folder
                elif tag == "Delete":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    folder_name = input(f"{GREEN}Name of folder{RESET}: ")
                    delete_folder(folder_name)

                # Weather Forecast
                elif tag == "weather":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    city = input(f"{GREEN}Enter city name{RESET}: ")
                    city, description, temperature = weather_forecast(city)
                    print(
                        f"{RED}{bot_name}{RESET}: In {city}, the temperature is {temperature} degrees Celsius. The weather condition is {description}.")

                # Google Search
                elif tag == "google":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    query = input(f"{GREEN}Enter search term{RESET}: ")
                    search_results = google_search(query)
                    if search_results:
                        print(
                            f"{RED}{bot_name}{RESET}: Here are the search results ->")
                        for result in search_results:
                            print(result)
                    else:
                        print(
                            f"{RED}{bot_name}{RESET}: No search results found for '{query}'.")

                # YouTube Search
                elif tag == "YouTube":
                    print(f"{RED}{bot_name}{RESET}: {response}")
                    query = input(f"{GREEN}Enter search term{RESET}: ")
                    video_url = youtube_search(query)
                    print(f"{RED}{bot_name}{RESET}: Click on link -> {video_url}")

                # Device control
                elif tag == "Sleep" or tag == "Shutdown" or tag == "LogOff":
                    choice = input(f"{RED}{bot_name}{RESET}: Enter device control mode once again to verify\n1. sleep\n2. shutdown\n3. logoff\n").lower()
                    cmd = system_control(choice)
                    print(f"Running script: {cmd}")
                    
                    # TODO: Exception for timer loop
                    for timer in range(5, 0, -1):  # Countdown from 5 to 1
                        print(f"{RED}{bot_name}{RESET}: {response} in {timer} sec{RESET}", end="\r")
                        time.sleep(1)  # 1-second delay between countdown messages
                    print(f"{RED}{bot_name}{RESET}: {response} now{RESET}")

                # Sending E_mail
                elif tag == "E_mail":
                    pass
                
                
                # VOLUME CONTROL
                elif tag == "Volume_Up":
                    print("Volume")
                    action_handler.volume_increase()
                elif tag == "Volume_Down":
                    action_handler.volume_decrease()

                # TODO: Storing messages in txt or docx file
                # TODO: Reminder, Alarm, Events, To-do list
                # TODO: ChatGPT
                # TODO: Email
                # TODO: Application Bookmark
                # TODO: File search and handling 'Copy, Renaming, Move Folders/Files'  
                # TODO: Final Speech Transcription Integration


                else:
                    print(f"{RED}{bot_name}{RESET}: {response}")
                break

                
    else:
        print(f'{RED}{bot_name}{RESET}: I donot understand...')
