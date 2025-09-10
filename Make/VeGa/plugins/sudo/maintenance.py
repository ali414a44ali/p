from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


@app.on_message(filters.command(["تفعيل البوت"], "") & SUDOERS, group=1121109)
async def maintenance_on_command(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    
    if await is_maintenance():
        await message.reply_text(_["maint_4"])
    else:
        await maintenance_on()
        await message.reply_text(_["maint_2"].format(app.mention))

@app.on_message(filters.command(["تعطيل البوت"], "") & SUDOERS, group=6556)
async def maintenance_off_command(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    
    if not await is_maintenance():
        await message.reply_text(_["maint_5"])
    else:
        await maintenance_off()
        await message.reply_text(_["maint_3"].format(app.mention))