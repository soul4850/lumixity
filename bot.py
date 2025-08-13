import telebot
from telebot import types
from flask import Flask, request
import os

# === НАСТРОЙКИ ===
TOKEN = "8173283253:AAHl7T6ixA3P2mFxsICpXuMz-ALzEmzd7vE"
RAILWAY_URL = f"https://{os.environ.get('RAILWAY_STATIC_URL')}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === ОБРАБОТЧИКИ КОМАНД ===
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Продолжить")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     "Приветствуем! Это поддержка бренда «Lummixia». "
                     "Мы благодарим Вас за покупку и с радостью ответим на вопросы, "
                     "связанные с качеством товара, а также поможем его подключить и настроить.",
                     reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Продолжить")
def choose_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Наушники")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Пожалуйста, выберите Ваш товар из списка ниже.", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Наушники")
def choose_model(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    models = [
        "T90", "Dots 8s", "G36", "TWS MAX", "F6-s",
        "TWS Air 2Pods", "TWS PRO", "N13"
    ]
    for m in models:
        markup.add(types.KeyboardButton(m))
    bot.send_message(message.chat.id,
                     "Пожалуйста, выберите модель товара из списка ниже, "
                     "данную информацию Вы можете найти на оригинальной коробке.",
                     reply_markup=markup)

# === ТЕКСТЫ ИНСТРУКЦИЙ ===
instructions = {
    "T90": "Инструкция по T90: ...",
    "Dots 8s": "Инструкция по Dots 8s: ...",
    "G36": "Инструкция по G36: ...",
    "TWS MAX": "Инструкция по TWS MAX: ...",
    "F6-s": "Инструкция по F6-s: ...",
}

@bot.message_handler(func=lambda msg: msg.text in [
    "T90", "Dots 8s", "G36", "TWS MAX", "F6-s",
    "TWS Air 2Pods", "TWS PRO", "N13"
])
def model_selected(message):
    model = message.text
    if model in instructions:
        text = instructions[model]
    else:
        text = "На данную модель пока не вышла инструкция. Если вы столкнулись с проблемой, обратитесь в поддержку: @dolmartik"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Проблема не решена"), types.KeyboardButton("Назад"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "Проблема не решена")
def unresolved(message):
    bot.send_message(message.chat.id,
                     "Если не получилось решить проблему, обратитесь сюда: @dolmartik\n"
                     "Опишите, что случилось, добавьте фото и укажите модель, ФИО и номер телефона.")

@bot.message_handler(func=lambda msg: msg.text == "Назад")
def go_back(message):
    choose_model(message)

# === ВЕБХУК ===
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Бот работает!", 200

if __name__ == '__main__':
    if RAILWAY_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RAILWAY_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
