# app.py
import os
import requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var is required")

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if not data:
        return jsonify(ok=True)
    # Only handle message updates (basic)
    message = data.get("message")
    if not message:
        return jsonify(ok=True)

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        reply = "Assalamu alaikum! Ami online achi. Apni /help try korte paren."
    elif text.startswith("/help"):
        reply = "Simple bot: lekho kichu, ami abar bole debo."
    else:
        reply = f"You said: {text}"

    send_message(chat_id, reply)
    return jsonify(ok=True)

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("send_message error:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
