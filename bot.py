import asyncio
import csv
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN, ADMIN_ID
# ======== INIT BOT ========
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
router = Router()

# ======== USERS CSV ========

def save_user(user_id: int):
    if not os.path.exists("users.csv"):
        open("users.csv", "w").close()

    with open("users.csv", "r") as f:
        users = [int(row[0]) for row in csv.reader(f)]

    if user_id not in users:
        with open("users.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([user_id])

def get_users():
    if not os.path.exists("users.csv"):
        return []
    with open("users.csv", "r") as f:
        return [int(row[0]) for row in csv.reader(f)]

# ======== START ========

@router.message(Command("start"))
async def start_handler(message: Message):
    save_user(message.from_user.id)
    await message.answer("👋 Хуш омадед ба бот!")

# ======== ADMIN PANEL ========

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🔐 Панели админ\n\n"
        "/stats - Омор\n"
        "/broadcast матн - Рассылка"
    )

# ======== STATS ========

@router.message(Command("stats"))
async def stats_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    total = len(get_users())
    await message.answer(f"👥 Ҳамагӣ истифодабарандагон: {total}")

# ======== BROADCAST ========

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.reply_to_message:
        await message.answer("Ба ягон паём reply карда /broadcast навис.")
        return

    users = get_users()
    sent = 0

    for user_id in users:
        try:
            await message.reply_to_message.copy_to(user_id)
            sent += 1
        except:
            pass

    await message.answer(f"✅ Рассылка фиристода шуд ба {sent} нафар.")
# ======== RUN ========

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
