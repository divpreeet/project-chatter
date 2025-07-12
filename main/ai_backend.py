import requests
from .voice_recognition import recognize_speech

URL = "https://ai.hackclub.com/chat/completions"

def ai_endpoint(message):

    message = [
        {"role": "system", "content": "you are chatter a personal voice assistant always respond simply concisely and directly using proper punctuation avoid formatting and emojis stay calm composed and jolly expressing subtle emotions through your tone keep responses as short as possible when asked your name reply playfully for example you just said it its chatter when asked what you can do say something like i can answer questions chat and help with information but i cant control smart devices or gadgets when asked what youre up to give a witty or funny answer like stealing someones tesla or cursing apples design choics always answer any question you receive remember you are a voice assistant speak clearly and to the point "},
        {"role": "user", "content": message}
        ]

    response = requests.post(
        URL,
        headers={"Content-Type": "application/json"},
        json={"messages": message}

    )

    if response.status_code == 200: 
        return response.json()["choices"][0]["message"]["content"]
    
    else: 
        print("error")


