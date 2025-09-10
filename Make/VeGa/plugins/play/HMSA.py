from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType, ChatMemberStatus
from config import SUPPORT_CHANNEL
import os
from typing import Dict, Union
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os


from pyrogram.types import (Message,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery,ChatPrivileges)
from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pyrogram.types import *
from pyrogram import enums
from typing import Union, List, Iterable
from datetime import datetime
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import ChatPermissions, ChatPrivileges
from pyrogram.types import (InlineKeyboardButton, ChatPermissions, InlineKeyboardMarkup, Message, User)
import sys
from pyrogram import Client as client
from pyrogram.errors import FloodWait
from pyrogram import Client, idle
from random import randint
from pyrogram.enums import ChatType
from pyrogram.types import (InlineKeyboardButton,CallbackQuery,InlineKeyboardMarkup, Message)
from config import *
from random import choice
from telegraph import upload_file
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup

import asyncio
import string
import os
import time
import requests
from pyrogram import filters
import random
import aiohttp
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from VeGa import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from VeGa import app
from random import  choice, randint
from pytube import Search
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from VeGa import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from VeGa import app
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.enums import ChatType, ChatMemberStatus, UserStatus
from config import SUPPORT_CHANNEL
from typing import Dict, Union
import random
from datetime import datetime

# تخزين الهمسات
hms_storage: Dict[int, Dict[int, Dict[str, Union[str, int]]]] = {}
waiting_for_hms = False
hms_ids = ""



@app.on_message(
    filters.reply & 
    filters.regex(r"^(همسه|اهمس)$") & 
    filters.group, 
    group=12
)
async def reply_with_link(client, message):
    # التحقق من أن الرد ليس على بوت
    if message.reply_to_message.from_user.is_bot:
        await message.reply_text("صحصح هذا البوت!!")
        return


    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply_text("لا يمكنك إرسال همسة لنفسك!")
        return
        
    bot_username = (await client.get_me()).username
    user_id = message.reply_to_message.from_user.id
    my_id = message.from_user.id
    chat_id = message.chat.id
    hms_id = random.randint(1000, 9999)
    
    start_link = f"https://t.me/{bot_username}?start=hms{my_id}to{user_id}in{chat_id}id{hms_id}"
    
    try:
        user = await client.get_users(user_id)
        mention = user.mention
    except:
        mention = f"المستخدم ({user_id})"
    
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("اضغط لإرسال الهمسه!", url=start_link)]
        ]
    )  
    await message.reply_text(
        f"**• تم تحديد الهمسه لـ ↤︎ •{mention} •\n اضغط الزر لكتابة الهمسة -**", 
        reply_markup=reply_markup
    )

@app.on_message(filters.command("start"), group=5790)
async def hms_start(client, message): 
    global waiting_for_hms, hms_ids
    bot_username = (await client.get_me()).username
    
    if len(message.command) > 1 and message.command[1].startswith("hms"):
        hms_ids = message.command[1]
        waiting_for_hms = True
        await message.reply_text(
            "-> **أرسل الهمسه الآن (يمكنك إرسال نص، صورة، فيديو، صوت، ملصق، أو أي ميديا)**.\n√", 
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("إلغاء ❌️", callback_data="hms_cancel")
            ]])
        )

@app.on_message(filters.private & ~filters.command("start"), group=576)
async def send_hms(client, message): 
    global waiting_for_hms, hms_ids
    
    if waiting_for_hms:    
        try:
            parts = hms_ids.split("to")
            from_id = int(parts[0][3:]) 
            
            parts = parts[1].split("in")
            to_id = int(parts[0])
            parts = parts[1].split("id")
            chat_id = int(parts[0])
            hms_id = int(parts[1])
            receiver = await client.get_users(to_id)
            if receiver.is_bot:
                await message.reply_text("صحصح هذا البوت!!")
                waiting_for_hms = False
                return
            
            sender = await client.get_users(from_id)
            
            if to_id not in hms_storage:
                hms_storage[to_id] = {}
            content = {"type": "unsupported", "content": "نوع الملف غير مدعوم"}
            
            if message.text:
                content = {"type": "text", "content": message.text}
            elif message.photo:
                content = {"type": "photo", "content": message.photo.file_id}
            elif message.video:
                content = {"type": "video", "content": message.video.file_id}
            elif message.audio:
                content = {"type": "audio", "content": message.audio.file_id}
            elif message.voice:
                content = {"type": "voice", "content": message.voice.file_id}
            elif message.sticker:
                content = {"type": "sticker", "content": message.sticker.file_id}
            elif message.document:
                content = {"type": "document", "content": message.document.file_id}
            
            hms_storage[to_id][hms_id] = {
                "content": content,
                "chat_id": chat_id,
                "from_id": from_id,
                "timestamp": datetime.now().timestamp()
            }
            
            await message.reply_text(f"-> تم ارسال الهمسه لـ {receiver.first_name} بنجاح")
            if content["type"] != "unsupported":
                message_text = (
                    f"<b>• الهمسه لـ [{receiver.first_name}](tg://user?id={to_id})\n</b>"
                    f"<b>• من :  [{sender.first_name}](tg://user?id={from_id})\n</b>"
                    f"-"
                )
                
                await client.send_message(
                    chat_id=chat_id,
                    text=message_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("• رؤية الهمسه •", callback_data=f"hms_answer_{to_id}_{hms_id}")],
                        [InlineKeyboardButton("ᴠᴇɢᴀ", url=SUPPORT_CHANNEL)]
                    ])
                )
            else:
                await message.reply_text("-> نوع الملف غير مدعوم للهمسات!\n×")

        except Exception as e:
            await message.reply_text(f"حدث خطأ: {e}")
        finally:
            waiting_for_hms = False

@app.on_callback_query(filters.regex(r"^hms_answer_(\d+)_(\d+)$"), group=888890)
async def display_hms(client, callback):  
    data_parts = callback.data.split("_")
    target_user_id = int(data_parts[2])
    hms_id = int(data_parts[3])
    current_user_id = callback.from_user.id
    
    # التحقق من أن المستخدم الحالي هو المستهدف
    if current_user_id != target_user_id:
        await callback.answer("🚫 هذه الهمسة ليست لك!", show_alert=True)
        return
        
    if target_user_id not in hms_storage or hms_id not in hms_storage[target_user_id]:
        await callback.answer("⏳ هذه الهمسة انتهت صلاحيتها!", show_alert=True)
        return
    
    content = hms_storage[target_user_id][hms_id]["content"]
    from_id = hms_storage[target_user_id][hms_id]["from_id"]
    timestamp = hms_storage[target_user_id][hms_id].get("timestamp", datetime.now().timestamp())
    time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        sender = await client.get_users(from_id)
        sender_name = sender.first_name
        sender_link = f"tg://user?id={from_id}"
    except:
        sender_name = "مجهول"
        sender_link = ""
    
    if content["type"] == "text":
        # إظهار الرسالة كنافذة منبثقة أولاً
        await callback.answer(content["content"], show_alert=True)
        # ثم إرسال تأكيد في المحادثة
        await callback.message.reply_text("✓ تم عرض الهمسة لك في النافذة المنبثقة")
    elif content["type"] in ["photo", "video", "audio", "voice", "sticker", "document"]:
        try:
            media_types = {
                "photo": "صورة",
                "video": "فيديو",
                "audio": "صوت",
                "voice": "بصمة",
                "sticker": "ملصق",
                "document": "ملف"
            }
            media_type_name = media_types.get(content["type"], content["type"])
            
            caption = (f"**همستك المطلوبة**\n\n"
                     f"**╮◉  النوع:** {media_type_name}\n"
                     f"**┃᚜◉ المرسل: **[{(sender_name)}]({sender_link})\n"
                     f"**╯◉  الوقت:** {time_str}") if content["type"] not in ["sticker", "voice"] else None
            
            # إرسال الميديا مع رسالة تأكيد
            await client.send_cached_media(
                chat_id=callback.from_user.id,
                file_id=content["content"],
                caption=caption
            )
            await callback.answer("✓ تم إرسال الهمسة إليك في الخاص", show_alert=True)
            await callback.message.reply_text("✓ تم إرسال الهمسة إليك في الرسائل الخاصة")
        except Exception as e:
            await callback.answer(f"خطأ في إرسال الميديا: {e}", show_alert=True)
            await callback.message.reply_text("❌ حدث خطأ أثناء إرسال الرجاء قم بضغط /start بداخل البوت\nلكي يقوم بتعرف عليكً")
    else:
        await callback.answer("نوع الهمسة غير مدعوم", show_alert=True)
        await callback.message.reply_text("❌ نوع الهمسة غير مدعوم")
    
    # حذف الهمسة بعد عرضها
    if target_user_id in hms_storage and hms_id in hms_storage[target_user_id]:
        del hms_storage[target_user_id][hms_id]
    
@app.on_callback_query(filters.regex("hms_cancel"), group=769800)
async def cancel_hms(client, callback):  
    global waiting_for_hms
    waiting_for_hms = False  
    await callback.message.edit_text("-> تم إلغاء الهمسه!\n√")