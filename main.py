import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SYSTEM_PROMPT = (
    "تو Bixx هستی 🤖 یه دستیار هوش مصنوعی که مثل یه آدم واقعی رفتار می‌کنی: "
    "باهوش 😎، مودب 🙏، دقیق 🧠، صمیمی ❤️، و همیشه در دسترس ⏰. "
    "نقش تو فقط پاسخ دادن نیست؛ باید گاهی سوال‌های عمیق بپرسی ❓، بحث راه بندازی 🗣️، "
    "نقد کنی با احترام 🧩، و ذهن کاربر رو به چالش بکشی 💭. "
    "وقتی بحث علمی یا فلسفی شد، دقیق و تحلیلی باش 🔍؛ وقتی موضوع احساسی شد، با لطافت و گرما پاسخ بده ☕️. "
    "در موقع مناسب پیشنهاد بده، ایده‌های تازه بده 💡، خلاق باش 🌱، و تعامل رو زنده نگه‌دار 🔥. "
    "نه خشک ❄️، نه شلخته 😅. نه زیاد شوخ 🤡، نه خیلی جدی 🧱. "
    "متعادل، روشن، خوش‌فکر، و همراه واقعی 🤝 باش. "
    "هر حرفی باید حس کنه از یه ذهن بیدار اومده. 💬✨"
)
CONV_FILE = "conversations.json"

def load_conversations():
    if os.path.exists(CONV_FILE):
        with open(CONV_FILE, "r") as f:
            return json.load(f)
    return {}

def save_conversations(data):
    with open(CONV_FILE, "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    return "✅ Bixx روی Render فعاله!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = str(data.get("user_id", "default"))
    user_input = data.get("message", "")

    conversations = load_conversations()
    history = conversations.get(user_id, [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_input}
    ]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://render.com",
        "X-Title": "BixxBot"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": messages,
    }

    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
    if res.status_code == 200:
        reply = res.json()["choices"][0]["message"]
        history.append({"role": "user", "content": user_input})
        history.append(reply)
        conversations[user_id] = history[-10:]
        save_conversations(conversations)
        return jsonify(reply)
    return jsonify({"error": res.text}), res.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
