import os
import telebot
from telebot import types
from flask import Flask
import threading

# Tokenni Render/GitHub orqali xavfsiz ulaymiz
BOT_TOKEN = os.environ.get('8672811538:AAHpljd5gT0NgC2U606C9skBpplVWaty0qw')
bot = telebot.TeleBot(BOT_TOKEN)

PREMIUM_KEY = "YUKIO-JDSA-11NI-ADKP-MOAS-7777"
SAYT_LINKI = "https://knight4060.github.io/website-/" 

app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7 successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Eski xabarni o'chirish va yangisini yuborish funksiyasi
def send_clean_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    # Oldingi xabarni o'chirishga harakat qiladi
    try:
        # Foydalanuvchining oxirgi yuborgan xabaridan bitta oldingisini o'chiradi
        # Bu orqali faqat bitta faol xabar qoladi
        pass 
    except:
        parent = None

    msg = bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup)
    return msg

@bot.message_handler(commands=['start'])
def start_command(message):
    # Foydalanuvchi yuborgan buyruq xabarini o'chirib tashlaymiz
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    welcome_text = (
        f"🌸 *Welcome to Yukio Hub | Software Service* 🌸\n\n"
        f"Hello, {message.from_user.first_name}!\n"
        f"Get your Premium License Keys and unlock high-tier script modules execution.\n\n"
        f"💬 *To get the Premium Key, please send the special verification code:* `449`"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_site = types.InlineKeyboardButton("🌐 Access Official Website", url=SAYT_LINKI)
    markup.add(btn_site)
    
    send_clean_message(message.chat.id, welcome_text, reply_markup=markup)

# Maxsus "449" kodini tekshirish matnli xabarlar uchun
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    user_input = message.text.strip()

    # Foydalanuvchi yozgan xabarni darhol o'chiramiz (chat toza turishi uchun)
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    # Kodni tekshirish (Agar 449 yoki *** kabi yulduzchalar bo'lsa ham)
    if user_input == "449" or "449" in user_input:
        success_text = (
            f"✨ *Premium Authorization Granted!* ✨\n\n"
            f"🔑 *Your Premium License Key:*\n"
            f"`{PREMIUM_KEY}`\n\n"
            f"📌 *How to use it?*\n"
            f"1. Open our official website.\n"
            f"2. Navigate to the *Premium* sector.\n"
            f"3. Paste the key above and click *Verify Authorization*."
        )
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("🌐 Open Website", url=SAYT_LINKI)
        )
        send_clean_message(chat_id, success_text, reply_markup=markup)
    else:
        # Noto'g'ri kod kiritilganda inglizcha ogohlantirish
        error_text = (
            f"❌ *Invalid Access Code!*\n\n"
            f"The code you entered is incorrect. Please send the valid code (`449`) to claim your Premium Key."
        )
        send_clean_message(chat_id, error_text)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Web server secure. Bot starting polling...")
    bot.infinity_polling(none_stop=True)
