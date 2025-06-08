from ai_backend import ai_endpoint 
from voice_recognition import recognize_speech
from tts import speak
import queue
import threading
import time

speaking_flag = threading.Event()
WAKE_WORDS = ["chatter", "charter", "chadar", "chadda"]
END_WORDS = ["bye", "goodbye", "exit", "quit"]


def main(ui_queue):
    print("Waiting for wake word")
    while True:
        if not speaking_flag.is_set():
            speech = recognize_speech()
        else:
            continue

        if not speech:
            ui_queue.put({"state": "idle", "text": ""})
            continue

        lower_speech = speech.lower()
        wake = next((w for w in WAKE_WORDS if w in lower_speech), None)
        if not wake:
            ui_queue.put({"state": "idle", "text": ""})
            continue

        ui_queue.put({"state": "listening", "text": f'"{speech}"'})
        # time.sleep(0.05)

        cmd = lower_speech.split(wake, 1)[1].strip()
        if not cmd:
            ui_queue.put({"state": "listening", "text": "Yes?"})
            time.sleep(0.05)
            print("Yes?")
            speak("Yes?")
            cmd = recognize_speech()
            if not cmd:
                ui_queue.put({"state": "idle", "text": ""})
                continue

        if any(end in cmd for end in END_WORDS):
            ui_queue.put({"state": "idle", "text": "Goodbye"})
            time.sleep(0.05)
            print("Goodbye")
            speak("Goodbye")
            break

        ui_queue.put({"state": "thinking", "text": ""})
        # time.sleep(0.05)

        response = ai_endpoint(cmd)

        ui_queue.put({"state": "speaking", "text": response})
        def _speak_and_reset(response):
            #time.sleep(0.05)
            speaking_flag.set()
            print(response)
            speak(response)
            speaking_flag.clear()
            ui_queue.put({"state": "idle", "text": ""})
        
        threading.Thread(target=_speak_and_reset, args=(response,), daemon=True).start()
