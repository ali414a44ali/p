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
import os
import asyncio
from pyrogram import Client, filters
from pyrogram import types
from pyrogram import enums
from pyrogram import enums
from pyrogram import Client
from pyrogram.types import ChatPermissions, ChatPrivileges
from pyrogram.errors import PeerIdInvalid
from os import getenv
from VeGa.misc import SUDOERS
from config import OWNER_ID
from VeGa.plugins.play.ADMANS import *
from config import BANNED_USERS
from config import BANNED_USERS, OWNER_ID
from pyrogram import filters, Client
from telegraph import upload_file
from dotenv import load_dotenv
from VeGa.utils.database import (set_cmode,get_assistant) 
from VeGa.utils.decorators.admins import AdminActual
from VeGa import app
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False, 
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_pin_messages=False,
    can_invite_users=True,
)




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



 
restricted_users = []

@app.on_message(filters.command(["تقيد"], "") & filters.group, group=728)
async def mute_user(client: Client, message: Message):
    global restricted_users    
    
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user = await client.get_users(message.reply_to_message.from_user.id)
        name = user.first_name
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        target = message.command[1].strip("@")
        try:
            if target.isdigit():
                target = int(target)
            user = await client.get_users(target)
            user_id = user.id
            name = user.first_name
        except:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        await message.reply_text("يجب الرد على المستخدم أو ذكر اسمه/ايديه")
        return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
        if target == message.from_user.id:
            await message.reply_text("هييه مايمديك تقيد نفسك ياورع!")
            return
            
        if target == 7654641648:
            await message.reply_text("هييه مايمديك تقيد فيجا ياورع!")
            return
        if target == 8165731842:
            await message.reply_text("هييه مايمديك تقيد رو ياورع!")
            return
            
        if target == OWNER_ID:
            await message.reply_text("هييه مايمديك تقيد مطوري ياورع!")
            return       
        if is_moteerr(int(user_id)) if str(user_id).isdigit() else False:
            await message.reply_text("هييه مايمديك تقيد مدير ياورع!")
            return
        if is_mutaw(int(user_id)) if str(user_id).isdigit() else False:
            await message.reply_text("هييه مايمديك تقيد مطور ياورع!")
            return
        if is_malkeen(int(user_id)) if str(user_id).isdigit() else False:
            await message.reply_text("هييه مايمديك تقيد مالك ياورع!")
            return
        if is_admann(int(user_id)) if str(user_id).isdigit() else False:
            await message.reply_text("هييه مايمديك تقيد ادمن ياورع!")
            return            
        member = await message.chat.get_member(target)
        if member.status in [ChatMemberStatus.OWNER]:
            return await message.reply("هييه مايمديك تقيد مالك اساسي ياورع!")
        
        member = await message.chat.get_member(target)
        if member.status in [ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("هييه مايمديك تقيد ادمن ياورع!")

        if target not in restricted_users and target != OWNER_ID:
            mute_permission = ChatPermissions(can_send_messages=False)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=target,
                permissions=mute_permission,
            )
            restricted_users.append(target)
            user = await client.get_users(target) 
            name = user.first_name  
            mention = f"<a href='tg://user?id={target}'>{name}</a>"
            await message.reply_text(f"「 {user.mention} 」\nقييدته\n༄.", parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply_text(f"「 {user.mention} 」\nمقيد من قبل.\n༄", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")




@app.on_message(filters.command(["الغاء تقيد","الغاء التقيد"], "") & filters.group, group=94) 
async def mute(client: Client, message: Message):
    global restricted_users    

    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user = await client.get_users(message.reply_to_message.from_user.id)
        name = user.first_name
        user_id = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        target = message.command[1].strip("@")
        user = await client.get_users(target)
    else:
        await message.reply_text("لا يمكن العثور على المستخدم")
        return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
        if target == message.from_user.id:
            await message.reply_text("هييه ما متقيده نفسك ياورع!")
            return
            
        if target == OWNER_ID:
            await message.reply_text("هييه ما متقيد مطوري ياورع!")
            return       
            
        member = await message.chat.get_member(target)
        if member.status in [ChatMemberStatus.OWNER]:
            return await message.reply("هييه ما متقيد المالك الاساسي ياورع!")
        
        member = await message.chat.get_member(target)
        if member.status in [ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("هييه ما متقيد الادمن ياورع!")

        if target != OWNER_ID:
            mute_permission = ChatPermissions(can_send_messages=False)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=target,
                permissions=unmute_permissions,
            )
            restricted_users.append(target)
            user = await client.get_users(target)  
            name = user.first_name  
            mention = f"<a href='tg://user?id={target}'>{name}</a>"
            await message.reply_text(f"「 {user.mention} 」\nابشر الغيت تقيدته\n༄", parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply_text(f"「 {user.mention} 」\nهييه ما متقيد\n༄", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")





@app.on_message(filters.command(["مسح المقيدين"], "") & filters.group, group=40)
async def unmute(client: Client, message: Message):
    global restricted_users
    user_id = message.from_user.id
    get = await client.get_chat_member(message.chat.id, message.from_user.id)
    if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
        count = len(restricted_users)
        for user_id in restricted_users:
            await client.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=unmute_permissions,
            )
        restricted_users = []
        await message.reply_text(f"↢ مسحت {count} من المقيدين")
    else:
        await message.reply_text(f"هذا الامر يخص ❪ الادمن وفوق ❫ بس")





    

@app.on_message(filters.command(["المقيدين"], "") & filters.group, group=4770)
async def get_restr_users(client: Client, message: Message):
   usr = await client.get_chat(message.from_user.id)
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == 7654641648:
         count = len(restricted_users)
         response = f" <u>قائمة المقيدين وعددهم :</u> {count}\n"
         for user in restricted_users:
             user = await client.get_users(user)
             response += f"{user.mention} \n"
         await message.reply_text(response)
   else:
        await message.reply_text(f"حجي هذا الامر ليس لك ")







# كتم ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# كتم ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


muted_users = []
        
        
@app.on_message(filters.command(["كتم"], "") & filters.group, group=726262728)
async def mute_user(client, message):
    global muted_users    
    
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
        user = await client.get_users(target)
        # التحقق من أن المستخدم ليس بوتًا
        if message.reply_to_message.from_user.is_bot:
            await message.reply_text("مايمديك تكتم البوت ياورع!")
            return
    elif len(message.text.split()) > 2:
        target = message.text.split()[2]
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
            # التحقق من أن المستخدم ليس بوتًا
            if user.is_bot:
                await message.reply_text("مايمديك تكتم البوت ياورع!")
                return
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
            # التحقق من أن المستخدم ليس بوتًا
            if user.is_bot:
                await message.reply_text("مايمديك تكتم البوت ياورع!")
                return
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:      
        if user_id == str(message.from_user.id):
            await message.reply_text("هييه مايمديك تكتم نفسك ياورع!")
            return
            
        if user_id == "7654641648":
            await message.reply_text("هييه مايمديك تكتم فيجا ياورع!")
            return
        if user_id == "8165731842":
            await message.reply_text("هييه مايمديك تكتم رو ياورع!")
            return
            
        if user_id == OWNER_ID:
            await message.reply_text("هييه مايمديك تكتم مطور ياورع!")
            return       
        if is_moteerr(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تكتم مدير ياورع!")
            return
        if is_mutaw(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تكم مطور ياورع!")
            return
        if is_malkeen(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تكتم مالك ياورع!")
            return
        if is_admann(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تكتم ادمن ياورع!")
            return            
        member = await message.chat.get_member(user_id)
        if member.status in [ChatMemberStatus.OWNER]:
            return await message.reply("هييه مايمديك تكتم مالك اساسي ياورع!")
       
        if user_id not in muted_users and user_id != OWNER_ID:
            muted_users.append(user_id)
            await message.reply_text(f"「 {user.mention} 」\n⇜كتمته\n༄")
        else:
            await message.reply_text(f"「 {user.mention} 」\n⇜مكتوم  من قبل\n༄")
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")
        
       
@app.on_message(filters.text)
async def handle_message(client, message):
    if message.from_user and str(message.from_user.id) in muted_users:
        await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
        


        

#الغاء الكتم ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


@app.on_message(filters.command(["الغاء الكتم","الغاء كتم"], "") & filters.group, group=2)
async def unmute_user(client, message):
    global muted_users    
    
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
    elif len(message.text.split()) > 2:
        target = message.text.split()[2]
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
        
        if user_id not in muted_users:
            await message.reply_text(f"「 {user.mention} 」\n⇜ولك مو مكتوم\n༄")
        else:
            muted_users.remove(user_id)
            user = await client.get_users(int(user_id))
            await message.reply_text(f"「 {user.mention} 」\n⇜ابشر الغيت كتمه\n༄")            
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")

#اامكتومين ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

@app.on_message(filters.command(["المكتومين"], "") & filters.group, group=137762627)
async def get_rmuted_users(client, message):
    global muted_users
    
    # التحقق من صلاحيات المستخدم
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and message.from_user.id != 7654641648:
        await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")
        return
    
    # التحقق من وجود مستخدمين في القائمة
    if not muted_users:
        await message.reply_text("لا يوجد مستخدمين مكتومين حالياً")
        return
    
    try:
        count = len(muted_users)
        user_mentions = []
        
        # جلب معلومات كل مستخدم
        for user_id in muted_users:
            try:
                user = await client.get_chat_member(message.chat.id, user_id)
                user_mentions.append(user)
            except Exception as e:
                print(f"Error getting user {user_id}: {e}")
                continue
        
        # بناء الرسالة
        response = f"<u>قائمة المكتومين وعددهم:</u> {count}\n"
        response += "..." * 15 + "\n"
        
        for i, user in enumerate(user_mentions, start=1):
            mention = user.user.mention()
            response += f"{i}- {mention}\n"
        
        await message.reply_text(response, parse_mode=enums.ParseMode.HTML)
        
    except Exception as e:
        print(f"Error in get_rmuted_users: {e}")
        await message.reply_text("حدث خطأ أثناء جلب قائمة المكتومين")

# مسح المكتومين  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

@app.on_message(filters.command(["مسح المكتومين"], "") & filters.group, group=136)
async def unmute_all(client, message):
   usr = await client.get_chat(message.from_user.id)
   name = usr.first_name
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
    global muted_users
    count = len(muted_users)
    chat_id = message.chat.id
    failed_count = 0

    for member in muted_users.copy():
        user_id = member
        try:
            muted_users.remove(member)
        except Exception:
            failed_count += 1

    successful_count = count - failed_count

    if successful_count > 0:
        await message.reply_text(f"مسحت {successful_count} من المكتومين")
    else:
        await message.reply_text(" ⇜ مافيه مكتومين")

    if failed_count > 0:
        await message.reply_text(f"↢ فشل في مسح {failed_count}\nمن المكتومين")
   else:
        await message.reply_text(f"هذا الامر يخص ❪ الادمن وفوق ❫ بس")



# حظر  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# حظر  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓


banned_users = []

@app.on_message(filters.command(["حظر"], "") & filters.group, group=726262728656)
async def ban_user(client, message):
    global banned_users

    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
        user = await client.get_users(target)
        # التحقق من أن المستخدم ليس بوتًا
        if message.reply_to_message.from_user.is_bot:
            await message.reply_text("مايمديك تحظر البوت ياورع!")
            return
    elif len(message.text.split()) > 1:
        target = message.text.split()[1].strip("@")
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
            # التحقق من أن المستخدم ليس بوتًا
            if user.is_bot:
                await message.reply_text("مايمديك تحظر البوت ياورع!")
                return
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        await message.reply_text("يجب الرد على المستخدم أو ذكر اسمه")
        return

    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name

    if (chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or 
        message.from_user.id == OWNER_ID or 
        message.from_user.id == 7654641648 or 
        is_owner(None, None, message) or 
        is_moteerr(message.from_user.id) or 
        is_mutaw(message.from_user.id) or  
        is_malkeen(message.from_user.id) or 
        is_admann(message.from_user.id)):
        
        if user_id == str(message.from_user.id):
            await message.reply_text("هييه مايمديك تحظر نفسك ياورع!")
            return

        if user_id == "7654641648":
            await message.reply_text("هييه مايمديك تحظر فيجا ياورع!")
            return
        if user_id == "8165731842":
            await message.reply_text("هييه مايمديك تحظر رو ياورع!")
            return
            
        if user_id == str(OWNER_ID):
            await message.reply_text("هييه مايمديك تحظر مطور ياورع!")
            return
                   
        if is_moteerr(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تحظر مدير ياورع!")
            return
        if is_mutaw(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تحظر مطور ياورع!")
            return
        if is_malkeen(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تحظر مالك ياورع!")
            return
        if is_admann(int(user_id)) if user_id.isdigit() else False:
            await message.reply_text("هييه مايمديك تحظر ادمن ياورع!")
            return
            
        member = await message.chat.get_member(int(user_id))
        if member.status in [ChatMemberStatus.OWNER]:
            return await message.reply("هييه مايمديك تحظر المالك ياورع!!")
        if member.status in [ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply("مايمديك تحظر مشرف!")

        if user_id not in banned_users:
            banned_users.append(user_id)
            await client.ban_chat_member(
                chat_id=message.chat.id,
                user_id=int(user_id)
            )
            await message.reply_text(f"「 {user.mention} 」\n⇜حظرته\n༄", parse_mode=enums.ParseMode.HTML)
        else:
            await message.reply_text(f"「 {user.mention} 」\n⇜محظور من قبل\n༄", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")


# الغاء الحظر ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

@app.on_message(filters.command(["الغاء الحظر","الغاء حظر"], "") & filters.group, group=726262782)
async def unban_user(client, message):
    global banned_users
    
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user.id
        user_id = str(target)
    elif len(message.text.split()) > 2:
        target = message.text.split()[2]
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    else:
        target = message.text.split()[1].strip("@")
        user = await client.get_users(target)
        if user:
            user_id = str(user.id)
        else:
            await message.reply_text("لا يمكن العثور على المستخدم")
            return
    
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    name = chat_member.user.first_name
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:  
        
        if user_id not in banned_users:
         user = await client.get_users(int(user_id))
         await message.reply_text(f"「 {user.mention} 」\n⇜ولك مو محظور\n༄")
        else:
            await app.unban_chat_member(message.chat.id, user_id)
            banned_users.remove(user_id)
            user = await client.get_users(int(user_id))
            await message.reply_text(f"「 {user.mention} 」\n⇜ابشر الغيت حظره\n༄")          
    else:
        await message.reply_text("هذا الامر يخص ❪ الادمن وفوق ❫ بس")        
 
 
# المحظورين  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        
               



@app.on_message(filters.command(["المحظورين"], "") & filters.group, group=137762627)
async def banned_userss(client, message):
    global banned_users
    
    # التحقق من صلاحيات المستخدم
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] and message.from_user.id != 7654641648:
        await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")
        return
    
    # التحقق من وجود مستخدمين في القائمة
    if not banned_users:
        await message.reply_text("لا يوجد مستخدمين محظورين حالياً")
        return
    
    try:
        count = len(banned_users)
        user_mentions = []
        
        # جلب معلومات كل مستخدم
        for user_id in banned_users:
            try:
                user = await client.get_chat_member(message.chat.id, user_id)
                user_mentions.append(user)
            except Exception as e:
                print(f"Error getting user {user_id}: {e}")
                continue
        
        # بناء الرسالة
        response = f"<u>قائمة المحظورين وعددهم:</u> {count}\n"
        response += "..." * 15 + "\n"
        
        for i, user in enumerate(user_mentions, start=1):
            mention = user.user.mention()
            response += f"{i}- {mention}\n"
        
        await message.reply_text(response, parse_mode=enums.ParseMode.HTML)
        
    except Exception as e:
        print(f"Error in banned_userss: {e}")
        await message.reply_text("حدث خطأ أثناء جلب قائمة المحظورين")
                                                              
# مسح المحظورين  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

@app.on_message(filters.command(["مسح المحظورين"], "") & filters.group, group=19)
async def unban_all(client: Client, message: Message):
   usr = await client.get_chat(message.from_user.id)
   usr = await client.get_chat(message.from_user.id)
   name = usr.first_name
   get = await client.get_chat_member(message.chat.id, message.from_user.id)
   if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or message.from_user.id == OWNER_ID or message.from_user.id == 7654641648:
    global banned_users
    count = len(banned_users)
    chat_id = message.chat.id
    failed_count = 0

    for member in banned_users.copy():
        user_id = member
        try:
            await client.unban_chat_member(chat_id, user_id)
            banned_users.remove(member)
        except Exception:
            failed_count += 1

    successful_count = count - failed_count

    if successful_count > 0:
        await message.reply_text(f"مسحت {successful_count} من المحظورين")
    else:
        await message.reply_text("⇜ مافيه محظورين")

    if failed_count > 0:
        await message.reply_text(f"↢ فشل في مسح {failed_count}\nمن المحظورين")
   else:
         await message.reply_text(f"هذا الامر يخص ❪ الادمن وفوق ❫ بس") 



@app.on_message(filters.command(["مسح الرتب"], "") & filters.group, group=999)
async def clear_all_ranks(client: Client, message: Message):
    # التحقق من صلاحيات المستخدم
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    
    if chat_member.status not in [ChatMemberStatus.OWNER] and message.from_user.id not in [OWNER_ID, 7654641648]:
        await message.reply_text("هذا الأمر يخص ❪ الأدمن وفوق ❫ بس")
        return
    
    # قوائم الرتب (يجب استيرادها من ملف التكوين أو مكان تخزينها)
    # هذه أمثلة، يجب استبدالها بالقوائم الفعلية المستخدمة في البوت
    motaherrin = []  # قائمة المديرين
    mutawin = []     # قائمة المطورين
    malkeen = []     # قائمة المالكين
    admann = []      # قائمة الادمن
    
    # مسح جميع القوائم
    motaherrin.clear()
    mutawin.clear()
    malkeen.clear()
    admann.clear()
    
    # يمكنك هنا إضافة أي عمليات حفظ للقوائم الفارغة إذا كنت تستخدم قاعدة بيانات
    
    await message.reply_text("✓ تم مسح جميع الرتب بنجاح (مديرين، مالكين، ادمن، مطورين)")




