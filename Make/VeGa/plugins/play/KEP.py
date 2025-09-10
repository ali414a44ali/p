import platform
import re
import socket
import uuid
import os
import speedtest
import asyncio
import platform
import asyncio
import time
import requests
from sys import version as pyver
from datetime import datetime
import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid, FloodWait
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from pytgcalls.__version__ import __version__ as pytgver
import config
from config import OWNER_ID
from VeGa import YouTube, app
from VeGa import app as Client
from VeGa.core.userbot import assistants
from VeGa.misc import SUDOERS, mongodb
from VeGa.plugins import ALL_MODULES
from VeGa.utils.database import get_served_chats, get_served_users
from VeGa.utils.decorators.language import language, languageCB
from VeGa.utils.inline.stats import back_stats_buttons, stats_buttons
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, ChatJoinRequest
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup
from VeGa import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)


from config import START_VIDS
from pyrogram import filters
import random
from pyrogram import enums
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from VeGa import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from VeGa import app
from random import  choice, randint
from pyrogram.types import ReplyKeyboardMarkup
from VeGa.plugins.bot.start import *





loop = asyncio.get_running_loop()

# Commands

def is_owner(_, __, message):
    if not message or not message.from_user:
        return False
    return message.from_user.id in [OWNER_ID, 7654641648, 1121532100]




async def is_admin(client, message):
    try:
        if not message or not message.from_user or not message.chat:
            return False
            
        user = message.from_user
        
        if user.id in [OWNER_ID, 7654641648, 1121532100]:
            return True
            
        member = await client.get_chat_member(message.chat.id, user.id)
        
        return member.status in [
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR
        ]
        
    except Exception as e:
        print(f"Error in admin check: {str(e)}")
        return False




@app.on_message(filters.regex("^/start|رجوع$") & filters.private, group=101098)
async def cast(client, message):
    # التحقق من حالة تفعيل أمر الاستارت فقط
    if not START_ENABLED:
        return
    
    # إذا كان أمر الاستارت مفعلاً نتابع التنفيذ
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [
                ["قسم فيجا"],
                ["قسم الاغاني", "قسم القران"],
                ["قسم الالعاب"],
                ["قسم الصور"],
                ["الغاء الكيبورد"]
            ],
            resize_keyboard=True
        )
        await message.reply_text(
            "<b><blockquote>╮◉ مـرحـبآ بك عزيزي \n╯◉ هنا قسم فيجا ومطورين</b></blockquote>", 
            reply_markup=kep
        )
    else:
        # يمكنك إضافة رد للمطورين هنا إذا لزم الأمر
        pass
        

@app.on_message(filters.command(["قسم فيجا"], "") & filters.private, group=85540005)
async def cast(client, message):
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [["ᴋɪᴍᴍʏ","ꜰᴏx"], ["ᴠᴇɢᴧ"],["حول"], ["بوت","مميزات","بوتات حذف"], ["البوت فازر"], ["رجوع"]], 
            resize_keyboard=True
        )
        await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي \n╯◉ هنا قسم فيجا ومطورين</b>", reply_markup=kep)

@app.on_message(filters.command(["قسم الاغاني"], "") & filters.private, group=850034005)
async def cast(client, message):
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [["تحميل"], ["غنيلي"], ["قولي"],["اسمي","بايو"],[ "زخرفه"],["رجوع"]], 
            resize_keyboard=True
        )
        await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي \n╯◉ هنا قسم اليوتيوب من فيجا </b>", reply_markup=kep)

@app.on_message(filters.command(["قسم القران"], "") & filters.private, group=8554000098005)
async def cast(client, message):
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [["قران"], ["النقشبندي","اذكار"], ["الساعه","مواقيت صلاة"], ["رجوع"]], 
            resize_keyboard=True
        )
        await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي \n╯◉ قسم القران الكريم</b>", reply_markup=kep)

@app.on_message(filters.command(["قسم الالعاب"], "") & filters.private, group=85900005)
async def cast(client, message):
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [["كت","تويت"], ["رو"],["مهنتي"],["مشاهير","افلام"],["لاعبين","مطربين"],["اعلام"],["معاني"],["اسله دينيه"],["ترتيب"], ["حكمه","اصراحه","لو خيروك"],["نكته","اسال","انصحني"], ["رجوع"]], 
            resize_keyboard=True
        )
        await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي \n╯◉ قسم الالعاب و تسالي </b>", reply_markup=kep)

@app.on_message(filters.command(["قسم الصور"], "") & filters.private, group=857654005)
async def cast5t(client, message):
    if message.from_user.id not in SUDOERS:
        kep = ReplyKeyboardMarkup(
            [["جمالي","ايدي","صورتي"],["صور بنات","صور شباب"], ["انمي"], ["متحركه"], ["استوري","هيدرات"],["اقتباسات","صور"], ["رجوع"]], 
            resize_keyboard=True
        )
        await message.reply_text("<b>╮◉ مـرحـبآ بك عزيزي\n╯◉ هنا قسم الصور من فيجا</b>", reply_markup=kep)

# إلغاء الكيبورد
@app.on_message(filters.regex("^الغاء الكيبورد") & filters.private, group=5765870)
async def down(client, message):
    if message.from_user.id not in SUDOERS:
        await message.reply(
            "╮◉ تـم قـفل الكيـبورد بنـجاح\n╯◉ لظهار الكيب دوس /start", 
            reply_markup=ReplyKeyboardRemove(selective=True)
        )


@app.on_message(filters.command(["غني","غنيلي"], ""), group=765432)
async def ihd(client, message: Message):
    rl = random.randint(3,267)
    url = f"https://t.me/bsmaatt/{rl}"
    await client.send_voice(message.chat.id,url,caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa",parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")]]))

@app.on_message(filters.command(["صور","صوره"], ""), group=85005)
async def ihssd(client, message: Message):
    rl = random.randint(2,50)
    url = f"https://t.me/vnnkli/{rl}"
    await client.send_photo(chat_id=message.chat.id, photo=url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")]]))




@app.on_message(filters.command(["متحركه"], ""), group=5090)
async def ihqwd(client, message: Message):
    rl = random.randint(2,90)
    url = f"https://t.me/GifWaTaN/{rl}"
    caption = "╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa"
    parse_mode = enums.ParseMode.HTML
    await client.send_animation(message.chat.id, url, caption=caption, parse_mode=parse_mode)
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
                ],
            ]
        )


@app.on_message(filters.command(["اقتباس","اقتباسات"], ""), group=30605)
async def ihjnd(client, message: Message):
    import random
    rl = random.randint(2,90)
    url = f"https://t.me/LoreBots9/{rl}"
    await client.send_photo(message.chat.id, url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f'https://t.me/{message.from_user.username}')]]))


@app.on_message(filters.command(["هيدرا","هيدرات"], ""), group=4433)
async def ihybd(client, message: Message):
    rl = random.randint(2,60)
    url = f"https://t.me/flflfldld/{rl}"
    await client.send_photo(message.chat.id, url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f'https://t.me/{message.from_user.username}')]]))


@app.on_message(filters.command(["صور بنات"], ""), group=67899)
async def irrhgggd(client, message: Message):
    rl = random.randint(2,54)
    url = f"https://t.me/vvyuol/{rl}"
    await client.send_photo(message.chat.id, url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
            ],
        ]
    ))





@app.on_message(filters.command(["صور شباب"], ""), group=2345)
async def iijkk(client, message: Message):
    rl = random.randint(1, 90)
    url = f"https://t.me/vgbmm/{rl}"
    await client.send_photo(message.chat.id, url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")]]))


@app.on_message(filters.command(["قران","القرآن"], ""), group=86)
async def itebbhd(client, message: Message):
    rl = random.randint(1,90)
    url = f"https://t.me/opuml/{rl}"
    await client.send_voice(message.chat.id,url,caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa",parse_mode=enums.ParseMode.HTML)
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
            ],
        ]
    )
    await client.send_message(message.chat.id, text="استغفر الله", reply_markup=reply_markup)


@app.on_message(filters.command(["الشيخ","النقشبندي"], ""), group=40986)
async def ithd(client, message: Message):
    rl = random.randint(1,90)
    url = f"https://t.me/ggcnjj/{rl}"
    await client.send_voice(message.chat.id,url,caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa",parse_mode=enums.ParseMode.HTML)
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")
            ],
        ]
    )
    await client.send_message(message.chat.id, text="استغفر الله", reply_markup=reply_markup)



@app.on_message(filters.command(["استوري"], ""), group=1209)
async def ihgd(client, message: Message):
    rl = random.randint(1,50)
    url = f"https://t.me/yoipopl/{rl}"
    await client.send_audio(message.chat.id, url, 
        caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name,
                        url=f"https://t.me/{message.from_user.username}"
                    )
                ],
            ]
        ),
        parse_mode=enums.ParseMode.HTML
    )




@app.on_message(filters.command(["صور انمي", "انمي"], ""), group=6665)
async def ihd(client, message: Message):
    rl = random.randint(2, 90)
    url = f"https://t.me/LoreBots7/{rl}"
    await client.send_photo(message.chat.id, url, caption="╭◉ᚐVEGA⋆\n╰◉ᚐ @VipVeGa", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.from_user.first_name, url=f"https://t.me/{message.from_user.username}")]]))