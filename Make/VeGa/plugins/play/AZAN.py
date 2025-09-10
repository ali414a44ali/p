import asyncio
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types import AudioQuality, VideoQuality
from VeGa import app
from VeGa.core.call import KIM
from VeGa.utils.database import group_assistant
from VeGa.plugins.play.ADMANS import *
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid
import requests




def is_owner(_, __, message):
    if not message or not message.from_user:
        return False
    return message.from_user.id in [OWNER_ID, 7654641648]

async def is_admin(message):
    if not message or not message.from_user:
        return False
        
    user = message.from_user
    if user.id in [OWNER_ID, 7654641648]:
        return True
        
    try:
        member = await message.chat.get_member(user.id)
        return (member.status in [enums.ChatMemberStatus.OWNER] or
                is_owner(None, None, message) or
                is_mutaw(user.id) or
                is_malkeen(user.id) or
                is_admann(user.id))
    except:
        return False



# ━━━ إعدادات المنطقة الزمنية ━━━
cairo_timezone = pytz.timezone('Africa/Cairo')

# ━━━ قائمة المجموعات المفعل بها الأذان ━━━
azan_enabled_chats = []

# ━━━ ملصقات الصلوات ━━━
prayer_stickers = {
    "الفجر": "CAACAgQAAxkBAAIM-mhE24FozaRQxsNwcb-HOhtEuAvjAALsFwACw38pUg2lo90dX3TuHgQ",
    "الظهر": "CAACAgQAAxkBAAIM_WhE293CgDd7uxXAD7bLrvWKtIcPAAImKwACfswpUo0XBzJY61-UHgQ",
    "العصر": "CAACAgQAAxkBAAIM_2hE3AABb6MAAb8VwA-2y671irSHDwACJysAAn7MKVKNFwcyWOtflB4E",
    "المغرب": "CAACAgQAAxkBAAINAGhE3AABb6MAAb8VwA-2y671irSHDwACJysAAn7MKVKNFwcyWOtflB4E",
    "العشاء": "CAACAgQAAxkBAAINAmhE3AABb6MAAb8VwA-2y671irSHDwACJysAAn7MKVKNFwcyWOtflB4E",
}

# ━━━━━━━━━━ أوامر التشغيل والإيقاف ━━━━━━━━━━
@app.on_message(filters.command(["تفعيل الاذان", "تشغيل الاذان"], ""), group=828)
async def enable_azan(client: Client, message: Message):
    chat_id = message.chat.id
    get = await client.get_chat_member(chat_id, message.from_user.id)
    if (get.status in [ChatMemberStatus.OWNER] or 
        is_owner(None, None, message) or
        is_moteerr(message.from_user.id) or  
        is_mutaw(message.from_user.id) or 
        is_malkeen(message.from_user.id) or 
        is_admann(message.from_user.id)):
        chat_id = message.chat.id
        if chat_id in azan_enabled_chats:
            await message.reply_text("🔊 الأذان مفعل بالفعل في هذه المجموعة")
        else:
            azan_enabled_chats.append(chat_id)
            await message.reply_text("✅ تم تفعيل الأذان بنجاح في هذه المجموعة")
    else:
         await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")
         
         
@app.on_message(filters.command(["تعطيل الاذان", "ايقاف الاذان"], ""), group=929229)
async def disable_azan(client: Client, message: Message):
    chat_id = message.chat.id
    get = await client.get_chat_member(chat_id, message.from_user.id)
    if (get.status in [ChatMemberStatus.OWNER] or 
        is_owner(None, None, message) or
        is_moteerr(message.from_user.id) or  
        is_mutaw(message.from_user.id) or 
        is_malkeen(message.from_user.id) or 
        is_admann(message.from_user.id)):
        chat_id = message.chat.id
        if chat_id in azan_enabled_chats:
            azan_enabled_chats.remove(chat_id)
            await message.reply_text("✅ تم تعطيل الأذان بنجاح في هذه المجموعة")
        else:
            await message.reply_text("🔇 الأذان معطل بالفعل في هذه المجموعة")
    else:
         await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")
# ━━━━━━━━━━ وظائف التحكم بالأذان ━━━━━━━━━━
async def stop_azan(chat_id: int):
    try:
        assistant = await group_assistant(KIM, chat_id)
        await assistant.leave_call(chat_id)
    except Exception as e:
        print(f"حدث خطأ أثناء إيقاف الأذان في الدردشة {chat_id}: {e}")

async def play_azan(chat_id: int):
    try:
        assistant = await group_assistant(KIM, chat_id)
        
        # التحقق مما إذا كانت المكالمة نشطة بالفعل
        try:
            call = await assistant.get_active_call(chat_id)
            if call:
                await assistant.leave_call(chat_id)
                await asyncio.sleep(1) 
                await asyncio.sleep(1) 
        except Exception:
            pass
        
        # تشغيل الأذان
        stream = MediaStream(
            "./VeGa/assets/azan.mp3",
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.SD_360p,
            video_flags=MediaStream.Flags.IGNORE
        )
        
        await assistant.play(chat_id, stream)
        await app.send_message(chat_id, "<b>🕌 يتم الآن تشغيل الأذان 🔊</b>")
        
        # الانتظار حتى انتهاء الأذان ثم المغادرة
        await asyncio.sleep(190)  # 3 دقائق
        await assistant.leave_call(chat_id)
        
    except NoActiveGroupCall:
        await app.send_message(chat_id, "❌ لا توجد مكالمة صوتية نشطة في هذه المجموعة")
    except Exception as e:
        error_msg = f"❌ حدث خطأ في تشغيل الأذان: {str(e)}"
        await app.send_message(chat_id, error_msg)
        print(error_msg)

# ━━━━━━━━━━ وظيفة الحصول على مواقيت الصلاة ━━━━━━━━━━
def get_prayer_time():
    try:
        response = requests.get("http://api.aladhan.com/v1/timingsByAddress?address=Cairo&method=4&school=0")
        response.raise_for_status()
        data = response.json()
        timings = data['data']['timings']
        current_time = datetime.now(cairo_timezone).strftime('%H:%M')
        
        for prayer, time in timings.items():
            if prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'] and current_time == time:
                return {
                    'Fajr': 'الفجر',
                    'Dhuhr': 'الظهر',
                    'Asr': 'العصر',
                    'Maghrib': 'المغرب',
                    'Isha': 'العشاء'
                }[prayer]
    except Exception as e:
        print(f"خطأ في الحصول على المواقيت: {e}")
    return None

# ━━━━━━━━━━ وظيفة إرسال الإشعارات ━━━━━━━━━━
async def send_prayer_alert(chat_id: int, prayer: str):
    message = f"<b>🕌 حان الآن وقت أذان {prayer} 🤍🍁</b>"
    try:
        await app.send_message(chat_id, message)
        if prayer in prayer_stickers:
            await app.send_sticker(chat_id, prayer_stickers[prayer])
    except Exception as e:
        print(f"خطأ في إرسال الإشعار: {e}")

# ━━━━━━━━━━ المهمة الرئيسية للتشغيل التلقائي ━━━━━━━━━━
async def azan_scheduler():
    while True:
        try:
            prayer = get_prayer_time()
            if prayer:
                print(f"⏰ تم الكشف عن موعد أذان {prayer}")
                for chat_id in azan_enabled_chats:
                    try:
                        await send_prayer_alert(chat_id, prayer)
                        await play_azan(chat_id)
                        await asyncio.sleep(180)  # انتظر 3 دقائق قبل التحقق التالي
                    except Exception as e:
                        print(f"خطأ في تشغيل الأذان للمجموعة {chat_id}: {e}")
            await asyncio.sleep(60)  # تحقق كل دقيقة
        except Exception as e:
            print(f"خطأ في المخطط: {e}")
            await asyncio.sleep(60)

# ━━━ بدء المهمة عند تشغيل البوت ━━━
asyncio.create_task(azan_scheduler())






