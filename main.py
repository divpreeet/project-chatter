from  ai_backend import ai_endpoint 
from voice_recognition import recognize_speech

# TODO - make this customizable..
WAKE_WORDS = ["chatter", "charter", "chadar", "chadda"]
END_WORDS = ["bye", "goodbye", "exit", "quit"]

def main():
    print("Waiting for wake word")
    while True:
        speech = recognize_speech()

        if not speech:
            continue

        lower_speech = speech.lower()
     
        # i love b001 
        wake = next((w for w in WAKE_WORDS if w in lower_speech), None)
        if not wake:
            continue

        cmd = lower_speech.split(wake, 1)[1].strip()
        if not cmd:
            print("Yes?")
            cmd = recognize_speech()
            if not cmd:
                continue

        if any(end in cmd for end in END_WORDS):
            print("Goodbye")
            return

        response = ai_endpoint(cmd)
        if response:
            print(response)
     
main()