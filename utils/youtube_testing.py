import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pywhatkit as kit
import time 


# Initialize Chrome WebDriver with options to ignore SSL errors
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Initialize WebDriverWait with timeout
wait = WebDriverWait(driver, 10)

# Define expected conditions for presence and visibility
presence = EC.presence_of_element_located
visible = EC.visibility_of_element_located

# Search query
query = "hello"

try:
    video = "minion"
    # Navigate to the YouTube search results page
    driver.get('https://www.youtube.com/results?search_query={}'.format(str(video)))

    # Wait for the video title to be visible and clickable
    video_title = wait.until(visible((By.ID, "video-title")))

    # Click on the video title to play the video
    video_title.click()


    time.sleep(15)

    # pauses
    next_button = driver.find_element(By.CLASS_NAME, "ytp-play-button")
    next_button.click()

    time.sleep(5)

    # play again
    play_button = driver.find_element(By.CLASS_NAME, "ytp-play-button")
    play_button.click()

    time.sleep(15)

except KeyboardInterrupt:
    # If the user interrupts the script, print a message and close the WebDriver session
    print("Script execution interrupted by user.")
finally:
    # Close the WebDriver session
    driver.quit()
