import os
import telebot
from telebot import types
import time

# Tokenni GitHub Secrets-dan olamiz
BOT_TOKEN = os.environ.get('8672811538:AAHpljd5gT0NgC2U606C9skBpplVWaty0qw')
bot = telebot.TeleBot(BOT_TOKEN)

PREMIUM_KEY = "YUKIO-JDSA-11NI-ADKP-MOAS-7777"
SAYT_LINKI = "https://knight4060.github.io/website-/" 

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

# GITHUB ACTIONS TO'XTAB QOLMASLIGI UCHUN MUSTAHKAM POLLING AYLANMASI
while True:
    try:
        print("Bot ishlamoqda...")
        bot.polling(none_stop=True, interval=2, timeout=20)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}. 5 soniyadan keyin qayta urunib ko'riladi...")
        time.sleep(5)
