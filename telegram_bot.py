import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.message.from_user.id)
    payload = {
        "user_id": user_id,
        "message": user_text
    }
    try:
        res = requests.post(BACKEND_URL, json=payload)
        if res.status_code == 200:
            reply = res.json().get("content", "✅ پاسخ دریافت شد ولی خالی بود")
        else:
            reply = f"❌ خطای سرور: {res.status_code}"
    except Exception as e:
        reply = f"🚫 خطا در اتصال: {e}"
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
