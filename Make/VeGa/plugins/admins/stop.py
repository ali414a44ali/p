from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils.database import set_loop
from VeGa.utils.decorators import AdminRightsCheck
from VeGa.utils.inline import close_markup
from config import BANNED_USERS
from strings import get_string






@app.on_message(filters.command(["/end", "/stop","ايقاف","انهاء"],"") & filters.channel)
async def stop_musiccc(cli, message):
    _ = get_string("en")
    chat_id = message.chat.id
    if not len(message.command) == 1:
        return
    await KIM.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.chat.title), reply_markup=close_markup(_)
    )

@app.on_message(
    filters.command(["/end","ايقاف", "إيقاف","/stop"], "") & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await KIM.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
