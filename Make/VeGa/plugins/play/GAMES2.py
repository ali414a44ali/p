
import asyncio
import re
import os
import random
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery)
from config import OWNER_ID
from VeGa import app
from VeGa.utils.database import set_cmode
from VeGa.utils.decorators.admins import AdminActual
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


import asyncio
import requests
from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils.database import set_loop
from VeGa.utils.decorators import AdminRightsCheck
from datetime import datetime
from config import BANNED_USERS, lyrical, START_VIDS, MONGO_DB_URI, OWNER_ID
from VeGa.utils import bot_sys_stats
from VeGa.utils.decorators.language import language
import random
import time
from pyrogram.enums import ChatMembersFilter
from pyrogram.enums import ChatMemberStatus
from aiohttp import ClientSession
from traceback import format_exc
import config
import re
import string
from pyrogram import enums
import lyricsgenius as lg
from pyrogram.types import (InlineKeyboardButton, ChatPermissions, InlineKeyboardMarkup, Message, User)
from pyrogram import Client, filters
from VeGa import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from typing import Union
import sys
import os
from asyncio import sleep


from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import random
import time

# تعريف فئات اللعبة
class Player:
    def __init__(self, name, attack_power, defense_power, is_legend=False):
        self.name = name
        self.attack = attack_power
        self.defense = defense_power
        self.is_legend = is_legend

class Team:
    def __init__(self, user_id):
        self.user_id = user_id
        self.players = []
        self.attackers = []
        self.defenders = []
        self.legends = []
        self.training_cooldown = 0
        self.cup_joined = False
        self.points = 0
        self.matches_played = 0
        self.matches_won = 0

class Database:
    def __init__(self):
        self.teams = {}
    
    def get_team(self, user_id):
        if user_id not in self.teams:
            self.teams[user_id] = Team(user_id)
        return self.teams.get(user_id)
    
    def save_team(self, user_id, team):
        self.teams[user_id] = team
    
    def get_top_teams(self):
        sorted_teams = sorted(self.teams.values(), key=lambda x: x.points, reverse=True)
        return sorted_teams[:10]

db = Database()
user_states = {}



@app.on_message(filters.command(["انشي فريق", "انشاء فريق","نوادي","نادي","النوادي"], ""), group=765555)
async def create_team(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if len(team.players) >= 6:
        return await message.reply("❌ لديك فريق بالفعل!")
    
    # إنشاء 6 لاعبين عشوائيين للمستخدم
    player_names = ["أحمد", "شيكابالا", "كهرباء", "خالد", "محمود", "ياسر", "حسن", "عمر", "مصطفى", "إبراهيم"]
    team.players = [
        Player(
            name=f"{random.choice(player_names)} {random.choice(player_names)}",
            attack_power=random.randint(5, 15),
            defense_power=random.randint(5, 15)
        ) for _ in range(6)
    ]
    
    db.save_team(user_id, team)
    
    players_list = "\n".join([f"{i+1}. {p.name} (⚔️ {p.attack} | 🛡 {p.defense})" for i, p in enumerate(team.players)])
    await message.reply(
        f"✅ تم إنشاء فريقك بنجاح!\n\n"
        f"🔰 لاعبيك:\n{players_list}\n\n"
        "استخدم الأمر `وضع_تشكيلة` لاختيار 3 هجوم و 3 دفاع"
    )

@app.on_message(filters.command(["وضع تشكيلة", "وضع تشكيله"], ""), group=3321)
async def set_formation(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if not team or len(team.players) < 6:
        return await message.reply("❌ ليس لديك فريق كامل (6 لاعبين)")
    
    # عرض اللاعبين للاختيار
    players_list = "\n".join([f"{i+1}. {p.name} (⚔️ {p.attack} | 🛡 {p.defense})" for i, p in enumerate(team.players)])
    
    await message.reply(
        f"📋 لاعبيك:\n\n{players_list}\n\n"
        "📌 أرسل أرقام 3 لاعبين للهجوم (مثل: 1 2 3)",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("إلغاء", callback_data="cancel_formation")]
        ])
    )
    
    user_states[user_id] = "selecting_attackers"

@app.on_message(filters.text & filters.group, group=644)
async def handle_formation_selection(client, message: Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != "selecting_attackers":
        return
    
    team = db.get_team(user_id)
    if not team:
        return
    
    try:
        selected = list(map(int, message.text.split()))
        if len(selected) != 3 or any(i < 1 or i > 6 for i in selected):
            return await message.reply("❌ يجب اختيار 3 أرقام بين 1 و 6")
        
        selected = [i-1 for i in selected]  # تحويل إلى indexes
        team.attackers = [team.players[i] for i in selected]
        team.defenders = [p for i, p in enumerate(team.players) if i not in selected]
        
        db.save_team(user_id, team)
        del user_states[user_id]
        
        attackers = "\n".join([f"⚽ {p.name} (⚔️ {p.attack})" for p in team.attackers])
        defenders = "\n".join([f"🛡 {p.name} (🛡 {p.defense})" for p in team.defenders])
        
        await message.reply(
            f"✅ تم وضع التشكيلة بنجاح!\n\n"
            f"**الهجوم:**\n{attackers}\n\n"
            f"**الدفاع:**\n{defenders}\n\n"
            "استخدم `انضمام الكأس` للانضمام إلى المنافسة"
        )
    
    except ValueError:
        await message.reply("❌ الرجاء إدخال أرقام فقط")

@app.on_callback_query(filters.regex("^cancel_formation$"), group=43333)
async def cancel_formation(client, query: CallbackQuery):
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    await query.message.edit_text("❌ تم إلغاء عملية وضع التشكيلة")

@app.on_message(filters.command(["تشكيلتي", "عرض تشكيلتي"], ""), group=422)
async def show_formation(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if not team or not team.attackers:
        return await message.reply("❌ ليس لديك تشكيلة محددة بعد")
    
    attackers = "\n".join([f"⚽ {p.name} (⚔️ {p.attack})" for p in team.attackers])
    defenders = "\n".join([f"🛡 {p.name} (🛡 {p.defense})" for p in team.defenders])
    
    text = (
        f"🏟 تشكيلة فريقك:\n\n"
        f"**الهجوم (3):**\n{attackers}\n\n"
        f"**الدفاع (3):**\n{defenders}\n\n"
        f"🏆 النقاط: {team.points}\n"
        f"📊 المباريات: {team.matches_played} (فوز: {team.matches_won})"
    )
    
    if team.legends:
        legends = "\n".join([f"🌟 {p.name} (⚔️ {p.attack} | 🛡 {p.defense})" for p in team.legends])
        text += f"\n\n**الأساطير:**\n{legends}"
    
    await message.reply(text)

@app.on_message(filters.command(["انضمام الكأس", "انضمام الكاس"], ""), group=3211)
async def join_cup(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if not team or len(team.attackers) != 3:
        return await message.reply("❌ يجب أن يكون لديك تشكيلة كاملة أولاً")
    
    if team.cup_joined:
        return await message.reply("❌ أنت بالفعل منضم للكأس!")
    
    total_attack = sum(p.attack for p in team.attackers)
    if total_attack < 30:
        return await message.reply(f"❌ قوة هجومك ({total_attack}) أقل من 30 المطلوبة")
    
    team.cup_joined = True
    db.save_team(user_id, team)
    await message.reply(
        "✅ تم انضمامك لكأس العالم بنجاح!\n\n"
        "ستبدأ المباريات تلقائياً كل ساعة\n"
        "استخدم `توب الكأس` لرؤية التصنيف"
    )

@app.on_message(filters.command(["توب الكأس", "توب الكاس"], ""), group=5333)
async def cup_leaderboard(client, message: Message):
    top_teams = db.get_top_teams()
    
    if not top_teams:
        return await message.reply("❌ لا يوجد فرق في الكأس بعد")
    
    leaderboard = []
    for i, team in enumerate(top_teams[:10], 1):
        try:
            user = await app.get_users(team.user_id)
            name = user.first_name
        except:
            name = f"لاعب {team.user_id}"
        
        leaderboard.append(
            f"{i}. {name} - {team.points} نقطة (⚔️ {sum(p.attack for p in team.attackers)} | 🛡 {sum(p.defense for p in team.defenders)})"
        )
    
    await message.reply(
        "🏆 تصنيف كأس العالم:\n\n" + "\n".join(leaderboard) + 
        "\n\nاستخدم `انضمام الكاس` للانضمام"
    )

@app.on_message(filters.command(["تمرين الهجوم", "تمرين هجوم"], ""), group=6668)
async def train_attack(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if not team:
        return await message.reply("❌ ليس لديك فريق لتدريبه")
    
    if time.time() - team.training_cooldown < 3600:
        remaining = 3600 - (time.time() - team.training_cooldown)
        return await message.reply(f"⏳ يجب الانتظار {int(remaining//60)} دقيقة قبل التدريب مجدداً")
    
    improvements = []
    for player in team.attackers:
        imp = random.randint(1, 3)
        player.attack += imp
        improvements.append(f"{player.name} +{imp}")
    
    team.training_cooldown = time.time()
    db.save_team(user_id, team)
    
    await message.reply(
        "✅ تم تدريب الهجوم بنجاح!\n\n" +
        "\n".join(improvements) +
        "\n\nيمكنك التدريب مرة أخرى بعد ساعة"
    )

@app.on_message(filters.command(["تحدي", "تحديات"], ""), group=5433)
async def challenge_match(client, message: Message):
    user_id = message.from_user.id
    team = db.get_team(user_id)
    
    if not team or len(team.attackers) != 3:
        return await message.reply("❌ يجب أن يكون لديك تشكيلة كاملة أولاً")
    
    # حساب قوة الفريق
    attack_power = sum(p.attack for p in team.attackers)
    defense_power = sum(p.defense for p in team.defenders)
    total_power = attack_power + defense_power
    
    # فرصة الفوز تعتمد على قوة الفريق
    win_chance = min(0.9, 0.5 + (total_power - 60) / 200)
    
    if random.random() < win_chance:
        # الفوز - الحصول على لاعب أسطوري
        legend_names = ["ميسي", "رونالدو", "نيمار", "صلاح", "مبابي", "هالاند", "دي بروين"]
        legend = Player(
            name=random.choice(legend_names),
            attack_power=random.randint(20, 30),
            defense_power=random.randint(15, 25),
            is_legend=True
        )
        team.legends.append(legend)
        team.points += 5
        db.save_team(user_id, team)
        
        await message.reply(
            f"🎉 فزت بالتحدي وحصلت على اللاعب الأسطوري:\n\n"
            f"🌟 {legend.name} (⚔️ {legend.attack} | 🛡 {legend.defense})\n\n"
            f"+5 نقاط! (إجمالي النقاط: {team.points})"
        )
    else:
        # الخسارة - فقدان بعض النقاط
        points_lost = random.randint(1, 3)
        team.points = max(0, team.points - points_lost)
        db.save_team(user_id, team)
        
        await message.reply(
            f"❌ خسرت التحدي وفقدت {points_lost} نقطة\n\n"
            f"النقاط الحالية: {team.points}\n"
            "حاول مرة أخرى لاحقاً!"
        )










game_data = {
    "active_chats": {},
    "winners": [],
    "half_winners": [],
    "losers": [],
    "banned_players": {},
    "kings": [],
    "questions": {
        1: [
            {"question": "ما هي عاصمة فرنسا؟", "answer": "باريس", "points": 10},
            {"question": "كم عدد أضلاع المثلث؟", "answer": "3", "points": 10},
            {"question": "ما هو الكوكب الأحمر؟", "answer": "المريخ", "points": 10},
            {"question": "من هو صاحب سورس فيجا", "answer": "كيمي", "points": 10},
            {"question": "ما هي اللغة الرسمية في البرازيل؟", "answer": "البرتغالية", "points": 10},
            {"question": "كم عدد أيام الأسبوع؟", "answer": "7", "points": 10},
            {"question": "ما هو الحيوان المعروف باسم ملك الغابة؟", "answer": "الأسد", "points": 10},
            {"question": "ما لون التفاحة الناضجة؟", "answer": "أحمر", "points": 10},
            {"question": "ما هو الشيء الذي يكتب ولا يقرأ؟", "answer": "القلم", "points": 10},
            {"question": "ما اسم صغير الكلب؟", "answer": "جرو", "points": 10}
        ],
        2: [
            {"question": "ما هي أكبر دولة في العالم من حيث المساحة؟", "answer": "روسيا", "points": 20},
            {"question": "في أي عام انتهت الحرب العالمية الثانية؟", "answer": "1945", "points": 20},
            {"question": "ما هو العنصر الكيميائي الذي رمزه O؟", "answer": "الأكسجين", "points": 20},
            {"question": "من هو مخترع المصباح الكهربائي؟", "answer": "توماس إديسون", "points": 20},
            {"question": "ما هي أعلى قمة جبل في العالم؟", "answer": "إفرست", "points": 20},
            {"question": "كم عدد أحرف اللغة الإنجليزية؟", "answer": "26", "points": 20},
            {"question": "ما هي العملة الرسمية في اليابان؟", "answer": "الين", "points": 20},
            {"question": "ما اسم العالم الذي اكتشف الجاذبية؟", "answer": "نيوتن", "points": 20},
            {"question": "كم عدد أيام السنة الكبيسة؟", "answer": "366", "points": 20},
            {"question": "ما هو الغاز الذي يشكل معظم الغلاف الجوي للأرض؟", "answer": "النيتروجين", "points": 20}
        ],
        3: [
            {"question": "ما هو أسرع حيوان بري؟", "answer": "الفهد", "points": 30},
            {"question": "كم عدد العظام في جسم الإنسان؟", "answer": "206", "points": 30},
            {"question": "ما هي عاصمة أستراليا؟", "answer": "كانبرا", "points": 30},
            {"question": "من هو افضل سورس في تليجرام", "answer": "فيجا", "points": 30},
            {"question": "ما هو أعمق محيط في العالم؟", "answer": "المحيط الهادئ", "points": 30},
            {"question": "كم عدد كواكب المجموعة الشمسية؟", "answer": "8", "points": 30},
            {"question": "ما هي أصغر دولة في العالم؟", "answer": "الفاتيكان", "points": 30},
            {"question": "ما هو أطول نفق في العالم؟", "answer": "نفق غوتهارد", "points": 30},
            {"question": "ما اسم أول رائد فضاء هبط على سطح القمر؟", "answer": "نيل أرمسترونج", "points": 30},
            {"question": "ما هي أقدم حضارة في التاريخ؟", "answer": "الحضارة السومرية", "points": 30}
        ],
        4: [
            {"question": "ما اسم العالم المسلم الذي أسس علم الجبر؟", "answer": "الخوارزمي", "points": 40},
            {"question": "كم عدد صمامات القلب في جسم الإنسان؟", "answer": "4", "points": 40},
            {"question": "ما هو المعدن الأكثر توصيلاً للكهرباء؟", "answer": "الفضة", "points": 40},
            {"question": "ما اسم أكبر صحراء في العالم؟", "answer": "الصحراء الكبرى", "points": 40},
            {"question": "ما هي أسرع الطيور في العالم؟", "answer": "الشفنين", "points": 40},
            {"question": "ما اسم أول رئيس للولايات المتحدة الأمريكية؟", "answer": "جورج واشنطن", "points": 40},
            {"question": "ما هي أطول عظمة في جسم الإنسان؟", "answer": "عظمة الفخذ", "points": 40},
            {"question": "ما اسم أول دولة استخدمت الطوابع البريدية؟", "answer": "بريطانيا", "points": 40},
            {"question": "ما هو أندر فصيلة دم في العالم؟", "answer": "O سالب", "points": 40},
            {"question": "ما اسم أول فيلم رسوم متحركة طويل من إنتاج ديزني؟", "answer": "سنو وايت", "points": 40}
        ],
        5: [
            {"question": "ما هو أطول نهر في أفريقيا؟", "answer": "النيل", "points": 50},
            {"question": "ما اسم أول حاسوب إلكتروني؟", "answer": "إنياك", "points": 50},
            {"question": "ما هي عاصمة كندا؟", "answer": "أوتاوا", "points": 50},
            {"question": "من هو مخترع الهاتف؟", "answer": "غراهام بيل", "points": 50},
            {"question": "ما هو أسرع حيوان بحري؟", "answer": "سمكة الزعنفة الشراعية", "points": 50},
            {"question": "ما هي أكبر جزيرة في العالم؟", "answer": "جرينلاند", "points": 50},
            {"question": "ما اسم أقوى عظم في جسم الإنسان؟", "answer": "عظمة الفك", "points": 50},
            {"question": "ما هو المعدن الأغلى ثمناً؟", "answer": "الروديوم", "points": 50},
            {"question": "ما اسم أطول جسر بحري في العالم؟", "answer": "جسر هونغ كونغ", "points": 50},
            {"question": "ما هي أقدم لغة مكتوبة؟", "answer": "السومرية", "points": 50}
        ],
        6: [
            {"question": "ما هو أعمق نقطة في المحيطات؟", "answer": "خندق ماريانا", "points": 60},
            {"question": "ما اسم أول قمر صناعي؟", "answer": "سبوتنيك", "points": 60},
            {"question": "ما هي أطول شجرة في العالم؟", "answer": "السيكويا", "points": 60},
            {"question": "ما اسم أكبر محيط في العالم؟", "answer": "المحيط الهادئ", "points": 60},
            {"question": "ما هو أسرع كمبيوتر في العالم؟", "answer": "فيوجاك", "points": 60},
            {"question": "ما اسم أول رجل سار على القمر؟", "answer": "نيل أرمسترونج", "points": 60},
            {"question": "ما هي أقدم جامعة في العالم؟", "answer": "جامعة القرويين", "points": 60},
            {"question": "ما هو أطول نفق للسكك الحديدية؟", "answer": "نفق غوتهارد", "points": 60},
            {"question": "ما اسم أكبر بركان في العالم؟", "answer": "مونا لوا", "points": 60},
            {"question": "ما هي أقدم عاصمة في التاريخ؟", "answer": "دمشق", "points": 60}
        ],
        7: [
            {"question": "ما هو أسرع حيوان طائر؟", "answer": "السنونو", "points": 70},
            {"question": "ما اسم أول دولة صنعت الصواريخ؟", "answer": "ألمانيا", "points": 70},
            {"question": "ما هي أطول سلسلة جبال في العالم؟", "answer": "الأنديز", "points": 70},
            {"question": "ما هو أقدم حيوان على الأرض؟", "answer": "الإسفنج", "points": 70},
            {"question": "ما اسم أول من اكتشف أمريكا؟", "answer": "ليف إريكسون", "points": 70},
            {"question": "ما هي أقدم ديانة في العالم؟", "answer": "الهندوسية", "points": 70},
            {"question": "ما هو أطول نهر في آسيا؟", "answer": "يانجتسي", "points": 70},
            {"question": "ما اسم أول من طار بالطائرة؟", "answer": "الأخوان رايت", "points": 70},
            {"question": "ما هي أقدم حضارة في أمريكا؟", "answer": "المايا", "points": 70},
            {"question": "ما هو أسرع قطار في العالم؟", "answer": "ماجليف", "points": 70}
        ],
        8: [
            {"question": "ما هو أقدم نصب تذكاري في العالم؟", "answer": "أهرامات الجيزة", "points": 80},
            {"question": "ما اسم أول من دار حول الأرض؟", "answer": "ماجلان", "points": 80},
            {"question": "ما هي أقدم لغة حية؟", "answer": "التاميلية", "points": 80},
            {"question": "ما هو أعمق بئر في العالم؟", "answer": "كولا سوبرديب", "points": 80},
            {"question": "ما اسم أول من صعد إلى الفضاء؟", "answer": "يوري جاجارين", "points": 80},
            {"question": "ما هي أقدم مملكة في العالم؟", "answer": "مملكة إيسن", "points": 80},
            {"question": "ما هو أسرع حيوان في الماء؟", "answer": "سمكة أبو شراع", "points": 80},
            {"question": "ما اسم أول من اكتشف الدورة الدموية؟", "answer": "ابن النفيس", "points": 80},
            {"question": "ما هي أقدم مدينة مأهولة؟", "answer": "أريحا", "points": 80},
            {"question": "ما هو أطول نفق للسيارات؟", "answer": "نفق لاردال", "points": 80}
        ],
        9: [
            {"question": "ما هو أقدم كتاب في العالم؟", "answer": "ملحمة جلجامش", "points": 90},
            {"question": "ما اسم أول من رسم خريطة العالم؟", "answer": "الإدريسي", "points": 90},
            {"question": "ما هي أقدم عملة في العالم؟", "answer": "الليدي", "points": 90},
            {"question": "ما هو أقدم متحف في العالم؟", "answer": "متحف الإسكندرية", "points": 90},
            {"question": "ما اسم أول من اخترع التلسكوب؟", "answer": "غاليليو", "points": 90},
            {"question": "ما هي أقدم شجرة في العالم؟", "answer": "ميثوسيلا", "points": 90},
            {"question": "ما هو أقدم حيوان مستأنس؟", "answer": "الكلب", "points": 90},
            {"question": "ما اسم أول من اكتشف الأنسولين؟", "answer": "بانتنغ", "points": 90},
            {"question": "ما هي أقدم حديقة حيوانات؟", "answer": "حديقة حيوانات فيينا", "points": 90},
            {"question": "ما هو أقدم نظام كتابة؟", "answer": "المسمارية", "points": 90}
        ],
        10: [
            {"question": "ما هو أقدم علم في العالم؟", "answer": "علم الدنمارك", "points": 100},
            {"question": "ما اسم أول من اكتشف جرثومة السل؟", "answer": "روبرت كوخ", "points": 100},
            {"question": "ما هي أقدم مملكة عربية؟", "answer": "مملكة معين", "points": 100},
            {"question": "ما هو أقدم دستور في العالم؟", "answer": "دستور الولايات المتحدة", "points": 100},
            {"question": "ما اسم أول من اخترع المطبعة؟", "answer": "جوتنبرج", "points": 100},
            {"question": "ما هي أقدم حضارة في الصين؟", "answer": "شيا", "points": 100},
            {"question": "ما هو أقدم نادي رياضي؟", "answer": "شيفيلد", "points": 100},
            {"question": "ما اسم أول من اكتشف أشعة إكس؟", "answer": "رونتجن", "points": 100},
            {"question": "ما هي أقدم جامعة في أوروبا؟", "answer": "بولونيا", "points": 100},
            {"question": "ما هو أقدم ميناء في العالم؟", "answer": "ميناء اللاذقية", "points": 100}
        ]
    },
    "last_response_time": {},
    "last_clean_time": datetime.now(),
    "menu_messages": {}
}

async def get_user_mention(client, user_id):
    try:
        user = await client.get_users(user_id)
        return user.mention
    except:
        return f"المستخدم {user_id}"

async def get_user_photo(client, user_id):
    try:
        user = await client.get_users(user_id)
        if user.photo:
            photo = await client.download_media(user.photo.big_file_id)
            return photo
        return None
    except:
        return None

async def clean_winners_list():
    while True:
        await asyncio.sleep(86400)
        now = datetime.now()
        if (now - game_data["last_clean_time"]).total_seconds() >= 86400:
            game_data["winners"] = []
            game_data["half_winners"] = []
            game_data["losers"] = []
            game_data["last_clean_time"] = now

@app.on_message(filters.command(["ro", "رو"], ""), group=433)
async def show_games_menu(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if user_id in game_data["banned_players"]:
        ban_time = game_data["banned_players"][user_id]
        if datetime.now() < ban_time:
            remaining = ban_time - datetime.now()
            await message.reply_text(
                f"⛔ أنت محظور من اللعبة لمدة {remaining.seconds//60} دقائق و {remaining.seconds%60} ثانية بسبب 5 إجابات خاطئة متتالية!"
            )
            return
        else:
            del game_data["banned_players"][user_id]
    
    menu_msg = await message.reply_photo(
        photo="https://i.ibb.co/Fb2Jd2hL/image.jpg",
        caption=f"<b>⭓ɢᴧᴍᴇꜱ✘ᴠᴇɢᴧ♪\n<blockquote>- مـرحـبـا بـك: {message.from_user.mention}\n- في لعبه ( رو) من فيجا</b></blockquote>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("ابدء للعب معي", callback_data=f"start_game_{chat_id}")],
            [InlineKeyboardButton("تعليمات", callback_data="show_instructions"),
             InlineKeyboardButton("الفائزين", callback_data="show_winners"),
             InlineKeyboardButton("الفاشلين", callback_data="show_losers")],
            [InlineKeyboardButton("الملوك", callback_data="show_kings")],
            [InlineKeyboardButton("ᴠᴇɢᴀ", url="https://t.me/vegaxone")]
        ])
    )
    
    game_data["menu_messages"][f"{chat_id}_{user_id}"] = menu_msg.id

@app.on_message(filters.command("مستويا", ""), group=434)
async def show_player_stats(client: Client, message: Message):
    chat_id = message.chat.id
    target_user = message.from_user
    
    if message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
        if chat_id in game_data["active_chats"]:
            for player_id in game_data["active_chats"][chat_id]["active_players"]:
                player_data = game_data["active_chats"][chat_id]["active_players"][player_id]
                if player_data.get("last_question_message_id") == message.reply_to_message.id:
                    target_user = await client.get_users(player_id)
                    break
    
    user_id = target_user.id
    
    if chat_id not in game_data["active_chats"] or user_id not in game_data["active_chats"][chat_id]["active_players"]:
        await message.reply_text("⚠️ ليس لديك جولة نشطة حالياً. ابدأ اللعبة أولاً!")
        return
    
    player_data = game_data["active_chats"][chat_id]["active_players"][user_id]
    
    rank = "🟢 مبتدئ"
    if player_data["level"] >= 3:
        rank = "🔵 متوسط"
    if player_data["level"] >= 5:
        rank = "🟣 محترف"
    if player_data["level"] >= 7:
        rank = "🟡 خبير"
    if player_data["level"] >= 9:
        rank = "🟠 محارب"
    if player_data["level"] >= 10:
        rank = "🔴 ملك"
    
    remaining_time = 300 - (datetime.now() - player_data["start_time"]).seconds
    remaining_time = max(0, remaining_time)
    
    stats_text = (
        f"📊 <b>إحصائيات اللاعب:</b> {await get_user_mention(client, user_id)}\n"
        f"🏅 <b>الرتبة:</b> {rank}\n\n"
        f"🏆 <b>المستوى الحالي:</b> {player_data['level']}\n"
        f"💰 <b>الفلوس الحالية:</b> {player_data['total_score']}\n"
        f"✅ <b>الإجابات الصحيحة:</b> {player_data['correct_answers']}\n"
        f"❌ <b>الإجابات الخاطئة:</b> {player_data['wrong_answers_count']}\n"
        f"📝 <b>الأسئلة المتبقية:</b> {10 - player_data['answered']}\n"
        f"⏳ <b>الوقت المتبقي:</b> {remaining_time} ثانية"
    )
    
    await message.reply_text(stats_text)

@app.on_callback_query(filters.regex(r"^start_game_(-?\d+)$"), group=4344)
async def start_game_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    chat_id = int(callback_query.data.split("_")[2])
    
    if chat_id not in game_data["active_chats"]:
        game_data["active_chats"][chat_id] = {
            "active_players": {},
            "max_players": 5,
            "current_players": 0
        }
    
    chat_data = game_data["active_chats"][chat_id]
    
    if chat_data["current_players"] >= chat_data["max_players"]:
        await callback_query.answer("⚠️ وصلت المجموعة إلى الحد الأقصى من اللاعبين (5 لاعبين)، يرجى الانتظار حتى ينتهي أحدهم!", show_alert=True)
        return
    
    if user_id in chat_data["active_players"]:
        await callback_query.answer("لديك جولة نشطة بالفعل! أكمل أسئلتك الحالية أولاً.", show_alert=True)
        return
    
    chat_data["active_players"][user_id] = {
        "level": 1,
        "score": 0,
        "total_score": 10,
        "current_questions": [],
        "answered": 0,
        "wrong_answers": 0,
        "consecutive_wrong": 0,
        "start_time": datetime.now(),
        "timeout_task": None,
        "chat_id": chat_id,
        "mute_count": 0,
        "can_control": True,
        "last_question_message_id": None,
        "correct_answers": 0,
        "wrong_answers_count": 0,
        "perfect_levels": 0
    }
    chat_data["current_players"] += 1
    
    player_data = chat_data["active_players"][user_id]
    player_data["current_questions"] = random.sample(game_data["questions"][1], 10)
    
    welcome_msg = await callback_query.message.reply_text(
        f"🎮 {callback_query.from_user.mention} بدأ جولة جديدة!\n"
        f"🔹 لديك 10 جنيه بداية\n"
        f"🔹 كل إجابة صحيحة: +{game_data['questions'][1][0]['points']} جنيه\n"
        f"🔹 5 إجابات خاطئة متتالية: حظر من اللعبة\n"
        f"🔹 لديك 5 دقائق للإجابة على كل سؤال\n"
        f"🔹 اللاعبون النشطون: {chat_data['current_players']}/{chat_data['max_players']}"
    )
    player_data["timeout_task"] = asyncio.create_task(timeout_player(client, user_id, chat_id))
    
    await asyncio.sleep(3)
    await send_question(client, user_id, chat_id)
    await callback_query.answer("بدأت اللعبة! مع ( رو )", show_alert=True)

async def send_question(client: Client, player_id: int, chat_id: int):
    if chat_id not in game_data["active_chats"] or player_id not in game_data["active_chats"][chat_id]["active_players"]:
        return
    
    chat_data = game_data["active_chats"][chat_id]
    player_data = chat_data["active_players"][player_id]
    
    if player_data["answered"] >= len(player_data["current_questions"]):
        await handle_level_completion(client, player_id, chat_id)
        return
    
    current_q = player_data["current_questions"][player_data["answered"]]
    
    question_text = (
        f"👤 اللاعب: {await get_user_mention(client, player_id)}\n"
        f"💰 الفلوس: {player_data['total_score']} | المستوى: {player_data['level']}\n\n"
        f"<blockquote>❓ السؤال ({player_data['answered'] + 1}/10):\n"
        f"{current_q['question']}</blockquote>\n\n"
        "<blockquote>⏱ لديك 5 دقائق للإجابة\n"
        "↪️ **قم بالرد على هذه الرسالة بإجابتك**\n"
        " **الارجاء كتابه الايجابة باللغه العربية الفصحي**</blockquote>"
    )
    
    try:
        if player_data["last_question_message_id"]:
            try:
                await client.delete_messages(
                    chat_id=chat_id,
                    message_ids=player_data["last_question_message_id"]
                )
            except:
                pass
        
        sent_message = await client.send_message(
            chat_id,
            question_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("إنهاء الجولة", callback_data=f"exit_game_{player_id}_{chat_id}")]
            ])
        )
        player_data["last_question_message_id"] = sent_message.id
        player_data["start_time"] = datetime.now()  # تحديث وقت بدء السؤال
        game_data["last_response_time"][player_id] = datetime.now()
        
        # إلغاء أي مهمة انتهاء وقت سابقة وإنشاء واحدة جديدة
        if player_data["timeout_task"]:
            player_data["timeout_task"].cancel()
        player_data["timeout_task"] = asyncio.create_task(timeout_player(client, player_id, chat_id))
    except Exception as e:
        print(f"Error sending question: {e}")

async def timeout_player(client: Client, player_id: int, chat_id: int):
    await asyncio.sleep(300)  # 5 دقائق
    
    if chat_id in game_data["active_chats"] and player_id in game_data["active_chats"][chat_id]["active_players"]:
        chat_data = game_data["active_chats"][chat_id]
        player_data = chat_data["active_players"].pop(player_id)
        chat_data["current_players"] -= 1
        
        try:
            await client.send_message(
                chat_id,
                f"⏰ انتهى وقت {await get_user_mention(client, player_id)}! تم إلغاء اللعبة."
            )
        except Exception as e:
            print(f"Error sending timeout message: {e}")

@app.on_message(filters.text & (filters.group | filters.private), group=321)
async def handle_answer(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if chat_id not in game_data["active_chats"] or user_id not in game_data["active_chats"][chat_id]["active_players"]:
        return
        
    chat_data = game_data["active_chats"][chat_id]
    player_data = chat_data["active_players"][user_id]
    
    if not message.reply_to_message or message.reply_to_message.from_user.id != client.me.id:
        return
    
    current_q = player_data["current_questions"][player_data["answered"]]
    
    if message.text.lower() == current_q["answer"].lower():
        player_data["score"] += 1
        player_data["total_score"] += current_q["points"]
        player_data["answered"] += 1
        player_data["consecutive_wrong"] = 0
        player_data["correct_answers"] += 1
        
        if player_data["timeout_task"]:
            player_data["timeout_task"].cancel()
        player_data["timeout_task"] = asyncio.create_task(timeout_player(client, user_id, chat_id))
        
        reply_msg = await message.reply_text(
            f"✅ إجابة صحيحة!\n"
            f"💰 تمت إضافة {current_q['points']} جنيه. فلوسك الآن: {player_data['total_score']}",
            quote=True
        )
        
        if player_data["answered"] >= 10:
            await handle_level_completion(client, user_id, chat_id)
        else:
            await send_question(client, user_id, chat_id)
    else:
        player_data["wrong_answers"] += 1
        player_data["consecutive_wrong"] += 1
        player_data["wrong_answers_count"] += 1
        player_data["total_score"] = max(0, player_data["total_score"] - 5)
        
        reply_msg = await message.reply_text(
            f"❌ إجابة خاطئة!\n"
            f"💰 تم خصم 5 جنيه. فلوسك الآن: {player_data['total_score']}\n"
            f"🔹 الإجابة الصحيحة: {current_q['answer']}",
            quote=True
        )
        
        if player_data["wrong_answers"] == 1:
            await mute_player(client, user_id, chat_id, 240)
        
        if player_data["consecutive_wrong"] >= 5:
            await ban_player(client, user_id, chat_id)
        else:
            player_data["answered"] += 1
            if player_data["answered"] >= 10:
                await handle_level_completion(client, user_id, chat_id)
            else:
                await send_question(client, user_id, chat_id)

async def mute_player(client: Client, user_id: int, chat_id: int, mute_time: int):
    try:
        if str(chat_id).startswith("-"):
            await client.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(),
                until_date=int(time.time()) + mute_time
            )
            
            if chat_id in game_data["active_chats"] and user_id in game_data["active_chats"][chat_id]["active_players"]:
                game_data["active_chats"][chat_id]["active_players"][user_id]["mute_count"] += 1
                
            user_mention = await get_user_mention(client, user_id)
            await client.send_message(
                chat_id,
                f"⛔ تم كتم {user_mention} لمدة {mute_time//60} دقائق بسبب إجابة خاطئة!"
            )
    except Exception as e:
        print(f"Error muting player: {e}")

async def ban_player(client: Client, user_id: int, chat_id: int):
    ban_duration = timedelta(hours=1)
    game_data["banned_players"][user_id] = datetime.now() + ban_duration
    
    if chat_id in game_data["active_chats"] and user_id in game_data["active_chats"][chat_id]["active_players"]:
        game_data["active_chats"][chat_id]["active_players"].pop(user_id)
        game_data["active_chats"][chat_id]["current_players"] -= 1
    
    try:
        user_mention = await get_user_mention(client, user_id)
        await client.send_message(
            chat_id,
            f"⛔ تم حظر {user_mention} من اللعبة لمدة ساعة بسبب 5 إجابات خاطئة متتالية!"
        )
    except Exception as e:
        print(f"Error sending ban message: {e}")

async def handle_level_completion(client: Client, player_id: int, chat_id: int):
    if chat_id not in game_data["active_chats"] or player_id not in game_data["active_chats"][chat_id]["active_players"]:
        return
    
    chat_data = game_data["active_chats"][chat_id]
    player_data = chat_data["active_players"][player_id]
    
    if player_data["wrong_answers_count"] == 0:
        player_data["perfect_levels"] += 1
    
    if player_data["score"] >= 7:
        # عند الوصول للمستوى الرابع (قبل المستوى الخامس)
        if player_data["level"] == 4:
            user_mention = await get_user_mention(client, player_id)
            
            # إضافة للفائزين بنصف الجولة إذا أكمل بدون أخطاء
            if player_data["wrong_answers_count"] == 0:
                game_data["half_winners"].append({
                    "user_id": player_id,
                    "score": player_data["total_score"],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": user_mention,
                    "level": player_data["level"],
                    "perfect": True
                })
            
            # عرض خيار الاستمرار للمستوى الخامس
            await client.send_message(
                chat_id,
                f"🎉 {user_mention} لقد أكملت المستوى الرابع بنجاح!\n"
                f"💰 فلوسك الحالية: {player_data['total_score']}\n"
                "هل تريد الاستمرار للمستوى الخامس؟",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("نعم، أريد الاستمرار", callback_data=f"continue_game_{player_id}_{chat_id}")],
                    [InlineKeyboardButton("لا، أريد التوقف", callback_data=f"stop_game_{player_id}_{chat_id}")]
                ])
            )
            return
        
        player_data["level"] += 1
        
        if player_data["level"] > len(game_data["questions"]):
            await handle_game_win(client, player_id, chat_id)
            return
        
        player_data["score"] = 0
        player_data["answered"] = 0
        player_data["wrong_answers"] = 0
        player_data["consecutive_wrong"] = 0
        player_data["current_questions"] = random.sample(
            game_data["questions"][player_data["level"]], 
            10
        )
        
        # تحديد الرتبة الجديدة
        rank = "🟢 مبتدئ"
        if player_data["level"] >= 3:
            rank = "🔵 متوسط"
        if player_data["level"] >= 5:
            rank = "🟣 محترف"
        if player_data["level"] >= 7:
            rank = "🟡 خبير"
        if player_data["level"] >= 9:
            rank = "🟠 محارب"
        if player_data["level"] >= 10:
            rank = "🔴 مالك رو"
        
        await client.send_message(
            chat_id,
            f"🎉 {await get_user_mention(client, player_id)} تجاوز المستوى {player_data['level']-1}!\n"
            f"💰 فلوسك الإجمالية: {player_data['total_score']}\n"
            f"🏅 رتبتك الجديدة: {rank}\n"
            f"➡️ المستوى التالي: {player_data['level']} (كل إجابة صحيحة: +{game_data['questions'][player_data['level']][0]['points']} جنيه)"
        )
        
        await send_question(client, player_id, chat_id)
    else:
        # إذا أجاب على أقل من 8 أسئلة بشكل صحيح (أي أكثر من 2 خطأ)
        if player_data["score"] < 8:
            player_data["total_score"] = 0
            player_data["level"] = 1
        
        user_mention = await get_user_mention(client, player_id)
        game_data["losers"].append({
            "user_id": player_id,
            "score": player_data["total_score"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": user_mention,
            "level": player_data["level"]
        })
        
        await client.send_message(
            chat_id,
            f"❌ {await get_user_mention(client, player_id)} لم يجتاز المستوى {player_data['level']}!\n"
            f"💰 فلوسك النهائية: {player_data['total_score']}\n"
            "يمكنك المحاولة مرة أخرى لاحقاً."
        )
        chat_data["active_players"].pop(player_id)
        chat_data["current_players"] -= 1

@app.on_callback_query(filters.regex(r"^continue_game_(\d+)_(-?\d+)$"), group=435)
async def continue_game_callback(client: Client, callback_query):
    user_id = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    
    if chat_id not in game_data["active_chats"] or user_id not in game_data["active_chats"][chat_id]["active_players"]:
        await callback_query.answer("❌ الجولة لم تعد نشطة!", show_alert=True)
        return
    
    player_data = game_data["active_chats"][chat_id]["active_players"][user_id]
    
    player_data["level"] += 1
    player_data["score"] = 0
    player_data["answered"] = 0
    player_data["wrong_answers"] = 0
    player_data["consecutive_wrong"] = 0
    player_data["current_questions"] = random.sample(
        game_data["questions"][player_data["level"]], 
        10
    )
    
    await callback_query.message.edit_text(
        f"🎉 {await get_user_mention(client, user_id)} سوف يستمر في اللعبة!\n"
        f"💰 فلوسك الحالية: {player_data['total_score']}\n"
        f"➡️ المستوى التالي: {player_data['level']}"
    )
    
    await send_question(client, user_id, chat_id)
    await callback_query.answer("استمرار اللعبة!", show_alert=True)

@app.on_callback_query(filters.regex(r"^stop_game_(\d+)_(-?\d+)$"), group=436)
async def stop_game_callback(client: Client, callback_query):
    user_id = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    
    if chat_id in game_data["active_chats"] and user_id in game_data["active_chats"][chat_id]["active_players"]:
        player_data = game_data["active_chats"][chat_id]["active_players"].pop(user_id)
        game_data["active_chats"][chat_id]["current_players"] -= 1
        
        # إذا أكمل بدون أخطاء يضاف للملوك
        if player_data["perfect_levels"] >= 5:
            user_mention = await get_user_mention(client, user_id)
            game_data["kings"].append({
                "user_id": user_id,
                "score": player_data["total_score"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": user_mention,
                "perfect_levels": player_data["perfect_levels"]
            })
        
        await callback_query.message.edit_text(
            f"🎮 {await get_user_mention(client, user_id)} قرر التوقف عند المستوى {player_data['level']}!\n"
            f"💰 فلوسك النهائية: {player_data['total_score']}\n"
            "يمكنك العودة في أي وقت لاستكمال المستويات الأخرى!"
        )
    else:
        await callback_query.answer("❌ الجولة لم تعد نشطة!", show_alert=True)
    
    await callback_query.answer("تم إنهاء اللعبة!", show_alert=True)

async def handle_game_win(client: Client, player_id: int, chat_id: int):
    if chat_id not in game_data["active_chats"] or player_id not in game_data["active_chats"][chat_id]["active_players"]:
        return
    
    chat_data = game_data["active_chats"][chat_id]
    player_data = chat_data["active_players"].pop(player_id)
    chat_data["current_players"] -= 1
    
    user_mention = await get_user_mention(client, player_id)
    
    # تحديد رتبة الفائز حسب عدد المستويات المكتملة بدون أخطاء
    rank = "🟢 فائز"
    if player_data["perfect_levels"] >= 3:
        rank = "🔵 فائز متميز"
    if player_data["perfect_levels"] >= 5:
        rank = "🟣 بطل"
    if player_data["perfect_levels"] >= 7:
        rank = "🟡 أسطورة"
    if player_data["perfect_levels"] >= 10:
        rank = "🔴 ملك"
        game_data["kings"].append({
            "user_id": player_id,
            "score": player_data["total_score"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": user_mention,
            "perfect_levels": player_data["perfect_levels"]
        })
    
    game_data["winners"].append({
        "user_id": player_id,
        "score": player_data["total_score"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": user_mention,
        "rank": rank,
        "perfect_levels": player_data["perfect_levels"]
    })
    
    try:
        user_photo = await get_user_photo(client, player_id)
        if user_photo:
            await client.send_photo(
                chat_id,
                photo=user_photo,
                caption=f"<blockquote>🎊 مبروك {user_mention}! أكملت جميع مراحل اللعبة بنجاح!\n"
                f"🏆 فلوسك النهائية: {player_data['total_score']}\n"
                f"👑 رتبتك: {rank}\n"
                f"⭐ المستويات المكتملة بدون أخطاء: {player_data['perfect_levels']}\n"
                "تم إضافتك إلى قائمة الفائزين!</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"{rank} {user_mention}", url=f"tg://user?id={player_id}")]
                ])
            )
        else:
            await client.send_message(
                chat_id,
                f"<blockquote>🎊 مبروك {user_mention}! أكملت جميع مراحل اللعبة بنجاح!\n"
                f"🏆 فلوسك النهائية: {player_data['total_score']}\n"
                f"👑 رتبتك: {rank}\n"
                f"⭐ المستويات المكتملة بدون أخطاء: {player_data['perfect_levels']}\n"
                "تم إضافتك إلى قائمة الفائزين!</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"{rank} {user_mention}", url=f"tg://user?id={player_id}")]
                ])
            )
        
        if str(chat_id).startswith("-"):
            last_msg = await client.get_messages(chat_id, limit=1)
            if last_msg:
                await client.pin_chat_message(chat_id, last_msg[0].id)
        
        if str(chat_id).startswith("-"):
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=player_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                    can_manage_video_chats=False
                )
            )
            await client.set_chat_administrator_custom_title(
                chat_id=chat_id,
                user_id=player_id,
                custom_title=rank
            )
    except Exception as e:
        print(f"Error handling win: {e}")

@app.on_callback_query(filters.regex("^show_instructions$"), group=77655)
async def show_instructions(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    instructions = """<blockquote>My Name ( Ro )</blockquote>\n
•**تعليمات لعبة (رو):**
•اللعبة تتكون من 10 مستويات
•كل مستوى يحتوي على 10 أسئلة
•يجب الإجابة على 10 أسئلة بشكل صحيح لاجتياز المستوى
•تبدأ بـ 10 جنيه فقط
•لديك 5 دقائق للإجابة على كل سؤال
•الجوائز:
•المستوى 1: +10 جنيه لكل إجابة صحيحة
•المستوى 2: +20 جنيه لكل إجابة صحيحة
•... حتى المستوى 10: +100 جنيه لكل إجابة صحيحة
    
•**العقوبات:**
•إجابة خاطئة: -5 جنيه + كتم لمدة 3 دقائق (من أول خطأ)
•5 إجابات خاطئة متتالية: حظر من اللعبة لمدة ساعة
•أقل من 8 إجابات صحيحة: تصفير الفلوس والعودة للمستوى الأول
    
•**المستويات والرتب:**
•1-2: مبتدئ (🟢)
•3-4: متوسط (🔵)
•5-6: محترف (🟣)
•7-8: خبير (🟡)
•9-10: محارب (🟠)
•فائز بكل المستويات: ملك (🔴)
    
•**قائمة الملوك:**
•اللاعبين الذين أكملوا كل المستويات بدون أخطاء
•يمكن عرضها عبر زر 'الملوك'
    
•**أمر [مستويا + مستوه]:**
•يعرض إحصائيات اللاعب الحالية
•يمكن استخدامه بالرد على رسالة اللاعب لعرض إحصائياته
    </blockquote>
    """
    
    menu_msg_id = game_data["menu_messages"].get(f"{chat_id}_{user_id}")
    
    if menu_msg_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=menu_msg_id,
                text=instructions,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
        except:
            await callback_query.message.edit_text(
                instructions,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
    else:
        await callback_query.message.edit_text(
            instructions,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
            ])
        )
    
    await callback_query.answer()

@app.on_callback_query(filters.regex("^show_winners$"), group=980)
async def show_winners(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    if not game_data["winners"] and not game_data["half_winners"]:
        await callback_query.answer("لا يوجد فائزين حتى الآن!", show_alert=True)
        return
    
    winners_text = "**🏆 قائمة الفائزين الكاملة:**\n\n"
    for idx, winner in enumerate(game_data["winners"][-10:], 1): 
        winners_text += f"{idx}. {winner['name']} - {winner['rank']} - فلوس: {winner['score']} - {winner['date']}\n"
    
    if game_data["half_winners"]:
        winners_text += "\n**🎖 قائمة الفائزين بنصف الجولة:**\n\n"
        for idx, winner in enumerate(game_data["half_winners"][-10:], 1): 
            winners_text += f"{idx}. {winner['name']} - فلوس: {winner['score']} - المستوى: {winner['level']} - {winner['date']}\n"
    
    menu_msg_id = game_data["menu_messages"].get(f"{chat_id}_{user_id}")
    
    if menu_msg_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=menu_msg_id,
                text=winners_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
        except:
            await callback_query.message.edit_text(
                winners_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
    else:
        await callback_query.message.edit_text(
            winners_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
            ])
        )
    
    await callback_query.answer()

@app.on_callback_query(filters.regex("^show_losers$"), group=981)
async def show_losers(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    if not game_data["losers"]:
        await callback_query.answer("لا يوجد فاشلين حتى الآن!", show_alert=True)
        return
    
    losers_text = "**😞 قائمة الفاشلين:**\n\n"
    for idx, loser in enumerate(game_data["losers"][-10:], 1): 
        losers_text += f"{idx}. {loser['name']} - فلوس: {loser['score']} - المستوى: {loser['level']} - {loser['date']}\n"
    
    menu_msg_id = game_data["menu_messages"].get(f"{chat_id}_{user_id}")
    
    if menu_msg_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=menu_msg_id,
                text=losers_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
        except:
            await callback_query.message.edit_text(
                losers_text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
                ])
            )
    else:
        await callback_query.message.edit_text(
            losers_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
            ])
        )
    
    await callback_query.answer()

@app.on_callback_query(filters.regex("^show_kings$"), group=982)
async def show_kings(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    # تعريف الرتب مع إيموجيات مميزة
    ranks = {
        "owner": ["المالك الأساسي", "👑"],
        "king": ["ملك اللعبة", "🔥"],
        "legend": ["أسطورة", "⭐"],
        "elite": ["نخبة", "🎖"],
        "veteran": ["محارب قديم", "🛡"]
    }
    
    # بيانات المطور (المالك الأساسي)
    game_owner = {
        "user_id": 7654641648,  # استبدل بمعرف المطور الحقيقي @TopVeGa
        "name": "كيمي",
        "score": "∞",
        "perfect_levels": "10+",
        "date": "منذ البداية",
        "rank": ranks["owner"],
        "is_owner": True
    }
    
    # إنشاء قائمة الملوك المعدلة
    modified_kings = [game_owner]  # المطور أولاً
    
    # إضافة بقية الملوك مع تحديد رتبهم
    for king in game_data["kings"][-9:]:  # آخر 9 لاعبين
        # تحديد الرتبة حسب عدد المستويات المكتملة بدون أخطاء
        if king.get("perfect_levels", 0) >= 10:
            rank = ranks["king"]
        elif king.get("perfect_levels", 0) >= 8:
            rank = ranks["legend"]
        elif king.get("perfect_levels", 0) >= 6:
            rank = ranks["elite"]
        else:
            rank = ranks["veteran"]
            
        king["rank"] = rank
        king["is_owner"] = False
        modified_kings.append(king)
    
    if not modified_kings:
        await callback_query.answer("لا يوجد ملوك حتى الآن!", show_alert=True)
        return
    
    # إنشاء نص الرسالة مع روابط الملفات الشخصية
    kings_text = f"""
<b>{ranks['owner'][1]} قائمة ملوك لعبة رو {ranks['owner'][1]}</b>

**المالك الأساسي:**
<a href='tg://user?id={game_owner['user_id']}'>[{game_owner['rank'][1]} {game_owner['name']}]</a> ({game_owner['rank'][0]})
<u>أبطال اللعبة:</u>
"""
    
    for idx, king in enumerate(modified_kings[1:], 1):  # نبدأ من 1 لأن 0 هو المطور
        kings_text += f"""
{idx}. <a href='tg://user?id={king['user_id']}'>[{king['rank'][1]} {king['name']}]</a>
• الرتبة: {king['rank'][0]}
• النقاط: {king['score']} 
• المستويات المثالية: {king['perfect_levels']}
⎯ ⎯ ⎯ ⎯ ⎯ ⎯ ⎯ ⎯ ⎯ ⎯
"""
    
    # إنشاء الأزرار
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("𝐓𝐎𝐏𝐕𝐄𝐆𝐀", url="https://t.me/TopVeGa")],
        [InlineKeyboardButton("رجوع", callback_data="back_to_menu")]
    ])
    
    try:
        await callback_query.message.edit_text(
            text=kings_text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error editing message: {e}")
        await callback_query.answer("حدث خطأ أثناء عرض القائمة!", show_alert=True)
    
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^exit_game_(\d+)_(-?\d+)$"), group=636)
async def exit_game(client: Client, callback_query):
    user_id = int(callback_query.data.split("_")[2])
    chat_id = int(callback_query.data.split("_")[3])
    if callback_query.from_user.id != user_id:
        await callback_query.answer("هذا الزر خاص باللاعب فقط!", show_alert=True)
        return
    
    if chat_id in game_data["active_chats"] and user_id in game_data["active_chats"][chat_id]["active_players"]:
        player_data = game_data["active_chats"][chat_id]["active_players"].pop(user_id)
        game_data["active_chats"][chat_id]["current_players"] -= 1
        
        await callback_query.message.edit_text(
            f"**تم الخروج من اللعبة. فلوسك النهائية: {player_data['total_score']}\n"
            "يمكنك العودة في أي وقت!\nتم انشاء هذه للعبة بواسطة : [ @TopVeGa ]**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("العودة للقائمة 🎮", callback_data="back_to_menu")]
            ])
        )
    await callback_query.answer()

@app.on_callback_query(filters.regex("^back_to_menu$"), group=2333)
async def back_to_menu(client: Client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    menu_msg_id = game_data["menu_messages"].get(f"{chat_id}_{user_id}")
    
    if menu_msg_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=menu_msg_id,
                text=f"<b>⭓ɢᴧᴍᴇꜱ✘ᴠᴇɢᴧ♪\n<blockquote>- مـرحـبـا بـك: {callback_query.from_user.mention}\n- في لعبه ( رو) من فيجا</b></blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ابدء للعب معي", callback_data=f"start_game_{chat_id}")],
                    [InlineKeyboardButton("تعليمات", callback_data="show_instructions"),
                     InlineKeyboardButton("الفائزين", callback_data="show_winners"),
                     InlineKeyboardButton("الفاشلين", callback_data="show_losers")],
                    [InlineKeyboardButton("الملوك", callback_data="show_kings")],
                    [InlineKeyboardButton("ᴠᴇɢᴀ", url="https://t.me/vegaxone")]
                ])
            )
        except:
            await show_games_menu(client, callback_query.message)
    else:
        await show_games_menu(client, callback_query.message)
    
    await callback_query.answer()

# بدء مهمة تنظيف القوائم كل 24 ساعة
asyncio.create_task(clean_winners_list())