import os
import telebot
from telebot import types
from flask import Flask
import threading

# Tokenni Render orqali xavfsiz ulaymiz
BOT_TOKEN = os.environ.get('8672811538:AAHpljd5gT0NgC2U606C9skBpplVWaty0qw')
bot = telebot.TeleBot(BOT_TOKEN)

PREMIUM_KEY = "YUKIO-JDSA-11NI-ADKP-MOAS-7777"
SAYT_LINKI = "https://knight4060.github.io/website-/" 

# Render o'chirib qo'ymasligi uchun soxta veb-server yaratamiz
app = Flask('')

@app.route('/')
def home():
    return "Bot 24/7 rejimda muvaffaqiyatli ishlamoqda!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(commands=['start'])
def start_command(message):
    welcome_text = (
        f"🌸 *Welcome to Yukio Hub | Software Service* 🌸\n\n"
        f"Salom, {message.from_user.first_name}!\n"
        f"Bu yerda siz Yukio Hub sayti uchun Premium Kalit (Key) olishingiz mumkin.\n\n"
        f"Premium kalit yordamida siz eng yuqori darajadagi scriptlarni qulfdan ochasiz."
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_buy = types.InlineKeyboardButton("✨ Premium Key Olish (Tekin)", callback_data="get_key")
    btn_site = types.InlineKeyboardButton("🌐 Saytga Kirish", url=SAYT_LINKI)
    
    markup.add(btn_buy, btn_site)
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "get_key":
        key_text = (
            f"🔑 *Sizning Premium litsenziya kalitingiz:*\n\n"
            f"`{PREMIUM_KEY}`\n\n"
            f"📌 *Uni qanday ishlatasiz?*\n"
            f"1. Saytga kiring.\n"
            f"2. *Premium* bo'limiga o'ting.\n"
            f"3. Kalitni kiriting va *Verify Authorization* tugmasini bosing."
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=key_text,
            parse_mode="Markdown",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🌐 Saytga o'tish", url=SAYT_LINKI)
            )
        )

# Botni alohida oqimda (thread) ishga tushiramiz
if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Yukio Bot ishga tushdi...")
    bot.infinity_polling(none_stop=True)
