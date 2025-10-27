import telebot
from telebot import types
import os

# 🔑 Токен берётся из переменной окружения Render (Environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ⚠️ Если запускаешь с компьютера — можешь раскомментировать строку ниже и вставить токен вручную
# BOT_TOKEN = "8046565380:AAHpWTI-A6juTxj7DZs4I66g2CmnDn1CC1M"

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Вопросы викторины
questions = [
    {
        "q": "Что тебе больше нравится?",
        "options": {"🎨 Рисовать и создавать": "design", "💻 Решать задачи и кодить": "it", "💬 Общаться и помогать людям": "psy"}
    },
    {
        "q": "Какой предмет тебе ближе?",
        "options": {"🖌 Изо": "design", "🧮 Информатика": "it", "📘 Обществознание": "psy"}
    },
    {
        "q": "Что ты делаешь в свободное время?",
        "options": {"📷 Редактирую фото/видео": "design", "🎮 Играю или создаю что-то на компе": "it", "👥 Советуюсь с друзьями": "psy"}
    },
    {
        "q": "Что тебе интереснее?",
        "options": {"🎭 Цвета, шрифты, формы": "design", "⚙️ Коды, программы, логика": "it", "❤️ Чувства, люди, отношения": "psy"}
    },
    {
        "q": "Что бы ты выбрал?",
        "options": {"🖼 Создать постер": "design", "🕹 Написать игру": "it", "📊 Провести опрос": "psy"}
    },
    {
        "q": "Что тебе даётся легче?",
        "options": {"✏️ Придумывать оформление": "design", "🔢 Решать логические задачи": "it", "🗣 Объяснять другим": "psy"}
    },
    {
        "q": "Какую профессию выбрал бы?",
        "options": {"👨‍🎨 Дизайнер": "design", "👨‍💻 Программист": "it", "👩‍🏫 Психолог": "psy"}
    },
    {
        "q": "Что важнее в работе?",
        "options": {"✨ Красота и стиль": "design", "📏 Точность и логика": "it", "🤝 Понимание людей": "psy"}
    },
    {
        "q": "Как ты относишься к команде?",
        "options": {"🎨 Хочу делать красиво вместе": "design", "🚀 Главное — результат": "it", "💬 Люблю помогать коллегам": "psy"}
    },
    {
        "q": "Кем ты видишь себя через 5 лет?",
        "options": {"🎨 Дизайнером": "design", "💻 Разработчиком": "it", "🧠 Психологом": "psy"}
    }
]

# 🔹 Храним данные пользователей
user_data = {}

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

    if step == "name":
        user["name"] = message.text.strip()
        user["step"] = "group"
        bot.send_message(message.chat.id, "📘 Отлично! Теперь напиши номер своей группы (например: *3-25*):", parse_mode="Markdown")

    elif step == "group":
        user["group"] = message.text.strip()
        user["step"] = 0
        bot.send_message(message.chat.id, f"✅ Спасибо, {user['name']} из группы {user['group']}!\n\nТеперь начнём викторину 🎯")
        ask_question(message.chat.id)

    elif isinstance(step, int):
        if step < len(questions):
            q = questions[step]
            answer = message.text
            if answer in q["options"]:
                sphere = q["options"][answer]
                user["scores"][sphere] += 1
                user["step"] += 1
                ask_question(message.chat.id)
            else:
                bot.send_message(message.chat.id, "⚠️ Пожалуйста, выбери один из предложенных вариантов.")
        else:
            finish_quiz(message.chat.id)

def ask_question(chat_id):
    user = user_data[chat_id]
    step = user["step"]

    if step < len(questions):
        q = questions[step]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in q["options"].keys():
            markup.add(option)
        bot.send_message(chat_id, f"❓ {q['q']}", reply_markup=markup)
    else:
        finish_quiz(chat_id)

def finish_quiz(chat_id):
    user = user_data[chat_id]
    scores = user["scores"]
    best = max(scores, key=scores.get)

    results = {
        "design": "🎨 Тебе подойдёт направление *Дизайн*! У тебя отличный вкус и творческое мышление!",
        "it": "💻 Тебе подойдёт направление *IT*! Ты логичный, внимательный и любишь технологии!",
        "psy": "🧠 Тебе подойдёт направление *Психология*! Ты понимаешь людей и умеешь слушать!"
    }

    bot.send_message(chat_id, f"✨ Викторина окончена!\n\n{results[best]}", parse_mode="Markdown")
    bot.send_message(chat_id, "Спасибо за участие! 🌟", reply_markup=types.ReplyKeyboardRemove())
    del user_data[chat_id]

print("✅ Бот запущен и работает...")
bot.polling(none_stop=True)
