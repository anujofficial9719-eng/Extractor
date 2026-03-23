from pyrogram import filters, types
from config import OWNER_ID
from main import dp  # ya jahan dp define hai

premium_users = {}

@dp.message_handler(commands=["add_premium"])
async def add_premium(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.reply("❌ Sirf owner hi premium add kar sakta hai.")
        return

    args = message.text.split()[1:]
    if len(args) < 2:
        await message.reply("⚠️ Usage: /add_premium user_id time")
        return

    user_id = int(args[0])
    time = " ".join(args[1:])
    premium_users[user_id] = time

    await message.reply(f"✅ User {user_id} ko {time} ke liye premium diya gaya.")
