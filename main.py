from  ai_backend import ai_endpoint 
from voice_recognition import recognize_speech
from tts import speak
import queue

# TODO - make this customizable..
WAKE_WORDS = ["chatter", "charter", "chadar", "chadda"]
END_WORDS = ["bye", "goodbye", "exit", "quit"]

def main(ui_queue):
    print("Waiting for wake word")
    while True:
        speech = recognize_speech()

        if not speech:
            ui_queue.put({"state": "idle"})
            continue


        lower_speech = speech.lower()
     
        
        wake = next((w for w in WAKE_WORDS if w in lower_speech), None)
        if not wake:
            continue

        cmd = lower_speech.split(wake, 1)[1].strip()
        if not cmd:
            ui_queue.put({"state": "listening"})
            print("Yes?")
            cmd = recognize_speech()
            if not cmd:
                continue

        if any(end in cmd for end in END_WORDS):
            ui_queue.put({"state": "idle"})
            print("Goodbye")
            ending = "Goodbye"
            speak(ending)
            return

        response = ai_endpoint(cmd)
        if response:
            ui_queue.put({"state": "listening"})
            print(response)
            speak(response)
            ui_queue.put({"state": "idle"})
            
     
