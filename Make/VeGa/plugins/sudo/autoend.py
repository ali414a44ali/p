from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import autoend_off, autoend_on


@app.on_message(filters.command(["تفعيل المغادره تلقائي"], "") & SUDOERS, group=55433)
async def auto_end_stream_on(_, message: Message):
    if await is_autoend_on():  # إذا كانت الميزة مفعلة أصلاً
        await message.reply_text("⦿ الإنهاء التلقائي مفعل بالفعل!")
    else:
        await autoend_on()
        await message.reply_text(
            "⦿ تم تفعيل الإنتهاء التلقائي بنجاح.\n\n"
            "✓ سيقوم المساعد بمغادرة الدردشة تلقائياً\n"
            "✓ عند عدم وجود مستمعين بعد عدة دقائق"
        )

@app.on_message(filters.command(["تعطيل المغادره تلقائي"], "") & SUDOERS, group=50555)
async def auto_end_stream_off(_, message: Message):
    if not await is_autoend_on():  # إذا كانت الميزة معطلة أصلاً
        await message.reply_text("⦿ الإنهاء التلقائي معطل بالفعل!")
    else:
        await autoend_off()
        await message.reply_text("⦿ تم تعطيل الإنتهاء التلقائي بنجاح.")