import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from VeGa import LOGGER, app, userbot
from VeGa.core.call import KIM
from VeGa.misc import sudo
from VeGa.plugins import ALL_MODULES
from VeGa.utils.database import get_banned_users, get_gbanned
from VeGa.utils.cookie_handler import fetch_and_store_cookies 
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("ᴀssɪsᴛᴀɴᴛ sᴇssɪᴏɴ ɴᴏᴛ ғɪʟʟᴇᴅ, ᴘʟᴇᴀsᴇ ғɪʟʟ ᴀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ...")
        exit()

    # ✅ Try to fetch cookies at startup
    try:
        await fetch_and_store_cookies()
        LOGGER("VeGa").info("ʏᴏᴜᴛᴜʙᴇ ᴄᴏᴏᴋɪᴇs ʟᴏᴀᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅")
    except Exception as e:
        LOGGER("VeGa").warning(f"⚠️ᴄᴏᴏᴋɪᴇ ᴇʀʀᴏʀ: {e}")


    await sudo()


    LOGGER("VeGa.plugins").info("ᴛᴜɴᴇ's ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")

    await userbot.start()
    await KIM.start()

    try:
        await KIM.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("VeGa").error(
            "ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n\nᴀɴɴɪᴇ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ..."
        )
        exit()
    except:
        pass

    await KIM.decorators()
    LOGGER("VeGa").info(
        "\x53\x6f\x75\x72\x63\x65\x20\x63\x6f\x64\x65\x20\x77\x61\x73\x20\x64\x65\x76\x65\x6c\x6f\x70\x65\x64\x20\x62\x79\x3a\x20\x40\x54\x6f\x70\x56\x65\x47\x61"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("VeGa").info("sᴛᴏᴘᴘɪɴɢ ᴛᴜɴᴇ ᴍᴜsɪᴄ ʙᴏᴛ ...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
