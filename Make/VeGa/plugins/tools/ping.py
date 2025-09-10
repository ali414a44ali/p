from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from config import *
from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils import bot_sys_stats
from VeGa.utils.decorators.language import language
from VeGa.utils.inline import supp_markup
from config import BANNED_USERS, PING_VID_URL


@app.on_message(filters.command(["/ping", "بينج","بنج"], "") & ~BANNED_USERS, group=34)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_video(
        video=PING_VID_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await KIM.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
