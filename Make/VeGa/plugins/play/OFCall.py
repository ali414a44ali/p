import asyncio
import os
from typing import Optional
from PIL import Image, ImageFilter
from pyrogram import Client, filters
from pyrogram.types import Message, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, Message, CallbackQuery
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from pyrogram.raw.types import (
    InputGroupCall,
    InputPeerChannel,
    InputPeerChat,
    InputPeerUser
)
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import (
    CreateGroupCall,
    DiscardGroupCall
)
from pytgcalls import PyTgCalls
from VeGa.misc import db
from pytgcalls.exceptions import NoActiveGroupCall  # تم إزالة AlreadyJoinedError
from pytgcalls.types import MediaStream
from VeGa import app
from VeGa.core.call import KIM
from VeGa.core.call import*
from VeGa.utils.database import get_assistant
from config import OWNER_ID

# وظيفة فتح المكالمة الجماعية
async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    try:
        assistant = await get_assistant(message.chat.id)
        chat_peer = await assistant.resolve_peer(message.chat.id)
        
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await assistant.invoke(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (await assistant.invoke(GetFullChat(chat_id=chat_peer.chat_id))).full_chat
        else:
            await app.send_message(message.chat.id, f"**نوع الدردشة غير مدعوم** {err_msg}")
            return None
            
        if full_chat is not None and hasattr(full_chat, 'call'):
            return full_chat.call
            
        await app.send_message(message.chat.id, f"**لا توجد مكالمة جماعية** {err_msg}")
        return None
    except Exception as e:
        await app.send_message(message.chat.id, f"**خطأ في الحصول على المكالمة: {str(e)}**")
        return None

@app.on_message(filters.regex(r"^(افتح الكول|فتح الكول)$") & (filters.group | filters.channel), group=53)
async def start_group_call(client: Client, message: Message):
    try:
        # التحقق من صلاحيات المستخدم
        if not message.from_user:
            return await message.reply("**⚠️ لا يمكن تحديد هوية المستخدم**")
            
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        allowed_statuses = [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
        allowed_users = [OWNER_ID, 6909581339]  # يمكنك إضافة المزيد من المستخدمين المصرح لهم
        
        if get.status not in allowed_statuses and message.from_user.id not in allowed_users:
            return await message.reply("**🚫 هذا الأمر للمشرفين فقط!**")
        
        chat_id = message.chat.id
        assistant = await get_assistant(chat_id)
        
        if not assistant:
            return await message.reply("**⚠️ خطأ في المساعد**")
            
        ass = await assistant.get_me()
        assid = ass.id
        
        # التحقق من وجود مكالمة نشطة بالفعل
        existing_call = await get_group_call(assistant, message)
        if existing_call:
            return await message.reply("**✅ المكالمة الجماعية مفتوحة بالفعل!**")
        
        msg = await message.reply("**🔄 جاري فتح المكالمة الجماعية...**")
        
        try:
            peer = await assistant.resolve_peer(chat_id)
            
            # معالجة مختلفة للقنوات والمجموعات
            if isinstance(peer, InputPeerChannel):
                await assistant.invoke(
                    CreateGroupCall(
                        peer=InputPeerChannel(
                            channel_id=peer.channel_id,
                            access_hash=peer.access_hash,
                        ),
                        random_id=assistant.rnd_id() // 9000000000,
                    )
                )
            elif isinstance(peer, InputPeerChat):
                await assistant.invoke(
                    CreateGroupCall(
                        peer=InputPeerChat(chat_id=peer.chat_id),
                        random_id=assistant.rnd_id() // 9000000000,
                    )
                )
            
            await msg.edit("**✅ تم فتح المكالمة الجماعية بنجاح**")
            
        except ChatAdminRequired:
            try:
                # منح الصلاحيات المطلوبة للمساعد
                await app.promote_chat_member(
                    chat_id, 
                    assid, 
                    privileges=ChatPrivileges(
                        can_manage_video_chats=True,
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    )
                )
                
                # إعادة محاولة إنشاء المكالمة
                peer = await assistant.resolve_peer(chat_id)
                if isinstance(peer, InputPeerChannel):
                    await assistant.invoke(
                        CreateGroupCall(
                            peer=InputPeerChannel(
                                channel_id=peer.channel_id,
                                access_hash=peer.access_hash,
                            ),
                            random_id=assistant.rnd_id() // 9000000000,
                        )
                    )
                elif isinstance(peer, InputPeerChat):
                    await assistant.invoke(
                        CreateGroupCall(
                            peer=InputPeerChat(chat_id=peer.chat_id),
                            random_id=assistant.rnd_id() // 9000000000,
                        )
                    )
                
                # إزالة الصلاحيات بعد الإنشاء
                await app.promote_chat_member(
                    chat_id, 
                    assid, 
                    privileges=ChatPrivileges(
                        can_manage_video_chats=False,
                        can_manage_chat=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_change_info=False,
                        can_invite_users=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                    )
                )
                
                await msg.edit("**✅ تم فتح المكالمة الجماعية بنجاح**")
            except Exception as e:
                error_msg = f"""
**⚠️ فشل في فتح المكالمة الجماعية**

**السبب:** تحتاج إلى منح البوت الصلاحيات التالية:
- إدارة المحادثات المرئية (الفيديو)
- صلاحية المشرف

**الخطأ التفصيلي:** {str(e)}
"""
                await msg.edit(error_msg)
        except Exception as e:
            await msg.edit(f"**⚠️ حدث خطأ غير متوقع: {str(e)}**")
            
    except Exception as e:
        await message.reply(f"**⚠️ حدث خطأ: {str(e)}**")

@app.on_message(filters.regex(r"^(اقفل الكول|قفل الكول)$") & (filters.group | filters.channel), group=53)
async def stop_group_call(client: Client, message: Message):
    try:
        # التحقق من صلاحيات المستخدم
        if not message.from_user:
            return await message.reply("**⚠️ لا يمكن تحديد هوية المستخدم**")
            
        get = await client.get_chat_member(message.chat.id, message.from_user.id)
        allowed_statuses = [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
        allowed_users = [OWNER_ID, 6909581339]  # يمكنك إضافة المزيد من المستخدمين المصرح لهم
        
        if get.status not in allowed_statuses and message.from_user.id not in allowed_users:
            return await message.reply("**🚫 هذا الأمر للمشرفين فقط!**")
        
        chat_id = message.chat.id
        assistant = await get_assistant(chat_id)
        
        if not assistant:
            return await message.reply("**⚠️ خطأ في المساعد**")
            
        ass = await assistant.get_me()
        assid = ass.id
        
        # التحقق من وجود مكالمة نشطة
        group_call = await get_group_call(assistant, message)
        if not group_call:
            return await message.reply("**⚠️ لا توجد مكالمة نشطة!**")
        
        msg = await message.reply("**🔄 جاري إغلاق المكالمة الجماعية...**")
        
        try:
            await assistant.invoke(DiscardGroupCall(call=group_call))
            await msg.edit("**✅ تم إغلاق المكالمة الجماعية بنجاح**")
            
        except Exception as e:
            if "GROUPCALL_FORBIDDEN" in str(e):
                try:
                    # منح الصلاحيات المطلوبة للمساعد
                    await app.promote_chat_member(
                        chat_id, 
                        assid, 
                        privileges=ChatPrivileges(
                            can_manage_video_chats=True,
                            can_manage_chat=False,
                            can_delete_messages=False,
                            can_restrict_members=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                            can_promote_members=False,
                        )
                    )
                    
                    # إعادة المحاولة بعد منح الصلاحيات
                    group_call = await get_group_call(assistant, message)
                    if not group_call:
                        return await msg.edit("**⚠️ لا توجد مكالمة نشطة!**")
                        
                    await assistant.invoke(DiscardGroupCall(call=group_call))
                    
                    # إزالة الصلاحيات بعد الإغلاق
                    await app.promote_chat_member(
                        chat_id, 
                        assid, 
                        privileges=ChatPrivileges(
                            can_manage_video_chats=False,
                            can_manage_chat=False,
                            can_delete_messages=False,
                            can_restrict_members=False,
                            can_change_info=False,
                            can_invite_users=False,
                            can_pin_messages=False,
                            can_promote_members=False,
                        )
                    )
                    
                    await msg.edit("**✅ تم إغلاق المكالمة الجماعية بنجاح**")
                except Exception as e:
                    error_msg = f"""
**⚠️ فشل في إغلاق المكالمة الجماعية**

**السبب:** تحتاج إلى منح البوت الصلاحيات التالية:
- إدارة المحادثات المرئية (الفيديو)
- صلاحية المشرف

**الخطأ التفصيلي:** {str(e)}
"""
                    await msg.edit(error_msg)
            else:
                await msg.edit(f"**⚠️ حدث خطأ غير متوقع: {str(e)}**")
                
    except Exception as e:
        await message.reply(f"**⚠️ حدث خطأ: {str(e)}**")

# وظيفة تشويش الصور
@app.on_message(filters.command(["تشويش"], ""), group=1262)
async def blur_image(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("⚠️ يرجى الرد على صورة لتطبيق التشويش عليها")
        return
    
    try:
        msg = await message.reply_text("⏳ جاري معالجة الصورة...")
        photo_path = await message.reply_to_message.download()
        
        with Image.open(photo_path) as img:
            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=15))
            blurred_path = "blurred_" + os.path.basename(photo_path)
            blurred_img.save(blurred_path, quality=95)
        
        await msg.delete()
        await message.reply_to_message.reply_photo(
            blurred_path,
            caption="تم تطبيق التشويش على الصورة ✅"
        )
        
    except Exception as e:
        await message.reply_text(f"❌ حدث خطأ أثناء معالجة الصورة: {str(e)}")
    
    finally:
        if 'photo_path' in locals() and os.path.exists(photo_path):
            os.remove(photo_path)
        if 'blurred_path' in locals() and os.path.exists(blurred_path):
            os.remove(blurred_path)

# معالجات أحداث المكالمات
@app.on_message(filters.video_chat_started)
async def call_started(client: Client, message: Message): 
    Startt = "<b>ارحب نظرو من هنا</b>"
    await message.reply_text(Startt)

@app.on_message(filters.video_chat_ended)
async def call_ended(client: Client, message: Message): 
    Enddd = "<b>قـفـله فـي دمـاغـك 😒</b>"
    await message.reply_text(Enddd)

@app.on_message(filters.video_chat_members_invited)
async def members_invited(client: Client, message: Message): 
    text = f"<b>╮⦿ قـام: {message.from_user.mention}\n╯⦿ بـدعـوه : </b>"
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a> "
            x += 1
        except Exception:
            pass
    try:
        await message.reply_text(f"{text}")
    except Exception:
        pass


KIM = Call()

@app.on_message(filters.regex("^(مين في الكول|من في الكول)$"), group=854367796)
async def who_in_call(client, message: Message):
    try:
        # تهيئة العميل إذا لم يكن قد بدأ بعد
        if not getattr(KIM, '_initialized', False):
            await KIM.start()
            KIM._initialized = True

        chat_id = message.chat.id
        assistant = await group_assistant(KIM, chat_id)
        
        # حذف الرسالة المؤقتة بعد ثانيتين
        msg = await message.reply("🔍")
        await asyncio.sleep(1)
        await msg.delete()
        
        try:
            # الانضمام إلى المحادثة الصوتية مع تشغيل فيديو
            stream_call = MediaStream(
                "https://files.catbox.moe/lp5v8n.mp4",
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.HD_720p
            )
            await assistant.play(chat_id, stream_call)
        except Exception as e:
            if "already in this chat" not in str(e):
                print(f"Error joining call: {e}")
        
        # جلب قائمة المشاركين
        try:
            participants = await assistant.get_participants(chat_id)
            if not participants:
                return await message.reply("❌ لا يوجد أحد في المكالمة الصوتية")
            
            # بناء رسالة الرد
            text = "🎤 <b>الأعضاء الموجودون في المكالمة:</b>\n\n"
            for idx, member in enumerate(participants, start=1):
                try:
                    user_obj = await client.get_users(member.user_id)
                    user_mention = user_obj.mention
                except:
                    user_mention = f"المستخدم ({member.user_id})"
                
                # الحصول على معلومات العضو في الدردشة
                try:
                    chat_member = await message.chat.get_member(member.user_id)
                    # تحديد الدور
                    if chat_member.status == ChatMemberStatus.OWNER:
                        role = "👑 (المالك)"
                    elif chat_member.status == ChatMemberStatus.ADMINISTRATOR:
                        role = "🔧 (مشرف)"
                    else:
                        role = "👤 (عضو كلب)"
                except:
                    role = "👤 (عضو)"
                
                # تحديد الحالة
                status = []
                if getattr(member, 'is_hand_raised', False):
                    status.append("✋ يرفع يده")
                if getattr(member, 'video', False):
                    status.append("🎥 الكاميرا فيديو")
                if getattr(member, 'screen_sharing', False):
                    status.append("🖥️ مشاركة شاشة")
                if getattr(member, 'muted', False) and not getattr(member, 'can_self_unmute', True):
                    status.append("🔇 مكتوم (إجباري)")
                elif not getattr(member, 'muted', False):
                    status.append("🎤 يتحدث")
                if getattr(member, 'left', False):
                    status.append("🚫 غادر المكالمة")
                
                text += f"<b>{idx} - {user_mention}\n {role}</b>\n"
                if status:
                    text += f" ({' | '.join(status)})"
                text += "\n"
            
            text += f"\n<b>العدد الإجمالي:</b> {len(participants)}\n"
            
            await message.reply(text)
            
        except Exception as e:
            await message.reply(f"❌ حدث خطأ أثناء جلب المشاركين: {str(e)}")
            print(f"Error getting participants: {e}")
        
        # المغادرة بعد 15 ثانية إذا لم يكن هناك تشغيل نشط
        await asyncio.sleep(15)
        if chat_id not in db or not db[chat_id]:
            try:
                await assistant.leave_call(chat_id)
            except Exception as e:
                print(f"Error leaving call: {e}")
            
    except Exception as e:
        print(f"Error in who_in_call: {e}")
        await message.reply("❌ حدث خطأ غير متوقع أثناء تنفيذ الأمر")
        
        
        

# KIM = Call()

# @app.on_message(filters.regex("^(مين في الكول|من في الكول)$"), group=854367796)
# async def who_in_call(client, message: Message):
    # try:
        # # تهيئة العميل إذا لم يكن قد بدأ بعد
        # if not getattr(KIM, '_initialized', False):
            # await KIM.start()
            # KIM._initialized = True

        # chat_id = message.chat.id
        # assistant = await group_assistant(KIM, chat_id)
        
        # # حذف الرسالة المؤقتة بعد ثانيتين
        # msg = await message.reply("🔍")
        # await asyncio.sleep(1)
        # await msg.delete()
        
        # try:
            # # الانضمام إلى المحادثة الصوتية مع تشغيل فيديو
            # stream_call = MediaStream(
                # "https://files.catbox.moe/lp5v8n.mp4",
                # audio_parameters=AudioQuality.STUDIO,
                # video_parameters=VideoQuality.HD_720p
            # )
            # await assistant.play(chat_id, stream_call)
        # except Exception as e:
            # if "already in this chat" not in str(e):
                # print(f"Error joining call: {e}")
        
        # # جلب قائمة المشاركين
        # try:
            # participants = await assistant.get_participants(chat_id)
            # if not participants:
                # return await message.reply("❌ لا يوجد أحد في المكالمة الصوتية")
            
            # # بناء رسالة الرد
            # text = "🎤 <b>الأعضاء الموجودون في المكالمة:</b>\n\n"
            # for idx, user in enumerate(participants, start=1):
                # try:
                    # user_obj = await client.get_users(user.user_id)
                    # user_mention = user_obj.mention
                # except:
                    # user_mention = f"المستخدم ({user.user_id})"
                
                # text += f"{idx} - {user_mention}\n"
            
            # text += f"\n<b>العدد الإجمالي:</b> {len(participants)}\n"
            
            # await message.reply(text)
            
        # except Exception as e:
            # await message.reply(f"❌ حدث خطأ أثناء جلب المشاركين: {str(e)}")
            # print(f"Error getting participants: {e}")
        
        # # المغادرة بعد 5 ثواني إذا لم يكن هناك تشغيل نشط
        # await asyncio.sleep(15)
        # if chat_id not in db or not db[chat_id]:
            # try:
                # await assistant.leave_call(chat_id)
            # except Exception as e:
                # print(f"Error leaving call: {e}")
            
    # except Exception as e:
        # print(f"Error in who_in_call: {e}")
        # await message.reply("❌ حدث خطأ غير متوقع أثناء تنفيذ الأمر")