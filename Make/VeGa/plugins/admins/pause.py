from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils.database import is_music_playing, music_off
from VeGa.utils.decorators import AdminRightsCheck
from VeGa.utils.inline import close_markup
from config import BANNED_USERS
from strings import get_string









@app.on_message(filters.command(["/pause","وقف","اسكت"],"") & filters.channel)
async def pause_admin(cli, message):
    _ = get_string("en")
    chat_id = message.chat.id
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await KIM.pause_stream(chat_id)
    await message.reply_text(_["admin_2"].format(message.chat.title))
    




@app.on_message(filters.command(["/pause", "وقف"], "") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await KIM.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
