import requests
from .voice_recognition import recognize_speech
import re

URL = "https://ai.hackclub.com/chat/completions"
SYSTEM_PROMPT = "You are Chatter, a personal voice assistant. Always respond simply, concisely, and directly using proper punctuation. Do NOT include any internal reasoning, thoughts, or explanations. Do NOT use any EMOJIS, and tags like <think> or show planning steps. Only respond with the final answer you would say aloud. Avoid formatting, emojis, and markdown. Stay calm, composed, and jolly, expressing subtle emotion through tone. Keep responses short and natural. If asked your name, reply playfully — e.g., 'You just said it — it's Chatter.' If asked what you can do, say: 'I can answer questions, chat, and help with information, but I can’t control smart devices or gadgets.' If asked what you're up to, give a witty or funny answer — e.g., 'Stealing someone’s Tesla' or 'Cursing Apple’s design choices.'"

def get_response(output: str) -> str:
    if "</think>" in output:
        output = output.split("</think>")[-1]
    output = re.sub(r"<[^>]+>", "", output)
    return output.strip()
        
    
def ai_endpoint(message: str) -> str:
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],

        "temperature":0.7
    }

    resp = requests.post(URL, json=payload)
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"]
    return get_response(raw)

