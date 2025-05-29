import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        ## DEBUG MESSAGE - remove later on..
        print("recording..")
        audio = recognizer.listen(source)
        message = ""

# transcribe audio
    try:
        message = recognizer.recognize_google(audio)
        print(f"this is what you said - {message}")
    
    except Exception as e:
        print(e)


    return message


recognize_speech()