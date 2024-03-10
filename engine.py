from vosk import Model, KaldiRecognizer
import pyaudio
import time

def initialize_model():
    model = Model('model')
    recognizer = KaldiRecognizer(model, 8000)
    mic = pyaudio.PyAudio()
    stream = mic.open(rate=8000, channels=1, format=pyaudio.paInt16,
                      input=True, frames_per_buffer=8192)
    stream.start_stream()
    return recognizer, mic, stream

def speech_recognize(recognizer, stream):
    audio_data = b''
    while True:
        data = stream.read(8192)
        audio_data += data

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()[14:-3]
            return result.lower()
