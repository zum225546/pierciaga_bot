import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "8564121416:AAGhF4-7PwUnSKeIBlwd-22jGaJUDWEHJ1c"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DB_FILE = "users.json"


def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_id = message.from_user.id
    users = load_users()

    if user_id not in users:
        users.append(user_id)
        save_users(users)

    await message.answer("Спасибо за активацию! 🎉 Теперь ты получаешь акции и новости ❤️")


ADMIN_ID = ТВОЙ_TELEGRAM_ID  # потом подскажешь — я скажу, что здесь поставить


@dp.message_handler(commands=['send'])
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

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


if __name__ == "__main__":
    executor.start_polling(dp)
