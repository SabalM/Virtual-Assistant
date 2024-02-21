# Virtual Assistant
## Features
- **Speech Recognition**: Utilizes the `Vosk` model for accurate speech recognition, enabling seamless interaction through voice commands.
- **Intent Classification**: Employs a `three-layer linear` model with `ReLU activation` functions to classify user intents effectively.
- **Basic Task Automation**: Capable of performing various basic tasks, such as creating, renaming, and deleting folders, searching the web, managing device controls, and more.
- **Expandability**: Can be easily expanded to accommodate additional functionalities based on specific user needs.

## Usage
To use the Virtual Assistant:

- **Download Speech Recongition Model**:
    Extract the compressed `.rar` file inside `model` named directory.
    
    [Click here ](https://drive.google.com/file/d/1yRg1b8Eo_L7tDpLq1UoywlfPAPdrQY0v/view?usp=sharing)

- **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
- **Run `train.py` for `Intent Classification`**:

    ```bash
    py .\neuralnet\train.py
    ```
    The `intent.pth` will be saved under `model` directory after executing `train.py`.

- **Set API Keys**:

    Create a `.env` file in the main directory of the project. Inside the `.env` file, define the variable for your *API key*

    Below is a list of websites and APIs used in this project. Click on the links to access their documentation and obtain the necessary information.

    - [Open Weather Map](https://openweathermap.org/api)

        *Make sure to review the documentation for each API to understand their usage and any specific requirements, such as obtaining API keys or authentication tokens.*

    ```bash
    WEATHER_API_KEY = "{{secret.YOUR_API_KEY}}"
    ```

- **Run Script**: 

    ```bash
    py chat.py
    ```

- **Interaction**:

    ```
    You: hello
    ByteBot: Hi there, how can I assist you today?
    You: tell me a joke
    ByteBot: A perfectionist walked into a bar...apparently, the bar wasn't set high enough
    You:  
    ```

- #### Customization:

    If you want to customize the intent according to your needs, add the `tags`, `patterns` and `responses` inside `intents.json` in following format and re-run `train.py` while adding functionality features in `chat.py`. The `intent.json` should follow this base format:

    ```json
    {
        "intents": [
            {
                "tag": "greeting",
                "patterns": [
                    "Hi there",
                    "Hello",
                    "yo"
                ],
                "responses": [
                    "Hello",
                    "Good to see you again",
                    "Hi there, how can I help?"
                ],
            }
        ]
    }
    ```

### Speech Recognition Model
If the **speech recognition** model shows errors, run this script on the same directory path

```python
from engine import initialize_model, speech_recognize
# Transcript
transcript = ''

if __name__ == "__main__":
    recognizer, mic, stream = initialize_model()

    while True:
        data=stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()[14:-3]
            transcript += result + ' '
            print(transcript)
```


## Contributors <img src="https://user-images.githubusercontent.com/74038190/213844263-a8897a51-32f4-4b3b-b5c2-e1528b89f6f3.png" width="25px" />
<a href="https://github.com/404saugat404/automation/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=404saugat404/automation"/>
</a>

### Limitations
*The current version of the Virtual Assistant may have limitations in complex tasks or specialized domains. You can add more functions or integrate `Language Models` like `Llama2`, `MistralAI`, `BERT`.*

<!-- License
[License Information] -->

---
Feel free to customize and extend the **Virtual Assistant** to suit your specific needs and requirements. Contributions and feedback are welcome! 