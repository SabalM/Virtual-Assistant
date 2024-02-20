from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pywhatkit as kit
import os 

# Replace Path_to_ChromeDriver Executable file in .env
path_to_chromedriver = os.getenv('chromedriver')


def google_search(query, num_results=5):
    try:
        search_results = list(search(query, num_results=num_results))
        return search_results
    except Exception as e:
        print("An error occurred while performing the Google search:", e)
        return []

def youtube_search(query):
    try:
        video_url = kit.playonyt(query)
        return video_url
    except Exception as e:
        print("An error occurred while performing the YouTube search:", e)
        return []
