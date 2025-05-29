import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        usr_message = ""

# transcribe audio
    try:
        usr_message = recognizer.recognize_google(audio)
        print(f"this is what you said - {usr_message}")
    
    except Exception as e:
        print(e)


    return usr_message


