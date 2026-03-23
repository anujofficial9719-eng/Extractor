import asyncio
import importlib
import signal
from pyrogram import Client, filters, idle
from config import BOT_TOKEN, API_ID, API_HASH, OWNER_ID
from Extractor.modules import ALL_MODULES
from Extractor.modules import premium  # premium.py import

# -------------------- Asyncio loop --------------------
loop = asyncio.get_event_loop()
should_exit = asyncio.Event()

def shutdown():
    print("Shutting down gracefully...")
    should_exit.set()

signal.signal(signal.SIGTERM, lambda s, f: loop.create_task(should_exit.set()))
signal.signal(signal.SIGINT, lambda s, f: loop.create_task(should_exit.set()))

# -------------------- Pyrogram client --------------------
app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# -------------------- Premium handler registration --------------------
@app.on_message(filters.command("add_premium"))
async def handle_add_premium(client, message):
    await premium.add_premium_handler(message)

# -------------------- Bot bootstrap --------------------
async def sumit_boot():
    # Import all modules dynamically
    for module_name in ALL_MODULES:
        importlib.import_module("Extractor.modules." + module_name)

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    await idle()  # keeps the bot running
    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

# -------------------- Run --------------------
if __name__ == "__main__":
    try:
        app.start()  # start pyrogram client
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        app.stop()  # stop pyrogram client gracefully
        loop.close()
        print("Loop closed.")
