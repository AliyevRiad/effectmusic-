import asyncio
import importlib
import os
from threading import Thread
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from flask import Flask

import config
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# --- Minimal Flask server (Heroku $PORT üçün) ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "OK"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        raise SystemExit

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    await app.start()

    # DİQQƏT: burada nöqtə çatmırdı
    for all_module in ALL_MODULES:
        importlib.import_module(f"BrandrdXMusic.plugins.{all_module}")
    LOGGER("BrandrdXMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Hotty.start()

    try:
        await Hotty.stream_call("https://graph.org/file/e999c40cb700e7c684b75.mp4")
    except NoActiveGroupCall:
        LOGGER("FrozenXMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        raise SystemExit
    except Exception:
        pass

    await Hotty.decorators()
    LOGGER("FrozenXMusic").info(
        "ᴅʀᴏᴘ ʏᴏᴜʀ ɢɪʀʟꜰʀɪᴇɴᴅ'ꜱ ɴᴜᴍʙᴇʀ ᴀᴛ @Frozensupport1 ᴊᴏɪɴ @vibeshiftbots , @Frozensupport1"
    )

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("FrozenXMusic").info("Stopping Frozen Music Bot...")

if __name__ == "__main__":
    # Flask-i ayrıca thread-də qaldırırıq ki, Heroku $PORT-a bağlana bilsin
    Thread(target=run_flask).start()

    # Botun əsas asyncio loop-u
    asyncio.get_event_loop().run_until_complete(init())
