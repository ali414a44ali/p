from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UsernameInvalid, PeerIdInvalid

from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import add_gban_user, remove_gban_user
from VeGa.utils.decorators.language import language
from config import BANNED_USERS

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ حظر مستخدم ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["حظر"], "") & filters.private & SUDOERS, group=655)
@language
async def block_user(client, message: Message, _):
    try:
        # ━━ التحقق من طريقة الإدخال
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            # ━━ طلب المعرف إذا لم يتم إدخاله
            ask = await message.reply_text("⌯︙يرجى إرسال **آيدي المستخدم** أو **يوزرنيمه**")
            
            try:
                response = await client.listen(
                    chat_id=message.chat.id,
                    filters=filters.text,
                    timeout=30
                )
                user_input = response.text.strip()
            except TimeoutError:
                return await ask.edit_text("⌯︙انتهى الوقت المخصص للإدخال!")
            finally:
                await ask.delete()

            # ━━ معالجة المدخلات
            try:
                if user_input.startswith("@"):
                    user = await client.get_users(user_input)
                else:
                    user_id = int(user_input)
                    user = await client.get_users(user_id)
            except (UsernameInvalid, PeerIdInvalid):
                return await message.reply_text("⌯︙المعرف غير صحيح أو غير موجود!")
            except ValueError:
                return await message.reply_text("⌯︙يجب إدخال آيدي رقمي صحيح!")

        # ━━ التحقق من الحظر المسبق
        if user.id in BANNED_USERS:
            return await message.reply_text(f"⌯︙المستخدم {user.mention} مُحظور بالفعل!")

        # ━━ تنفيذ الحظر
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(f"⌯︙تم حظر {user.mention} بنجاح ✅")

    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ إلغاء حظر مستخدم ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["الغاء حظر"], "") & filters.private & SUDOERS, group=626)
@language
async def unblock_user(client, message: Message, _):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            ask = await message.reply_text("⌯︙يرجى إرسال **آيدي المستخدم** أو **يوزرنيمه**")
            
            try:
                response = await client.listen(
                    chat_id=message.chat.id,
                    filters=filters.text,
                    timeout=30
                )
                user_input = response.text.strip()
            except TimeoutError:
                return await ask.edit_text("⌯︙انتهى الوقت المخصص للإدخال!")
            finally:
                await ask.delete()

            try:
                if user_input.startswith("@"):
                    user = await client.get_users(user_input)
                else:
                    user_id = int(user_input)
                    user = await client.get_users(user_id)
            except (UsernameInvalid, PeerIdInvalid):
                return await message.reply_text("⌯︙المعرف غير صحيح أو غير موجود!")
            except ValueError:
                return await message.reply_text("⌯︙يجب إدخال آيدي رقمي صحيح!")

        if user.id not in BANNED_USERS:
            return await message.reply_text(f"⌯︙المستخدم {user.mention} غير محظور!")

        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(f"⌯︙تم إلغاء حظر {user.mention} بنجاح ✅")

    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ قائمة المحظورين ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@app.on_message(filters.command(["المحظورين"], "") & filters.private & SUDOERS, group=43)
@language
async def blocked_users_list(client, message: Message, _):
    try:
        if not BANNED_USERS:
            return await message.reply_text("⌯︙لا يوجد مستخدمين محظورين حالياً")

        loading_msg = await message.reply_text("⌯︙جاري تجميع البيانات...")
        
        users_list = []
        success_count = 0
        
        for user_id in BANNED_USERS:
            try:
                user = await app.get_users(user_id)
                user_btn = InlineKeyboardButton(
                    text=f"{user.first_name}" if user.first_name else f"مستخدم ({user_id})",
                    url=f"tg://user?id={user_id}"
                )
                users_list.append([user_btn])
                success_count += 1
            except:
                continue

        if success_count == 0:
            await loading_msg.edit_text("⌯︙فشل جلب بيانات المحظورين")
        else:
            keyboard = InlineKeyboardMarkup(users_list)
            await loading_msg.edit_text(
                f"⌯︙قائمة المحظورين ({success_count} مستخدم):\n"
                "⌯︙اضغط على الأسماء للانتقال إلى الملفات الشخصية",
                reply_markup=keyboard
            )
            
    except Exception as e:
        await message.reply_text(f"⌯︙حدث خطأ: {str(e)}")