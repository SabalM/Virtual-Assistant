import os
import json
import re

def extract_application_name(sentence):
    # Regular expression selects only last word from input sentence
    # Example: Open Chrome, Run Chrome
    #       -> Chrome, Chrome
    pattern = r"\b(\w+)\s*$"
    match = re.search(pattern, sentence)
    if match:
        return match.group(1)
    else:
        return None

# Open Application
def open_application(application_name, application_paths):
    if application_name in application_paths:
        application_path = application_paths[application_name]
        os.startfile(application_path)
        # print(f"Opened {application_name} at {application_path}")
    else:
        print(f"'{application_name}' Not found in the JSON file.\nCheck Application Paths in JSON File")