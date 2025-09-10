from pyrogram import filters
from pyrogram.types import Message

from VeGa import app
from VeGa.utils import extract_user, int_to_alpha
from VeGa.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from VeGa.utils.decorators import AdminActual, language
from VeGa.utils.inline import close_markup
from config import BANNED_USERS, adminlist
from strings import get_string

@app.on_message(filters.command(["اعتماد"], "") & filters.group & ~BANNED_USERS, group=511211121)
@AdminActual
async def auth(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)
    if int(count) == 25:
        return await message.reply_text("❌ وصلت الحد الأقصى للمستخدمين المصرح لهم (25 مستخدم)")
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        get = adminlist.get(message.chat.id)
        if get:
            if user.id not in get:
                get.append(user.id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(f"✅ تم تفويض المستخدم {user.mention} بنجاح")
    else:
        return await message.reply_text(f"⚠️ المستخدم {user.mention} مفوض بالفعل")


@app.on_message(filters.command(["الغاء اعتماد","الغاء الاعتماد"], "") & filters.group & ~BANNED_USERS, group=522111)
@AdminActual
async def unauthusers(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    deleted = await delete_authuser(message.chat.id, token)
    get = adminlist.get(message.chat.id)
    if get:
        if user.id in get:
            get.remove(user.id)
    if deleted:
        return await message.reply_text(f"✅ تم إلغاء تفويض المستخدم {user.mention} بنجاح")
    else:
        return await message.reply_text(f"⚠️ المستخدم {user.mention} غير مفوض أصلاً")


@app.on_message(
    filters.command(["قائمة المعتدين", "المعتمدين"], "") & filters.group & ~BANNED_USERS, group=5444
)
@language
async def authusers(client, message: Message, _):
    _wtf = await get_authuser_names(message.chat.id)
    if not _wtf:
        return await message.reply_text("ℹ️ لا يوجد مستخدمين مفوضين في هذه المجموعة")
    else:
        j = 0
        mystic = await message.reply_text("⏳ جاري جلب قائمة المفوضين...")
        text = f"📜 قائمة المستخدمين المصرح لهم في {message.chat.title}:\n\n"
        for umm in _wtf:
            _umm = await get_authuser(message.chat.id, umm)
            user_id = _umm["auth_user_id"]
            admin_id = _umm["admin_id"]
            admin_name = _umm["admin_name"]
            try:
                user = (await app.get_users(user_id)).first_name
                j += 1
            except:
                continue
            text += f"{j}➤ {user}[<code>{user_id}</code>]\n"
            text += f"   🛠 تم التفويض بواسطة: {admin_name}[<code>{admin_id}</code>]\n\n"
        await mystic.edit_text(text, reply_markup=close_markup(_))