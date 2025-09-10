import asyncio
import random
import json
from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
from pyrogram import enums
import json
from VeGa import app
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from pyrogram import filters, Client

import asyncio
import config
import re
import os
import requests
from os import getenv
from pyrogram import Client, filters
from VeGa import app
from config import OWNER_ID
from pyrogram import filters, Client
from pyrogram import filters
from pyrogram import Client
from typing import Union
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from VeGa.misc import SUDOERS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup
from pyrogram.types import (InlineKeyboardButton,CallbackQuery,InlineKeyboardMarkup, Message)
from VeGa.utils.database import (set_cmode,get_assistant)
from pyrogram.types import (InlineKeyboardButton, ChatPermissions, InlineKeyboardMarkup, Message, User)
from datetime import datetime
from pyrogram import enums
from config import OWNER_ID
from pyrogram.errors import MessageNotModified


from pyrogram.types import CallbackQuery

from pyrogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from VeGa import app
from pyrogram.types import ChatPermissions, ChatPrivileges
from config import *
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup                           
import asyncio
from VeGa import (Apple, Resso, SoundCloud, Spotify, Telegram)
from VeGa import app
import pyrogram
from VeGa.misc import SUDOERS
from emoji import emojize
from config import *
from pyrogram import filters
from config import OWNER_ID
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.enums import ParseMode
from VeGa import app
from VeGa.utils.database import is_on_off
from config import LOGGER_ID


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
#──██████──────██████───█████████████──────██████████████───████████████████────
#──██──██──────██──██───██─────────██────██────────────██───██────────────██────
#──██──██──────██──██───██──█████████───██───████████████───██───███████──██────
#──██──██──────██──██───██──██──────────██──██──────────────██───██───██──██────
#──██──██──────██──██───██──██──────────██──██──────────────██───██───██──██────
#──██──██──────██──██───██──██──────────██──██──────────────██───██───██──██────
#──██──██──────██──██── ██──██──────────██──██──────────────██───██───██──██───
#──██──██──────██──██───██──█████████───██──██───███████────██───███████──██────
#──██───██────██───██───██─────────██───██──██───██────██───██────────────██────
#───██───██──██───██────██──█████████───██──██───████──██───██───███████──██────
#────██───████───██─────██──██──────────██──██─────██──██───██───██───██──██────
#─────██───██───██──────██──██──────────██───██────██──██───██───██───██──██────
#──────██──────██───────██──██───────────██───██───██──██───██───██───██──██────
#───────██────██────────██──█████████─────██──███████──██───██───██───██──██────
#────────██──██─────────██─────────██──────██─────────██────██───██───██──██────
#─────────████──────────█████████████───────████████████────███████───██████────
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ̷𝖾𝙙𝙚𝙥𝙡𝙤𝙮𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮
# (2024-2025) 𝙗𝙮: @𝙏𝙊𝙋𝙑𝙀𝙂𝘼
# 𝙂𝙧𝙚𝙚𝙩𝙞𝙣𝙜𝙨 𝙛𝙧𝙤𝙢 : 𝙑𝙚𝙂𝙖

 

# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

abraagof = []
@app.on_message(filters.command(["قفل الابراج", "تعطيل الابراج"], ""), group=277288870000127181882)
async def abraaglock(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 6753126490 or message.from_user.id == 6760053475:
      if message.chat.id in abraagof:
        return await message.reply_text("الابراج معطله من قبل")
      abraagof.append(message.chat.id)
      return await message.reply_text("تم تعطيل الابراج بنجاح")
   else:
      return await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")

@app.on_message(filters.command(["فتح الابراج", "تفعيل الالابراج"], ""), group=720288)
async def abraagopen(client, message):
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 6753126490 or message.from_user.id == 6760053475:
      if not message.chat.id in abraagof:
        return await message.reply_text("الابراج مفعله من قبل\n")
      abraagof.remove(message.chat.id)
      return await message.reply_text("تم تفعيل الابراج بنجاح")
   else:
      return await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")





user = ""

@app.on_message(filters.command(["الابراج", "ابراج"], ""), group=78281)
async def mmmfdsfy(client: Client, message: Message):
    global user
    user = message.from_user.id
    if message.chat.id in abraagof:
        return await message.reply_text("الاوامر معطله من قبل الادمن")
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    await message.reply_photo(
        photo="https://telegra.ph/file/394d47db7f99cfe7473e8.jpg",
        caption=f" ˚‧VEGA˳+\n╮❖ مـرحـبـا بـك: {message.from_user.mention()}\n╯❖ لـيك قـايـمـة الابراج مـن فيـجـا",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "꙳.الجدي.꙳", callback_data="gatyy"),
                        
                    InlineKeyboardButton(
                        "꙳.الدلو.꙳", callback_data="dalooo"),
               ],[
                    InlineKeyboardButton(
                        "꙳.الحوت.꙳", callback_data="hood"),
                    InlineKeyboardButton(
                    "꙳.الحمل.꙳", callback_data="haamal"),
               ],[
                    InlineKeyboardButton(
                    "꙳.الثور.꙳", callback_data="elsoor"),
                    InlineKeyboardButton(
                    "꙳.الجوزاء.꙳", callback_data="gwzaa"),
               ],[
                    InlineKeyboardButton(
                        "꙳.السرطان.꙳", callback_data="sltaan"),
                    InlineKeyboardButton(
                        "꙳.الأسد.꙳", callback_data="asat"),
               ],[
                    InlineKeyboardButton(
                        "꙳.العذراء.꙳", callback_data="azrraa"),
                    InlineKeyboardButton(
                        "꙳.الميزان.꙳", callback_data="mezan"),
               ],[
                    InlineKeyboardButton(
                        "꙳.العقرب.꙳", callback_data="akrrab"),
                    InlineKeyboardButton(
                        "꙳.القوس.꙳", callback_data="koss"),
               ],[
                    InlineKeyboardButton("ᴠᴇɢᴧ", url=SUPPORT_CHANNEL),
                ],
            ]
        )
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


@app.on_callback_query(filters.regex("abraag"), group=186382)
async def mpdtsf(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
        
    await query.answer("abraagg")
    await query.edit_message_text(
        f"""<b> ˚‧VEGA˳+\n╮❖ تنويه هام:- هذا ليس حقيقيا\n╯❖ وانما يعلم الغيب سيد الخلائق</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                     InlineKeyboardButton(
                            "꙳.الجدي.꙳", callback_data="gatyy"),
                     InlineKeyboardButton(
                            "꙳.الدلو.꙳", callback_data="dalooo"),
                ],[
                     InlineKeyboardButton(
                            "꙳.الحوت.꙳", callback_data="hood"),
                     InlineKeyboardButton(
                        "꙳.الحمل.꙳", callback_data="haamal"),
                ],[
                     InlineKeyboardButton(
                        "꙳.الثور.꙳", callback_data="elsoor"),
                     InlineKeyboardButton(
                        "꙳.الجوزاء.꙳", callback_data="gwzaa"),
                ],[
                     InlineKeyboardButton(
                            "꙳.السرطان.꙳", callback_data="sltaan"),
                    InlineKeyboardButton(
                            "꙳.الأسد.꙳", callback_data="asat"),
                ],[
                    InlineKeyboardButton(
                            "꙳.العذراء.꙳", callback_data="azrraa"),
                    InlineKeyboardButton(
                            "꙳.الميزان.꙳", callback_data="mezan"),
                ],[
                    InlineKeyboardButton(
                            "꙳.العقرب.꙳", callback_data="akrrab"),
                    InlineKeyboardButton(
                            "꙳.القوس.꙳", callback_data="koss"),
                ],[
                    InlineKeyboardButton("ᴠᴇɢᴧ", url=SUPPORT_CHANNEL),
                ],
            ]
        )
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


@app.on_callback_query(filters.regex("gatyy"), group=1487877)
async def gatyyyy(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("gatyy")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الجدي ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳━━
عاطفيا || \n:  حاول ترطيب الأجواء مع الشريك، بعد ثورة الغضب التي انتابتك في الأيام الماضية 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n لا تنجرّ وراء محاولات استدراجك إلى أن تثور وتغضب لتعريض وضعك الصحي للخطر
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يدعوك هذا اليوم المليء بالسلبيات إلى عدم التورط في قضايا أكبر منك، وخصوصاً أن رياح التغيير بدأت تعصف باتجاهك
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("dalooo"), group=12324)
async def daloooj(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("dalooo")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الدلو ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳.꙳
عاطفيا || \n:  لا تتسرّع في الموافقة على قرار مهم قبل أن تدرس الوضع من جميع جوانبه، لأن الندم قد لا يفيدك لاحقاً 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n لكي تحافظ على صحتك السليمة، ما عليك سوى ممارسة الرياضة ثلاث مرات على الأقل في الأسبوع
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  هذا اليوم يفرض عليك أن تنظر إلى الأمور بطريقة أخرى، وأن تتعلّم كيف تحوّل الخسارة إلى ربح
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )
    
   
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


    
@app.on_callback_query(filters.regex("hood"), group=14976799)
async def hoodgh(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("hood")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الحوت ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  صداقة قديمة تعود إلى الواجهة عن طريق المصادفة، لكنّ الشريك يشعر بالقلق، فسارع إلى توضيح الأمور 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n لا تستسلم للإحباط بسبب وضعك الصحّي المتردي نوعاً ما، بل كن متسلّحاً بالتفاؤل
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يرّوج بعض الزملاء الإشاعات عن وضعك، لكنّك تبقى صلباً وتحديداً في المركز المهم الذي أسنده إليك أرباب العمل
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )    
    
    
  
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("haamal"), group=18778994)
async def haaymal(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("haamal")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الحمل ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  يحتاج الشريك اليوم إلى عاطفتك واهتمامك أكثر من أي وقت مضى، فاستمع إليه وأمن له ما يتمنّاه 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n القيام ببعض التمارين الخفيفة صباحاً تساعد على تليين العضلات وخصوصاً عضلات العنق الكتفين
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  قد يطرأ اليوم ما يهدد ببعض المشاريع على الصعيد المهني ويكون المناخ ضاغطاً جداً وملبداً بغيوم المشاكل
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )
        
        
        
        


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


@app.on_callback_query(filters.regex("elsoor"), group=1497688)
async def elsoortt(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("elsoor")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الثور ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  يطلب منك الشريك أن تعطيه جواباً حاسماً بشأن طبيعة العلاقة بينكما، من دون أن يغفل عن أمور تهمكما 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n ترتاح من تعب أرهقك جداً وأبقاك في حالة صحية متذبذبة ومضطربة بعض الشيء
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  حاول ألاّ توظف طاقتك في مشاريع صغيرة لا خطط واضحة لها، وانتظر حتى تعرض عليك المشاريع الكبيرة
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("gwzaa"), group=14976789)
async def gwzaauu(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("gwzaa")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الجوزاء ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  مهمة إقناع الشريك بالسير معك حتى النهاية ليست صعبة، وتجاربه السابقة معك مشجعة جداً 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n أنت المسؤول عما آل إليه وضعك الصحي، لأنك لم تلتزم إرشادات الطبيب ولم تطبقها
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يطرأ اليوم ما يبشر بيوم دقيق من التجارب المرة، لكن النجاح يكون حليفك في نهاية المطاف</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )    


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("sltaan"), group=1866784)
async def sltaanhh(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("sltaan")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
━━❪❪ برج السرطان ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  تمنحك مساندة الحبيب لك في هذه المرحلة الاندفاع والتفاؤل في الحياة والتفكير في الخطوات المقبلة بثقة كبيرة جداً 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n انتبه لصحتك وانظر إلى الخيارات المتاحة أمامك للمحافظة عليها معافاة
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يحمل إليك هذا اليوم كلمات الإطراء والمديح والتهنئة، فيسطع نجمك وتبدأ بمشروع جديد
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )



# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("asat"), group=11220982334)
async def azrrttaatg(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("azryyraa")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الاسد ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  لا تحمّل الشريك مسؤولية الأخطاء القديمة، وحاول أن تتخطى ذلك برحابة صدر وبساطة 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n التدخين والإفراط في شرب الكحول والسهر سرعان ما تظهر نتائجهما على صحتك
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  قد يجعلك هذا اليوم تتردّد في تسلم مهمة مع أنك تمتلك القدرة على ذلك وتحقيق النجاح المطلوب
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )

# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

            
@app.on_callback_query(filters.regex("azrraa"), group=1122239734)
async def azrraatg(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("azrraa")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج العذراء ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  تشعر بقوة العاطفة وتزداد رغبتك في التقرّب من الشريك الذي تكنّ له الحب الكبير 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n إذا أحسست أن وضعك الصحي يتحسّن، فهذا جراء تطبيق إرشادات أصحاب الاختصاص في مجال التغذية
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يولّد هذا اليوم كلاماً غير مقنع أو لا يتمتّع بمصداقية، فتحاول معرفة الأسباب الكامنة وراء كل ما يحصل وتنجح في ذلك
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂


                        
@app.on_callback_query(filters.regex("mezan"), group=187431174)
async def mezannn(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("mezan")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج الميزان ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  تمرّ بظرف صعب اليوم وأنت بأمسّ الحاجة إلى مساندة الشريك لتجاوز ما تواجهه بأقل ضرر ممكن 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n تنضم إلى إحدى الفرق أو المجموعات الرياضية وتواظب على المشاركة في جميع أنشطتها فتستفيد صحياً
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  يجعلك هذا اليوم تشغل نفسك بأمور صغيرة لن تنفعك بشيء، بل بالعكس قد تضيّع لك وقتك، وأنت بحاجة ماسة إلى كل ثانية
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )




# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂



@app.on_callback_query(filters.regex("akrrab"), group=1409325877)
async def akrrabtt(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("akrrabuu")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج العقرب ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  كثرة التأجيل في حسم الأمور المصيرية تهدد علاقتك بالشريك، وتدفعها إلى المزيد من التأزم 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n قد تشعر بضيق في النفس وباضطراب مفاجئ في الرئتين بسبب إدمانك التدخين
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  قد يعرقل طارئ هذا اليوم تقدمك في مجالك المهني، لكنك قادر على تخطي المصاعب مهما تكن شديدة
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )


# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

              

@app.on_callback_query(filters.regex("koss"), group=148766436877)
async def gatyy(client, query: CallbackQuery):
    global user
    chat = query.message.chat
    get = await client.get_chat_member(chat.id, query.from_user.id)
    user_status = get.status
    if query.from_user.id != user:
        await client.answer_callback_query(query.id, text="هييه مايمديك الامر ياروعه!!", show_alert=True)
        return

    await client.answer_callback_query(query.id)
    
    await query.answer ("gyy")
    await query.edit_message_text(
        f"""<b><b>⭓ᴍᴜˢɪᴄ✘ᴠᴇɢᴧ♪</b>
       
━━❪❪ برج القوس ❫❫━━
مــن :- تاريخ 2024-4-1
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
عاطفيا || \n:  كن طويل البال مع الشريك وامنحه مزيداً من الوقت، فهو ساعدك كثيراً ويستحق منك بعض التضحية 
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
صحياً ||\n تجنّب قدر الإمكان الأماكن الرطبة ولا سيما أنك تعاني الربو وضيقاً في التنفس
꙳.━━━━❰❪ VeGa ❫❱━━━━━.꙳
مهنياً ||\n  قد يفقدك هذا اليوم الظروف المشجعة على التحرّك والاستثمار وتوظيف الأموال وتحقيق الأرباح
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("˹➻ٰ", callback_data="abraag")]]
        ),
    )
    

# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂
# ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂[𝗩.𝗘.𝗚.𝗔]▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂

