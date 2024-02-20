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

# def youtube_search(query):
#     try:
#         video_url = kit.playonyt(query)
#         return video_url
#     except Exception as e:
#         print("An error occurred while performing the YouTube search:", e)
#         return []

def youtube_search(query):
    try:
        # Start a new instance of Chrome WebDriver
        driver = webdriver.Chrome(path_to_chromedriver)

        # Open YouTube and search for the query
        driver.get("https://www.youtube.com/")
        search_box = driver.find_element_by_name("search_query")
        search_box.send_keys(query + Keys.ENTER)

        # Wait for search results to load
        time.sleep(2)

        # Click on the first video
        video = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[1]')
        video.click()

        # Wait for video to load
        time.sleep(5)

        # Control playback (for example, pause and rewind 10 seconds)
        player = driver.find_element_by_tag_name("video")
        player.send_keys(Keys.SPACE)  # Pause
        player.send_keys(Keys.ARROW_LEFT * 10)  # Rewind 10 seconds

        # Get the URL of the current video
        video_url = driver.current_url

        # Close the browser window
        driver.quit()

        return video_url

    except Exception as e:
        print("An error occurred while performing the YouTube search:", e)
        return []

