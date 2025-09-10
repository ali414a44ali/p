from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UsernameInvalid, PeerIdInvalid

from config import BANNED_USERS, OWNER_ID
from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import add_sudo, remove_sudo
from VeGa.utils.decorators.language import language
from VeGa.utils.extraction import extract_user

# ─── Add Sudo ─────────────────────────────────────────────
SUDORS = [OWNER_ID]


@app.on_message(filters.command(["اضف مطور"], "") & filters.private & filters.user(OWNER_ID), group=234455)
@language
async def add_sudo_user(client, message: Message, _):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            ask = await message.reply_text("⌯︙يرجى إرسال **آيدي المستخدم** أو **يوزرنيمه**")
            try:
                response = await client.listen(
                    chat_id=message.chat.id,
                    filters=filters.text & filters.private,
                    timeout=30
                )
                user_input = response.text.strip()
            except TimeoutError:
                return await ask.edit_text("⌯︙انتهى الوقت المخصص للإدخال!")
            finally:
                await ask.delete()

            try:
                user = await client.get_users(user_input)
            except (UsernameInvalid, PeerIdInvalid):
                return await message.reply_text("⌯︙المستخدم غير موجود أو المعرف خاطئ!")

        if user.id in SUDOERS:
            return await message.reply_text(f"⌯︙المستخدم {user.mention} موجود بالفعل في قائمة المطورين!")

        if await add_sudo(user.id):
            SUDOERS.add(user.id)
            await message.reply_text(f"⌯︙تمت إضافة {user.mention} إلى المطورين بنجاح ✅")
        else:
            await message.reply_text("⌯︙فشل إضافة المستخدم!")

    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")

# ─── Remove Sudo ───────────────────────────────────────────

@app.on_message(filters.command(["rmsudo"], "") & filters.private & filters.user(OWNER_ID), group=4333)
@language
async def remove_sudo_user(client, message: Message, _):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            ask = await message.reply_text("⌯︙يرجى إرسال **آيدي المستخدم** أو **يوزرنيمه**")
            try:
                response = await client.listen(
                    chat_id=message.chat.id,
                    filters=filters.text & filters.private,
                    timeout=30
                )
                user_input = response.text.strip()
            except TimeoutError:
                return await ask.edit_text("⌯︙انتهى الوقت المخصص للإدخال!")
            finally:
                await ask.delete()

            try:
                user = await client.get_users(user_input)
            except (UsernameInvalid, PeerIdInvalid):
                return await message.reply_text("⌯︙المستخدم غير موجود أو المعرف خاطئ!")

        if user.id not in SUDOERS:
            return await message.reply_text(f"⌯︙المستخدم {user.mention} غير موجود في قائمة المطورين!")

        if await remove_sudo(user.id):
            SUDOERS.remove(user.id)
            await message.reply_text(f"⌯︙تمت إزالة {user.mention} من المطورين بنجاح ✅")
        else:
            await message.reply_text("⌯︙فشل إزالة المستخدم!")

    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")

# ─── Sudo List ─────────────────────────────────────────────

@app.on_message(filters.command(["listsudo", "sudoers"], "") & filters.private & ~BANNED_USERS, group=224)
@language
async def sudoers_list(client, message: Message, _):
    if not SUDOERS:
        return await message.reply_text("⌯︙لا يوجد مطورين مضافين حالياً!")
    
    try:
        owner = await app.get_users(OWNER_ID)
        text = f"**𓆰 قائمة مطورين البوت 𓆪**\n\n**👑 المالك:** {owner.mention}\n\n"
        keyboard = []

        count = 1
        for user_id in SUDOERS:
            if user_id == OWNER_ID:
                continue
            try:
                user = await app.get_users(user_id)
                text += f"**𓂅 المطور {count}:** {user.mention}\n"
                keyboard.append([InlineKeyboardButton(f"عرض المطور {count}", url=f"tg://user?id={user_id}")])
                count += 1
            except:
                continue

        keyboard.append([InlineKeyboardButton("𓂑 اغلاق", callback_data="close")])
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")

# ─── Delete All Sudo ───────────────────────────────────────

@app.on_message(filters.command("delallsudo", prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.private & filters.user(OWNER_ID))
@language
async def remove_all_sudo_users(client, message: Message, _):
    try:
        if len(SUDOERS) == 0:
            return await message.reply_text("⌯︙لا يوجد مطورين لحذفهم!")
        
        count = 0
        for user_id in list(SUDOERS):
            if user_id != OWNER_ID:
                if await remove_sudo(user_id):
                    SUDOERS.remove(user_id)
                    count += 1
        
        await message.reply_text(f"⌯︙تم حذف {count} مطورين بنجاح ✅")
    
    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")