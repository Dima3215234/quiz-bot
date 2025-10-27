import telebot
from telebot import types
import os

# 🔑 Берём токен из переменной окружения (Render → Environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Если запускаешь с компьютера — можешь просто вставить токен сюда:
# BOT_TOKEN = "твой_токен"

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Храним данные пользователей
user_data = {}

# 🔹 Вопросы викторины (пример, если их нет — добавь свои)
questions = [
    {
        "q": "Что тебе больше нравится?",
        "options": {
            "Рисовать и творить 🎨": "design",
            "Работать с компьютерами 💻": "it",
            "Помогать людям 🧠": "psy"
        }
    },
    {
        "q": "Что тебе интереснее?",
        "options": {
            "Создавать красивые вещи": "design",
            "Писать код и решать задачи": "it",
            "Разговаривать и понимать людей": "psy"
        }
    }
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Это мини-викторина, которая поможет определить, какая профессия тебе подходит.\n\nДля начала напиши своё *Имя и Фамилию*:",
        parse_mode="Markdown"
    )
    user_data[message.chat.id] = {"step": "name", "scores": {"design": 0, "it": 0, "psy": 0}}

@bot.message_handler(func=lambda m: m.chat.id in user_data)
def handle_message(message):
    user = user_data[message.chat.id]
    step = user["step"]

    # 🔸 Шаг 1: имя
    if step == "name":
        user["name"] = message.text.strip()
        user["step"] = "group"
        bot.send_message(message.chat.id, "📘 Отлично! Теперь напиши номер своей группы (например: *3-25*):", parse_mode="Markdown")

    # 🔸 Шаг 2: группа
    elif step == "group":
        user["group"] = message.text.strip()
        user["step"] = 0  # начинаем викторину
        bot.send_message(message.chat.id, f"✅ Спасибо, {user['name']} из группы {user['group']}!\n\nТеперь начнём викторину 🎯")
        ask_question(message.chat.id)

    # 🔸 Шаги викторины
    elif isinstance(step, int):
        if step < len(questions):
            q = questions[step]
            answer = message.text
            if answer in q["options"]:
                sphere = q["options"][answer]
                user["scores"][sphere] += 1
                user["step"]
