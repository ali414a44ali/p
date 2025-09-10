from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils.database import is_music_playing, music_on
from VeGa.utils.decorators import AdminRightsCheck
from VeGa.utils.inline import close_markup
from config import BANNED_USERS
from strings import get_string



@app.on_message(filters.command(["/resume","كمل"],"") & filters.channel)
async def resume_comcc(cli, message):
    _ = get_string("en")
    chat_id = message.chat.id
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await KIM.resume_stream(chat_id)
    await message.reply_text(_["admin_4"].format(message.chat.title))
    
    
    
    
    
    
@app.on_message(filters.command(["/resume", "كمل"], "") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await KIM.resume_stream(chat_id)
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
