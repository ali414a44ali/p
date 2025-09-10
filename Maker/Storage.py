


import os
import asyncio

from pyrogram import Client, filters
from pyrogram import filters
from pyrogram import Client, filters
from pyrogram import types
from pyrogram import enums
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.errors import PeerIdInvalid
from bot import bot, bot_id, db, SUDORS
from pyrogram import types
from pyrogram import enums
from pyrogram import __version__ as pyrover
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from pymongo import MongoClient
from bot import SUDORS
from motor.motor_asyncio import AsyncIOMotorClient as mongo_client
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from Maker.Makr import *
from Maker.Makr import mongo_client
from pyrogram.types import ReplyKeyboardRemove

BROADCAST_TYPES = {
    "normal": f":broadcast:{bot_id}",
    "forward": f":fbroadcast:{bot_id}",
    "pin": f":pinbroadcast:{bot_id}"
}

# ============ دوال إدارة المستخدمين ============

def add_new_user(user_id: int) -> None:
    """إضافة مستخدم جديد إلى قاعدة البيانات"""
    if not is_user(user_id):
        db.sadd(f"botusers&{bot_id}", user_id)

def is_user(user_id: int) -> bool:
    """التحقق من وجود المستخدم في قاعدة البيانات"""
    try:
        return user_id in get_users()
    except Exception:
        return False

def get_users() -> list:
    """جلب قائمة جميع المستخدمين"""
    try:
        return db.get(f"botusers&{bot_id}")["set"] or []
    except Exception:
        return []

def users_backup() -> str:
    """إنشاء نسخة احتياطية للمستخدمين"""
    users = "\n".join(str(user) for user in get_users())
    with open("users.txt", "w+") as f:
        f.write(users)
    return "users.txt"

def del_user(user_id: int) -> bool:
    """حذف مستخدم من قاعدة البيانات"""
    if is_user(user_id):
        db.srem(f"botusers&{bot_id}", user_id)
        return True
    return False



		

@bot.on_message(filters.command("start") & filters.private)
async def new_user(bot, msg):
    if not is_user(msg.from_user.id):
        add_new_user(msg.from_user.id)
        text = f"""┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈\n
<blockquote> ⦿  دخل عضو جديد لـ.» فـيـجا</blockquote>

<blockquote>╮⦿  الاسم : {msg.from_user.first_name}</blockquote>
<blockquote>│᚜⦿ منشن : {msg.from_user.mention}</blockquote>
<blockquote>╯⦿  الايدي : {msg.from_user.id}</blockquote>\n┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈
        """
        
        username = msg.from_user.username if msg.from_user.username else "unknown"
        buttons = [
            [InlineKeyboardButton(msg.from_user.first_name, url=f"https://t.me/{username}")],
            [InlineKeyboardButton(f"» عدد الاعضاء: {len(get_users())}", callback_data=f"user_count_{msg.from_user.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        if SUDORS:  
            for user_id in SUDORS:
                await bot.send_message(int(user_id), text, reply_markup=reply_markup)
        else:
            LOGGER.warning("قائمة SUDORS فارغة! لا يمكن إرسال الإشعار.")
					



		
@bot.on_message(filters.command("start") & filters.private, group=162728)
async def start_command(bot, msg):
    await show_main_menu(bot, msg)

@bot.on_message(filters.command(["رجوع"], "") & filters.private, group=7262737)
async def back_command(bot, msg):
    await show_main_menu(bot, msg)
    
   
async def show_main_menu(bot, msg):
    if msg.from_user.id in SUDORS:
        # قسم البوتات
        bots_section = ReplyKeyboardMarkup([
            [KeyboardButton("صنع بوت"), KeyboardButton("حذف بوت")],
            [KeyboardButton("البوتات المصنوعه")],
            [KeyboardButton("ايقاف البوت"), KeyboardButton("تشغيل البوت")],
            [KeyboardButton("ايقاف البوتات"), KeyboardButton("تشغيل البوتات")],
            [KeyboardButton("حذف البوتات")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # قسم الإحصائيات والفحص
        stats_section = ReplyKeyboardMarkup([
            [KeyboardButton("فحص البوتات"), KeyboardButton("احصائيات البوتات")],
            [KeyboardButton("تصفيه البوتات"), KeyboardButton("الاحصائيات")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # قسم التحديثات
        update_section = ReplyKeyboardMarkup([
            [KeyboardButton("تحديث الصانع"), KeyboardButton("تحديث البوتات")],
            [KeyboardButton("جلب ملف env"), KeyboardButton("تغير الجلسة")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # قسم الإذاعة
        broadcast_section = ReplyKeyboardMarkup([
            [KeyboardButton("اذاعه"), KeyboardButton("اذاعه بالتوجيه")],
            [KeyboardButton("اذاعه عام للمجموعات"), KeyboardButton("اذاعه عام للمستخدمين")],
            [KeyboardButton("اذاعه عام بالتوجيه"), KeyboardButton("اذاعه بالتوجيه للمستخدمين")],
            [KeyboardButton("اذاعه عام بالثبيت")],
            [KeyboardButton("جلب نسخه"), KeyboardButton("رفع نسخه")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)


        # قسم المطورين والإدارة
        admin_section = ReplyKeyboardMarkup([
            [KeyboardButton("رفع مطور"), KeyboardButton("تنزيل مطور")],
            [KeyboardButton("المطورين")],
            [KeyboardButton("حظر"), KeyboardButton("الغاء حظر")],
            [KeyboardButton("المحظورين"), KeyboardButton("مسح المحظورين")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # قسم الإعدادات
        settings_section = ReplyKeyboardMarkup([
            [KeyboardButton("فتح فيجا"), KeyboardButton("قفل فيجا")],
            [KeyboardButton("تفعيل التواصل"), KeyboardButton("تعطيل التواصل")],
            [KeyboardButton("تعين كوكيز"), KeyboardButton("إعادة تهيئة")],
            [KeyboardButton("تفريغ التخزين")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # قسم المعلومات
        info_section = ReplyKeyboardMarkup([
            [KeyboardButton("معلومات الصانع"), KeyboardButton("معلومات التنصيب")],
            [KeyboardButton("الاسكرينات المفتوحه")],
            [KeyboardButton("رجوع")]
        ], resize_keyboard=True)

        # القائمة الرئيسية
        main_menu = ReplyKeyboardMarkup([
            [KeyboardButton("قسم البوتات"), KeyboardButton("قسم الإحصائيات")],
            [KeyboardButton("قسم التحديثات")],
            [KeyboardButton("قسم الإذاعة"), KeyboardButton("قسم المطورين")],
            [KeyboardButton("قسم الإعدادات")],
            [KeyboardButton("قسم المعلومات"), KeyboardButton("INFO")],
            [KeyboardButton("اخفاء الكيبورد")]
        ], resize_keyboard=True)
        
        # عرض لوحة المفاتيح الرئيسية مباشرة بدون رسالة ترحيبية
        await msg.reply(
            f"<b> مرحباً بك عزيزي :</b> {msg.from_user.mention}",
            reply_markup=main_menu,
            quote=True
        )
        
        @bot.on_message(filters.text & filters.private, group=5663)
        async def handle_sections(bot, msg):
            if msg.from_user.id not in SUDORS:
                return

            section = msg.text
            sections = {
                "قسم البوتات": bots_section,
                "قسم الإحصائيات": stats_section,
                "قسم التحديثات": update_section,
                "قسم الإذاعة": broadcast_section,
                "قسم المطورين": admin_section,
                "قسم الإعدادات": settings_section,
                "قسم المعلومات": info_section,
                "التحكم": main_menu
            }
            if section in sections:
                await msg.reply(
                    text=f" انت الان في قسم : <b>{section}</b> ", 
                    reply_markup=sections[section]  
                )

    else:
        # لوحة المفاتيح للمستخدمين العاديين
        reply_markup = ReplyKeyboardMarkup([
            [KeyboardButton("صنع بوت"), KeyboardButton("حذف بوت")],
            [KeyboardButton("تغير الجلسة")],
            [KeyboardButton("INFO")]
        ], resize_keyboard=True)
        
        await msg.reply(
            "<blockquote><b>تم تطويري من قبل فيجا: @TopVeGa</blockquote>\n<blockquote>أقوى تيم برمجيات مصري</b></blockquote>",
            reply_markup=reply_markup,
            quote=True
        )
        

     


# ============ معالجات الأوامر ============

@bot.on_message(filters.text & filters.private, group=5662)
async def handle_commands(bot, msg):
    if msg.from_user.id not in SUDORS:
        return
    
    command = msg.text
    user_id = msg.from_user.id
    commands = {
        "الغاء": cancel_command,
        "اخفاء الكيبورد": hide_keyboard,
        "الاحصائيات": show_stats,
        "تفعيل التواصل": enable_communication,
        "تعطيل التواصل": disable_communication,
        "اذاعه": prepare_broadcast,
        "اذاعه بالتوجيه": prepare_forward_broadcast,
        "اذاعه بالتثبيت": prepare_pin_broadcast,
        "جلب نسخه": backup_users,
        "رفع نسخه": prepare_users_upload
    }
    if command in commands:
        await commands[command](bot, msg)

async def cancel_command(bot, msg):
    """إلغاء جميع الأوامر النشطة"""
    for broadcast_type in BROADCAST_TYPES.values():
        db.delete(f"{msg.from_user.id}{broadcast_type}")
    db.delete(f"{msg.from_user.id}:users_up:{bot_id}")
    await msg.reply("تم الغاء الامر")

async def hide_keyboard(bot, msg):
    """إخفاء لوحة المفاتيح"""
    await msg.reply(
        "» تم اخفاء الكيبورد ارسل /start لعرضه مره اخري",
        reply_markup=ReplyKeyboardRemove(selective=True),
        quote=True
    )



async def prepare_forward_broadcast(bot, msg):
    """تحضير للإذاعة بالتوجيه"""
    await msg.reply(
        "<blockquote>ارسل الاذاعه :-\n❰❪ نص + ملف +متحركه + ملصق + صوره ❫❱</blockquote>", 
        quote=True
    )
    db.set(f"{msg.from_user.id}{BROADCAST_TYPES['forward']}", 1)
    clear_other_broadcasts(msg.from_user.id)

async def prepare_pin_broadcast(bot, msg):
    """تحضير للإذاعة بالتثبيت"""
    await msg.reply(
        "<blockquote>ارسل الاذاعه :-\n❰❪ نص + ملف +متحركه + ملصق + صوره ❫❱</blockquote>", 
        quote=True
    )
    db.set(f"{msg.from_user.id}{BROADCAST_TYPES['pin']}", 1)
    clear_other_broadcasts(msg.from_user.id)

async def backup_users(bot, msg):
    """إنشاء نسخة احتياطية للمستخدمين"""
    wait_msg = await msg.reply("» يـرجـئ الانتـظار...", quote=True)
    await bot.send_document(msg.chat.id, users_backup())
    await wait_msg.delete()
    os.remove("users.txt")

async def prepare_users_upload(bot, msg):
    """تحضير لرفع نسخة المستخدمين"""
    await msg.reply("<blockquote>» ارسل الان نسخه ملف الاعضاء</blockquote>", quote=True)
    db.set(f"{msg.from_user.id}:users_up:{bot_id}", 1)

def clear_other_broadcasts(user_id: int):
    """مسح أنواع الإذاعة الأخرى"""
    for key, value in BROADCAST_TYPES.items():
        if key != current_type:
            db.delete(f"{user_id}{value}")

# ============ معالجة الإذاعة ============
@bot.on_message(filters.private, group=368388)
async def handle_broadcasts(bot, msg):
    if msg.from_user.id not in SUDORS:
        return
    if msg.text in ["اذاعه", "اذاعه بالتوجيه", "اذاعه بالتثبيت", "الغاء", 
                   "رفع نسخه", "• اوامر الاذاعه •", "تعطيل التواصل", 
                   "تفعيل التواصل", "• اوامر التواصل •", "اخفاء الكيبورد", 
                   "الاحصائيات"]:
        return
        
    user_id = msg.from_user.id
    broadcast_stats = {
        "success": 0,
        "failed": 0,
        "total": len(get_users()),
        "deleted_users": 0
    }
    
    broadcast_type = None
    for key, value in BROADCAST_TYPES.items():
        if db.get(f"{user_id}{value}"):
            broadcast_type = key
            db.delete(f"{user_id}{value}")
            break
    
    if not broadcast_type:
        return
    
    progress_msg = await msg.reply("» جاري الإذاعة ..", quote=True)
    for current, user in enumerate(get_users(), 1):
        try:
            user = int(user)
            await send_broadcast(bot, msg, user, broadcast_type)
            broadcast_stats["success"] += 1
            if not db.get(f"{user_id}:flood:{bot_id}"):
                progress = (current / broadcast_stats["total"]) * 100
                await progress_msg.edit(f"» نسبه الاذاعه {int(progress)}%")
                db.set(f"{user_id}:flood:{bot_id}", 1)
                db.expire(f"{user_id}:flood:{bot_id}", 4)
                
        except PeerIdInvalid:
            del_user(user)
            broadcast_stats["deleted_users"] += 1
            broadcast_stats["failed"] += 1
        except Exception as e:
            broadcast_stats["failed"] += 1
    
    report = (
        f"┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈\n<blockquote>╭─ تقرير الإذاعة ──</blockquote>\n"
        f"<blockquote>• نوع الإذاعة: {broadcast_type}</blockquote>\n"
        f"<blockquote>• عدد المستخدمين: {broadcast_stats['total']}</blockquote>\n"
        f"<blockquote>• ناجحة: {broadcast_stats['success']}</blockquote>\n"
        f"<blockquote>• فاشلة: {broadcast_stats['failed']}</blockquote>\n"
        f"<blockquote>• حسابات محذوفة: {broadcast_stats['deleted_users']}</blockquote>\n┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈"
    )
    
    await progress_msg.edit(report)

async def send_broadcast(bot, msg, user_id: int, broadcast_type: str):
    """إرسال الرسالة حسب نوع الإذاعة"""
    if broadcast_type == "normal":
        await msg.copy(user_id)
    elif broadcast_type == "forward":
        await msg.forward(user_id)
    elif broadcast_type == "pin":
        m = await msg.copy(user_id)
        await m.pin(disable_notification=False, both_sides=True)

# ============ معالجة رفع النسخة ============

@bot.on_message(filters.document & filters.private, group=793874)
async def handle_users_upload(bot, msg):
    if msg.from_user.id not in SUDORS:
        return
    
    if not db.get(f"{msg.from_user.id}:users_up:{bot_id}"):
        return
    
    message = await msg.reply("» يـرجـئ الانتـظار...", quote=True)
    await msg.download("./users.txt")
    db.delete(f"botusers&{bot_id}")
    
    with open("./users.txt", "r", encoding="utf8", errors="ignore") as file:
        for user in file.read().splitlines():
            if user and not is_user(user):
                add_new_user(user)
    
    report = (
        f"<blockquote>╮⦿ تم رفع نسخه الاعضاء</blockquote>\n"
        f"<blockquote>╯⦿ عدد الاعضاء : {len(get_users())}</blockquote>"
    )
    
    await message.edit(report)
    try:
        os.remove("./users.txt")
        db.delete(f"{msg.from_user.id}:users_up:{bot_id}")
    except Exception:
        pass

# ============ معالجة التواصل ============

@bot.on_message(filters.private, group=793874)
async def twasl(bot, msg):
	if msg.from_user.id not in SUDORS:
		for user in SUDORS:
			if db.get(f"{user}:twasl:{bot_id}"):
				await msg.forward(user)
	if msg.from_user.id in SUDORS:
		if msg.reply_to_message:
			if msg.reply_to_message.forward_from:
				try:
					await msg.copy(msg.reply_to_message.forward_from.id)
					await msg.reply(f"╮⦿ تم إرسال رسالتك إلى {msg.reply_to_message.forward_from.first_name}\n╯⦿ بنجاح", quote=True)
				except Exception as Error:
					await msg.reply(f"• لم يتم ارسال رسالتك بسبب: {str(Error)}", quote=True)
					pass