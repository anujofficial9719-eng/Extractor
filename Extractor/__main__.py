import asyncio
import importlib
import signal
import os  # ✅ added
from aiohttp import web  # ✅ added
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

# -------------------- Web Server (Render Fix) --------------------
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)

    runner = web.AppRunner(app_web)
    await runner.setup()

    port = int(os.environ.get("PORT", 5000))  # ✅ important
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
    print(f"🌐 Web server started on port {port}")

# -------------------- Pyrogram client with persistent session --------------------
app = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -------------------- Premium handler registration --------------------
@app.on_message(filters.command("add_premium"))
async def handle_add_premium(client, message):
    await premium.add_premium_handler(message)

# -------------------- Bot bootstrap --------------------
async def sumit_boot():
    # Import all modules dynamically
    for module_name in ALL_MODULES:
        importlib.import_module("Extractor.modules." + module_name)

    # ✅ Start web server (ADDED, nothing removed)
    asyncio.create_task(web_server())

    print("» ʙᴏᴛ ᴅᴇᴘʟᴏʏ sᴜᴄᴄᴇssғᴜʟʟʏ ✨ 🎉")
    await idle()
    print("» ɢᴏᴏᴅ ʙʏᴇ ! sᴛᴏᴘᴘɪɴɢ ʙᴏᴛ.")

# -------------------- Run --------------------
if __name__ == "__main__":
    try:
        app.start()
        loop.run_until_complete(sumit_boot())
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        pending = asyncio.all_tasks(loop)
        for task in pending:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        app.stop()
        loop.close()
        print("Loop closed.")
