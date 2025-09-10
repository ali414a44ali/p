import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant, PeerIdInvalid, UsernameInvalid, ChatAdminRequired
from VeGa import app
from config import OWNER_ID

# تحويل OWNER_ID إلى قائمة إذا كان رقمًا واحدًا
join_locked = False
ch = ""

@app.on_message(filters.command(["تفعيل الاشتراك العام"], "") & filters.private, group=508)
async def lock_joiiin(client, message):
    if (message.from_user.id == OWNER_ID or message.from_user.id == 7654641648):
        global ch
        ask = await app.ask(message.chat.id, f"<b>⭓ᴍᴜꜱɪᴄ✘ᴠᴇɢᴧ♪\n╮⦿  تاكد من رفع البوت مشرف في القناه \n╯⦿  وارسل معرف القناه بدون علامه @\n <code>VeGaOne</code></b>", timeout=300)
        ch = ask.text 
        usr = await client.get_chat(message.from_user.id)
        name = usr.first_name
        global join_locked
        join_locked = True
        await message.reply_text(f"تم تفعيل الاشتراك العام بنجاح")
    else:
        await message.reply_text(f"هييه ياروع هذا الامر لفيجا وبس!")


@app.on_message(filters.command(["تعطيل الاشتراك العام"], "") & filters.private, group=728)
async def unlock_joinn(client, message):
    if (message.from_user.id == OWNER_ID or message.from_user.id == 7654641648):
        usr = await client.get_chat(message.from_user.id)
        name = usr.first_name
        global join_locked
        join_locked = False
        await message.reply_text(f"تم تعطيل الاشتراك العام بنجاح")
    else:
        await message.reply_text(f"هييه ياروع هذا الامر لفيجا وبس!")


@app.on_message(filters.group & filters.text & filters.create(lambda _, __, message: join_locked), group=5028)
async def check_subscription(client, message):
    global ch
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    try:
        await client.get_chat_member(ch, message.from_user.id)
    except:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("اشتراك هنا", url=f"https://t.me/{ch}")]
        ])
        await app.send_message(
            chat_id=message.chat.id,
            text=f"⇜「 {message.from_user.mention} 」\n⇜اشتراك فالقناه اولا\n༄",
            reply_markup=keyboard
        )
        await message.delete()
        return
    message.continue_propagation()


join_private = False   
chhh = ""
@app.on_message(filters.command(["تفعيل الاشتراك برايفت"], "") & filters.private, group=1201201203227)
async def lock_joiiinprivate(client, message):
  global chhh
  ask = await app.ask(message.chat.id, f"<b>⭓ᴍᴜꜱɪᴄ✘ᴠᴇɢᴧ♪</b>\n╮⦿  تاكد من رفع البوت مشرف في القناه \n╯⦿  وارسل معرف القناه بدون علامه @</b>", timeout=300)
  chhh = ask.text 
  usr = await client.get_chat(message.from_user.id)
  name = usr.first_name
  global join_private
  join_private = True
  await message.reply_text(f"تم تفعيل الاشتراك برايفت بنجاح")

@app.on_message(filters.command(["تعطيل الاشتراك برايفت"], "") & filters.private, group=4023150879)
async def unlock_joinprivet(client, message):
   usr = await client.get_chat(message.from_user.id)
   name = usr.first_name
   global join_private
   join_private = False
   await message.reply_text(f"تم تعطيل الاشتراك برايفت بنجاح")


@app.on_message(filters.private & filters.text & filters.create(lambda _, __, message: join_private), group=405012902109)
async def subscripprivate(client, message):
    global chhh
    usr = await client.get_chat(message.from_user.id)
    name = usr.first_name
    try:
        await client.get_chat_member(ch, message.from_user.id)
    except:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("اشتراك هنا", url=f"https://t.me/{chhh}")]
        ])
        await app.send_message(
            chat_id=message.chat.id,
            text=f"⇜「 {message.from_user.mention} 」\n⇜اشتراك فالقناه اولا\n༄",
            reply_markup=keyboard
        )        
        return
    message.continue_propagation()
    
    
    
