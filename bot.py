import os
import telebot
from telebot import types
from flask import Flask
import threading

# Tokenni Render/GitHub orqali xavfsiz ulaymiz
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

PREMIUM_KEY = "YUKIO-JDSA-11NI-ADKP-MOAS-7777"
SAYT_LINKI = "https://o_zingizning_github_username.github.io/yukio-hub/" 

app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7 successfully!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Eski xabarlarni tozalab, faqat bitta toza xabar qoldirish funksiyasi
last_bot_messages = {}

def send_clean_message(chat_id, text, reply_markup=None):
    # Oldingi bot xabarini o'chirishga harakat qiladi
    if chat_id in last_bot_messages:
        try:
            bot.delete_message(chat_id, last_bot_messages[chat_id])
        except:
            pass
            
    msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=reply_markup)
    last_bot_messages[chat_id] = msg.message_id
    return msg

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    # Foydalanuvchi yuborgan buyruqni o'chiramiz
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    welcome_text = (
        f"🌸 *Welcome to Yukio Hub | Software Service* 🌸\n\n"
        f"Hello, {message.from_user.first_name}!\n"
        f"Unlock high-tier elite script modules execution right now.\n\n"
        f"💎 *Premium License Key Price:* 449 ⭐ (Telegram Stars)\n"
        f"Click the button below to secure your transaction and claim your key instantly."
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Telegram Stars to'lov tugmasi
    btn_pay = types.InlineKeyboardButton("💳 Pay 449 Stars", callback_data="buy_premium_stars")
    btn_site = types.InlineKeyboardButton("🌐 Access Official Website", url=SAYT_LINKI)
    markup.add(btn_pay, btn_site)
    
    send_clean_message(chat_id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    
    if call.data == "buy_premium_stars":
        # Telegram Stars uchun Invoice (Invoys) shakllantiramiz
        try:
            bot.send_invoice(
                chat_id=chat_id,
                title="Yukio Hub Premium Key",
                description="Instant lifetime access code for Sakura Premium modules.",
                invoice_payload="yukio_premium_payload",
                provider_token="", # Telegram Stars uchun bu joy bo'sh qolishi Shart!
                currency="XTR",    # XTR - Telegram Stars valyutasi kodi
                prices=[types.LabeledPrice(label="Premium Key", amount=449)] # 449 Stars
            )
            # Invoys yuborilgach, uning ortidagi eski xabarni tozalaymiz
            if chat_id in last_bot_messages:
                try:
                    bot.delete_message(chat_id, last_bot_messages[chat_id])
                except:
                    pass
        except Exception as e:
            print(f"Invoice error: {e}")

# TO'LOV OLDIDAN TEKSHIRUV (Pre-checkout query)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    # To'lov oynasi ochilganda unga tasdiq javobini qaytaramiz (Ok)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# TO'LOV MUVAFFAQIYATLI YAKUNLANGANDA (Successful Payment)
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    chat_id = message.chat.id
    
    # To'lov haqidagi xabarni va foydalanuvchi chekini darhol o'chiramiz chat toza turishi uchun
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    success_text = (
        f"✨ *Payment Successful! Authorization Granted!* ✨\n\n"
        f"🔑 *Your Premium License Key:*\n"
        f"`{PREMIUM_KEY}`\n\n"
        f"📌 *How to use it?*\n"
        f"1. Open our official website.\n"
        f"2. Navigate to the *Premium* sector.\n"
        f"3. Paste the key above and click *Verify Authorization*.\n\n"
        f"Thank you for supporting Yukio Hub! 🌸"
    )
    
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("🌐 Open Website", url=SAYT_LINKI)
    )
    send_clean_message(chat_id, success_text, reply_markup=markup)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Stars Payment Server online. Bot polling starting...")
    bot.infinity_polling(none_stop=True)
