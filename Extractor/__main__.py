import asyncio
import importlib
import signal
from pyrogram import Client, filters, idle
from config import OWNER_ID
from Extractor.modules import ALL_MODULES

loop = asyncio.get_event_loop()

# -------------------- Graceful shutdown --------------------
should_exit = asyncio.Event()

def shutdown():
    print("Shutting down gracefully...")
    should_exit.set()  # triggers exit from idle

signal.signal(signal.SIGTERM, lambda s, f: loop.create_task(should_exit.set()))
signal.signal(signal.SIGINT, lambda s, f: loop.create_task(should_exit.set()))

# -------------------- Premium users storage --------------------
premium_users = {}

async def add_premium_handler(client, message):
    """Owner-only /add_premium handler"""
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

# -------------------- Bot bootstrap --------------------
app = Client("bot")  # aapka pyrogram client

async def sumit_boot():
    # Import all modules
    for all_module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + all_module)

    # Register premium handler
    app.add_handler(
        pyrogram.handlers.MessageHandler(
            add_premium_handler,
            filters.command("add_premium")
        )
    )

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    await idle()  # keeps the bot alive
    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

# -------------------- Main --------------------
if __name__ == "__main__":
    try:
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Cancel pending tasks to avoid "destroyed but pending" error
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        loop.close()
        print("Loop closed.")
