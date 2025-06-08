import speech_recognition as sr
import sounddevice as sd
import numpy as np

def recognize_speech():
    recognizer = sr.Recognizer()

    duration = 5 
    sample_rate = 16000

    print("Listening...")
    audio_array = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    audio_array = audio_array.flatten()

    audio_bytes = audio_array.tobytes()
    audio = sr.AudioData(audio_bytes, sample_rate, 2)  

    usr_message = ""
    try:
        usr_message = recognizer.recognize_google(audio)
        print(f"this is what you said - {usr_message}")
    except Exception as e:
        print(e)

    return usr_message
