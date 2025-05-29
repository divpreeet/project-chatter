# AI Backend using HC AI. 
import requests

URL = "https://ai.hackclub.com/chat/completions"

def ai_endpoint(message):

    message = [
        {"role": "system", "content": "Your name is chatter, a personal voice assistant, you provide simple, concise and to the point repsonses, you dont use any formatting, you should provide an response to anything the user asks, you should alwasy be calm, composed, and straight to the point, avoid emojis, but provide a sense of emotions and feelings"},
        {"role": "user", "content": message}
        ]

    response = requests.post(
        URL,
        headers={"Content-Type": "application/json"},
        json={"messages": message}

    )

    if response.status_code == 200: 
#        print("working")
        return response.json()["choices"][0]["message"]["content"]
    
    else: 
        print("error")

message = input("how can i assist you?: ")
print(ai_endpoint(message))
