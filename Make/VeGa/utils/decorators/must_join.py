from pyrogram.enums import ChatType
from VeGa import app
from pyrogram.types import Message, InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb
from pyrogram.errors import UserNotParticipant
import asyncio 
import requests
import json
from VeGa.utils.database import get_must, get_must_ch
from config import BOT_TOKEN


def must_join_ch(kimy):
  async def ch_user(c,msg):
    if msg.chat.type != ChatType.CHANNEL:
      if (await get_must(app.username)) and (await get_must_ch(app.username) == "مفعل"):
        i = await get_must(app.username)
        s = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id=@{i}&user_id={msg.from_user.id}")
        data = s.json()
        if data["ok"] and data["result"]["status"] in ["member","creator","administrator"]:
          return await kimy(c,msg)
        else:
          return await msg.reply(f"<b>⭓ᴍᴜˢɪᴄ♪〩⸢ᴠᴇɢᴧ♪\n<blockquote>╮⊚ عـزيزي : {msg.from_user.mention}\n╯⊚ اشترك فالقناه اولا لتشغيل الاغاني</b></blockquote>",disable_web_page_preview=True,reply_markup=ikm([[ikb("اضغط للاشتراك بالقناه.",url=f"https://t.me/{i}")],]))
    return await kimy(c,msg)
  return ch_user
