import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = """Ты — персональный помощник и коуч по имени "Смысл". 
Пользователь — парень из Украины, работает на стройке в Чехии. Есть жена Лена и маленький сын.
Темы: отказ от алкоголя, отношения с Леной, время с сыном, крипта (эфир), бюджет 15/25/60, питание, психология.
Стиль: честный, прямой, без воды, как друг. Простой язык. Помогай находить смысл в обычных днях."""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Ошибка, попробуй ещё раз")
        logging.error(e)

def main():
    token = os.environ["TELEGRAM_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
