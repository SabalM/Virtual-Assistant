from googlesearch import search
import pywhatkit as kit
import webbrowser
# import os 

# Replace Path_to_ChromeDriver Executable file in .env
# path_to_chromedriver = os.getenv('chromedriver')


# Google Search
# NOTE: Chrome must be installed in default path 
def google_search(query, num_results=5):
    try:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        # print(chrome_path)

        if chrome_path:
            search_results = list(search(query, num_results=num_results))
            if search_results:
                first_result = search_results[0]
                # print(first_result)

                # Open chrome and open first search_results
                webbrowser.get(chrome_path).open(first_result)
                print("Opened the first search result in Google Chrome.")
                return search_results
            else:
                print("No search results found.")
        else:
            print("Chrome path not found in app_paths.json. Cannot open Chrome.")
    except Exception as e:
        print("An error occurred while performing the Google search:", e)
        return []

# YouTube Search
def youtube_search(query):
    try:
        video_url = kit.playonyt(query)
        return video_url
    except Exception as e:
        print("An error occurred while performing the YouTube search:", e)
        return []
