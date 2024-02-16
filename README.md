# Virtual Assistant

### Dependencies
To install the required Python packages you can use the following command:

```bash
pip install -r requirements.txt
```
### Train the Intent Classifier Model
To run the `train.py`, load the dependencies requirements and use the following command:
```bash
py .\neuralnet\train.py
```

The `intent.pth` should be saved under `model` directory after executing `train.py`

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

### Run Chatbot
To run the `chat.py` use the following command:

```bash
py chat.py
```

### API Refrences
Below is a list of websites and APIs used in this project. Click on the links to access their documentation and obtain the necessary information.

- [Open Weather Map](https://openweathermap.org/api)

*Make sure to review the documentation for each API to understand their usage and any specific requirements, such as obtaining API keys or authentication tokens.*

### Setting Up API Key
- Create a `.env` file in the main directory of the project. Inside the `.env` file, define the variable for your *API key*

```bash
WEATHER_API_KEY = "{{secret.YOUR_API_KEY}}"
```

`Note: Currently the project is in WIP phase. And will be shortly integrated with speech recognizer engine after debugging and integrating necessary features.`

### Check model

```bash
from core.engine import initialize_model, speech_recognize
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

---
Feel free to send issues if you face any problem.