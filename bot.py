import json
import os
from aiogram import Bot, Dispatcher, executor, types

# =========================
# 1️⃣ Токен бота
# =========================
# НЕ вставляй токен прямо сюда!
# На PythonAnywhere лучше использовать переменные окружения:
#   Name: BOT_TOKEN
#   Value: <твой токен от BotFather>
from myconfig import BOT_TOKEN

API_TOKEN = BOT_TOKEN
bot = Bot(token=API_TOKEN)

# =========================
# 2️⃣ Файл для хранения пользователей
# =========================
# Можно оставить название "users.json", он будет создан автоматически
DB_FILE = "users.json"

# создаём файл, если его нет
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)

# =========================
# 3️⃣ Функции для работы с базой пользователей
# =========================
def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# =========================
# 4️⃣ Команда /start
# =========================
# Отправляет приветствие и добавляет пользователя в базу
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
    await message.answer(
        "Спасибо за активацию! 🎉 Теперь ты получаешь акции и новости ❤️"
    )

# =========================
# 5️⃣ Твой Telegram ID для рассылки
# =========================
# Замени 123456789 на свой реальный Telegram ID (число)
ADMIN_ID = 459856214  

# =========================
# 6️⃣ Команда /send для рассылки
# =========================
# Используется только админом (твой ID)
@dp.message_handler(commands=['send'])
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    # Текст рассылки берется из команды, например:
    # /send Привет, акция уже началась!
    text = message.get_args()
    if not text:
        await message.reply("Используй: /send ваш текст")
        return

    users = load_users()
    count = 0
    for u in users:
        try:
            await bot.send_message(u, text)
            count += 1
        except:
            pass

    await message.reply(f"Рассылка отправлена {count} пользователям ✔️")

# =========================
# 7️⃣ Запуск бота
# =========================
# skip_updates=True — бот не будет обрабатывать старые сообщения при старте
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
