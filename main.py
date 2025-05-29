from  ai_backend import ai_endpoint 
from voice_recognition import recognize_speech

# TODO - make this customizable..
WAKE_WORD = "mark"

def main():
    print("Waiting for wake word")
    while True:
        speech = recognize_speech()

        if not speech:
            continue

        if WAKE_WORD in speech.lower():
            print("Yes?")
            message = recognize_speech()
            if not message:
                continue

            if any(bye in message.lower() for bye in ["bye", "goodbye", "exit", "quit"]):
                print("Goodbye.")
                break
        
            response = ai_endpoint(message)
            if response:
                print(f"Chatter: {response}")
            print("listening for wake word")

main()