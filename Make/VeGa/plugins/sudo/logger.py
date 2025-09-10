from pyrogram import filters

from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import add_off, add_on
from VeGa.utils.decorators.language import language
        
        
        
@app.on_message(filters.command(["/logger", "تفعيل السجل", "تشغيل السجل"], "") & SUDOERS, group=555)
@language
async def enable_logger(client, message, _):
    await add_on(2)
    await message.reply_text(_["log_2"]) 
        
        
        
@app.on_message(filters.command(["ايقاف السجل", "تعطيل السجل"], "") & SUDOERS, group=556)
@language
async def disable_logger(client, message, _):
    await add_off(2)
    await message.reply_text(_["log_3"])