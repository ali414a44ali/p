import asyncio
import os
import asyncio
import random
from pyrogram import Client, filters



from config import *
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from VeGa import app
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
import asyncio
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait




array = []

@app.on_message(filters.command(["قفل تاك", "تعطيل التاك"], ""), group=277288870000127181882)
async def mooslock(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 6753126490 or message.from_user.id == 6760053475:
      if message.chat.id in array:
        return await message.reply_text("<b>التاك معطله من قبل</b>")
      array.append(message.chat.id)
      return await message.reply_text("<b>تم تعطيل تاك بنجاح</b>")
   else:
      return await message.reply_text("<b>هذا الامر يخص ❪ الادمن وفوق ❫ بس</b>")

@app.on_message(filters.command(["فتح تاك", "تفعيل التاك"], ""), group=726262766000288)
async def moosopen(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 6753126490 or message.from_user.id == 6760053475:
      if not message.chat.id in array:
        return await message.reply_text("<b>تاك مفعله من قبل</b>")
      array.remove(message.chat.id)
      return await message.reply_text("<b>تم تفعيل تاك بنجاح</b>")
   else:
      return await message.reply_text("<b>هذا الامر يخص ❪ الادمن وفوق ❫ بس</b>")



@app.on_message(filters.command(["@all", "تاك", "all"], "") & ~filters.private, group=767667)
async def mention_all(client, message):
    # التحقق من إيقاف التاك في المجموعة
    if message.chat.id in array:
        return await message.reply("<b>⛔ التاك معطلة في هذه المجموعة!</b>")
    
    # التحقق من صلاحيات المستخدم
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("<b>❌ هذا الأمر متاح فقط للمشرفين والمالك!</b>")
    except Exception as e:
        return await message.reply(f"<b>⚠️ حدث خطأ: {e}</b>")

    # الرد مرة واحدة فقط عند بدء التاك
    start_msg = await message.reply("<b>⏳ جاري بدء التاك...</b>")
    
    stats = {
        'deleted': 0,
        'no_username': 0,
        'success': 0,
        'no_mention': 0
    }
    
    batch_size = 20
    delay_between_messages = 1  
    txt = ""
    zz = message.text or message.caption or ""
    media = None
    media_type = None
    if message.photo:
        media = message.photo.file_id
        media_type = "photo"
    elif message.video:
        media = message.video.file_id
        media_type = "video"
    
    zz = zz.replace("@all", "").replace("تاك", "").replace("all", "").strip()
    
    array.append(message.chat.id)
    
    try:
        async for member in client.get_chat_members(message.chat.id):
            if message.chat.id not in array:
                break
                
            if member.user.is_deleted:
                stats['deleted'] += 1
                continue
                
            mention = member.user.mention if member.user.username else f"[{member.user.first_name or 'مستخدم'}](tg://user?id={member.user.id})"
            
            if not (member.user.username or member.user.first_name):
                stats['no_mention'] += 1
                continue
                
            stats['success'] += 1
            txt += f" {mention} ›"
            
            if stats['success'] % batch_size == 0: 
                try:
                    if media_type == "photo":
                        await client.send_photo(
                            chat_id=message.chat.id,
                            photo=media,
                            caption=f"{zz}\n{txt}" if zz else txt
                        )
                    elif media_type == "video":
                        await client.send_video(
                            chat_id=message.chat.id,
                            video=media,
                            caption=f"{zz}\n{txt}" if zz else txt
                        )
                    else:
                        await client.send_message(
                            chat_id=message.chat.id,
                            text=f"{zz}\n{txt}" if zz else txt
                        )
                    
                    txt = ""
                    await asyncio.sleep(delay_between_messages)
                
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    print(f"Error: {e}")
                    continue
    
        if txt and message.chat.id in array:
            try:
                if media_type == "photo":
                    await client.send_photo(
                        chat_id=message.chat.id,
                        photo=media,
                        caption=f"{zz}\n{txt}" if zz else txt
                    )
                elif media_type == "video":
                    await client.send_video(
                        chat_id=message.chat.id,
                        video=media,
                        caption=f"{zz}\n{txt}" if zz else txt
                    )
                else:
                    await client.send_message(
                        chat_id=message.chat.id,
                        text=f"{zz}\n{txt}" if zz else txt
                    )
            except Exception as e:
                print(f"Error sending final batch: {e}")
    
    finally:
        if message.chat.id in array:
            array.remove(message.chat.id)
        
        report_msg = (
            f"<b>✅ تم الانتهاء من التاك بنجاح!</b>\n\n"
            f"<b>• عدد المذكرين:</b> {stats['success']}\n"
            f"<b>• الحسابات المحذوفة:</b> {stats['deleted']}\n"
            f"<b>• الحسابات بدون معرف:</b> {stats['no_username']}\n"
            f"<b>• الحسابات غير القابلة للتذكير:</b> {stats['no_mention']}\n\n"
            f"<i>~ {message.chat.title}</i>"
        )
        await message.reply(report_msg)


@app.on_message(filters.command(["/cancel", "ايقاف التاك", "بس منشن"], ""), group=666111111)
async def stop_mention(client, message):
    # التحقق من صلاحيات المستخدم
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("<b>❌ هذا الأمر متاح فقط للمشرفين والمالك!</b>")
    except Exception as e:
        return await message.reply(f"<b>⚠️ حدث خطأ: {e}</b>")

    if message.chat.id not in array:
        return await message.reply("<b>⚠️ لا يوجد عملية تاك جارية لإيقافها!</b>")
    
    array.remove(message.chat.id)
    await message.reply("<b>⏹ تم إيقاف عملية التاك بنجاح!</b>", reply_to_message_id=message.id)




