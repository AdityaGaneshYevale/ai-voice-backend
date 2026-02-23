# #  IMPORTS
# from fastapi import FastAPI
# from pydantic import BaseModel
# import datetime
# import requests
# import re
# import feedparser
# import firebase_admin
# from firebase_admin import credentials, firestore
# import ollama
# #CONFIG
# OPEN_WEATHER_API_KEY = "c490ae765bd4f1bb67c96f114004f886"
# app = FastAPI(title="Voice Assistant Backend")
# # 🔥 Firebase Init
# cred = credentials.Certificate("firebase_key.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()
# #MODELS
# class CommandRequest(BaseModel):
#     text: str
#     userId: str | None = "guest"
# class CommandResponse(BaseModel):
#     reply: str
# # FIRESTORE SAVE
# def save_chat(user_id: str, user_text: str, ai_reply: str):
#     db.collection("chats").add({
#         "userId": user_id,
#         "userText": user_text,
#         "aiReply": ai_reply,
#         "timestamp": firestore.SERVER_TIMESTAMP
#     })
# #INTENT DETECTION
# def detect_intent(text: str) -> str:
#     text = text.lower()
#     if "weather" in text or "temperature" in text:
#         return "weather"
#     if "news" in text or "headlines" in text:
#         return "news"
#     if any(k in text for k in ["what", "who", "explain", "why", "how", "tell me"]):
#         return "faq"
#     # simple chat detection
#     if len(text.split()) > 1:
#         return "chat"
#     return "unknown"
# # OLLAMA
# def ollama_reply(prompt: str) -> str:
#     try:
#         response = ollama.chat(
#             model="llama3.2:3b",
#             messages=[{"role": "user", "content": prompt}]
#         )
#         return response["message"]["content"]
#     except Exception as e:
#         return f"Ollama error: {e}"

# #WEATHER
# def handle_weather(text: str) -> str:
#     city = "Pune"
#     match = re.search(r"(in|of)\s([a-zA-Z\s]+)", text)
#     if match:
#         city = match.group(2).strip()
#     url = (
#         "https://api.openweathermap.org/data/2.5/weather"
#         f"?q={city}&appid={OPEN_WEATHER_API_KEY}&units=metric"
#     )
#     try:
#         response = requests.get(url, timeout=10)
#         data = response.json()
#         if response.status_code != 200:
#             return f"Sorry, I could not fetch weather information for {city}."
#         temp = data["main"]["temp"]
#         desc = data["weather"][0]["description"]
#         now = datetime.datetime.now().strftime("%d %B %Y %I:%M %p")
#         return (
#             f"Today is {now}. "
#             f"The weather in {city} is {desc} "
#             f"with a temperature of {temp} degree Celsius."
#         )
#     except Exception:
#         return "Sorry, I could not fetch the weather information."
# #NEWS
# def handle_news() -> str:
#     feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
#     feed = feedparser.parse(feed_url)
#     if not feed.entries:
#         return "Sorry, I could not find any news right now."
#     headlines = []
#     for i, entry in enumerate(feed.entries[:5]):
#         headlines.append(f"Headline {i+1}: {entry.title}")
#     return "Here are the latest news headlines. " + " . ".join(headlines)
# #MAIN API
# @app.post("/command", response_model=CommandResponse)
# def process_command(req: CommandRequest):
#     print("Received:", req.text)
#     text = req.text.lower()
#     user_id = req.userId or "guest"
#     intent = detect_intent(text)
#     if intent == "weather":
#         reply = handle_weather(text)
#     elif intent == "news":
#         reply = handle_news()
#     else:
#         reply = ollama_reply(text)  # faq/chat/unknown → Ollama
#     save_chat(user_id, req.text, reply)
#     return {"reply": reply}



from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
import feedparser

app = FastAPI(title="AI Voice Assistant Backend")

# ✅ API key environment मधून घेणार (secure)
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY", "demo_key")

class CommandRequest(BaseModel):
    text: str
    userId: str | None = "guest"

class CommandResponse(BaseModel):
    reply: str


@app.get("/")
def home():
    return {"message": "Server Running Successfully 🚀"}


@app.post("/command", response_model=CommandResponse)
def process_command(req: CommandRequest):
    text = req.text.lower()

    if "weather" in text:
        return {"reply": "Weather feature working ✅"}

    elif "news" in text:
        return {"reply": "News feature working ✅"}

    else:
        return {"reply": "Hello Aditya! Backend is live 🚀"}