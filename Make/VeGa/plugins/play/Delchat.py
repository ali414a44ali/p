from __future__ import annotations
import asyncio
import logging
from typing import Optional, Tuple

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter
from pyrogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPrivileges
from pyrogram.errors import RPCError, UserNotParticipant, ChatAdminRequired, FloodWait, PeerIdInvalid, InviteHashInvalid

from VeGa import app
from VeGa.misc import SUDOERS
from VeGa.utils.database import get_assistant

logger = logging.getLogger(__name__)

# دالة للحصول على مالك المجموعة
async def get_group_owner(client: Client, chat_id: int) -> Optional[User]:
    try:
        async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
                return member.user
    except RPCError as e:
        logger.error(f"Error fetching group owner: {e}")
    return None

async def is_authorized_user(client: Client, chat_id: int, user_id: int) -> Tuple[bool, Optional[User]]:
    owner = await get_group_owner(client, chat_id)
    if not owner:
        return False, None
    return (user_id == owner.id or user_id in SUDOERS), owner

def confirmation_keyboard(command: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ تأكيد", callback_data=f"{command}_confirm"),
            InlineKeyboardButton("❌ إلغاء", callback_data=f"{command}_cancel")
        ]
    ])

async def mention(user_id: int, first_name: str) -> str:
    return f'<a href="tg://user?id={user_id}">{first_name}</a>'

@app.on_message(filters.command(["تنظيف"], "") & filters.group & ~filters.forwarded, group=57643366)
async def deleteall_command_handler(client: Client, message: Message):
    chat = message.chat
    user = message.from_user

    authorized, owner = await is_authorized_user(client, chat.id, user.id)
    if not authorized:
        owner_mention = await mention(owner.id, owner.first_name) if owner else "مالك المجموعة"
        return await message.reply(f"⚠️ فقط {owner_mention} يمكنه استخدام هذا الأمر.")

    try:
        bot_member = await client.get_chat_member(chat.id, client.me.id)
        if not (bot_member.privileges.can_delete_messages and 
                bot_member.privileges.can_invite_users and 
                bot_member.privileges.can_promote_members):
            return await message.reply("🔒 أحتاج صلاحيات حذف الرسائل، دعوة المستخدمين وترقية الأعضاء.")
    except RPCError as e:
        logger.error(f"خطأ في التحقق من الصلاحيات: {e}")
        return await message.reply("❌ خطأ في التحقق من صلاحيات البوت.")

    await message.reply(
        f"⚠️ {user.mention}, هذا الأمر سيقوم بحذف جميع الرسائل في هذه الدردشة. هل تريد المتابعة؟",
        reply_markup=confirmation_keyboard("deleteall")
    )


@app.on_callback_query(filters.regex(r"^deleteall_(confirm|cancel)$"), group=76457754)
async def deleteall_confirmation_handler(client: Client, callback: CallbackQuery):
    action = callback.data.split("_")[1]
    chat = callback.message.chat
    user = callback.from_user

    try:
        if action == "cancel":
            await callback.message.edit_text("❌ تم إلغاء العملية.")
            return

        authorized, owner = await is_authorized_user(client, chat.id, user.id)
        if not authorized:
            return await callback.answer("ليس لديك صلاحية لتأكيد هذا الإجراء.", show_alert=True)

        original_message = callback.message
        await callback.message.edit_text("🔄 بدء عملية الحذف...")
        assistant = await get_assistant(chat.id)
        assistant_client = assistant
        assistant_user = await assistant_client.get_me()

        try:
            await _manage_assistant_membership(client, chat.id, assistant_user.id)
            await _configure_assistant_permissions(client, chat.id, assistant_user.id)
            deleted_count = await _batch_delete_messages(assistant_client, chat.id)
            
            try:
                await original_message.edit_text(f"✅ تم حذف {deleted_count} رسالة بنجاح!")
            except RPCError as e:
                await client.send_message(
                    chat.id,
                    f"✅ تم حذف {deleted_count} رسالة بنجاح!",
                    reply_to_message_id=original_message.id
                )
        except Exception as e:
            logger.error(f"خطأ في الحذف: {e}")
            error_msg = f"❌ حدث خطأ أثناء الحذف: {str(e)}"
            try:
                await original_message.edit_text(error_msg)
            except RPCError:
                await client.send_message(chat.id, error_msg)
        finally:
            await _cleanup_assistant(client, chat.id, assistant_user.id)

    except Exception as e:
        logger.error(f"خطأ غير متوقع في المعالج: {e}")
        # رد فعل احتياطي
        await callback.answer("حدث خطأ. يرجى مراجعة السجلات.", show_alert=True)

async def _manage_assistant_membership(main_client: Client, chat_id: int, assistant_id: int):
    try:
        await main_client.get_chat_member(chat_id, assistant_id)
    except (UserNotParticipant, PeerIdInvalid):
        try:
            try:
                banned = await main_client.get_chat_member(chat_id, assistant_id)
                if banned.status == ChatMemberStatus.BANNED:
                    await main_client.unban_chat_member(chat_id, assistant_id)
            except (UserNotParticipant, PeerIdInvalid):
                pass 

            invite_link = await main_client.create_chat_invite_link(chat_id, member_limit=1)
            await assistant_client.join_chat(invite_link.invite_link)
        except Exception as e:
            logger.error(f"خطأ في عضوية المساعد: {e}")
            raise Exception("فشل في إضافة المساعد إلى المجموعة")

async def _configure_assistant_permissions(main_client: Client, chat_id: int, assistant_id: int):
    try:
        await main_client.promote_chat_member(
            chat_id,
            assistant_id,
            privileges=ChatPrivileges(
                can_delete_messages=True,
                can_invite_users=True,
                can_manage_chat=True
            )
        )
        await asyncio.sleep(1)
    except RPCError as e:
        logger.error(f"خطأ في الترقية: {e}")
        raise Exception("فشل في ضبط صلاحيات المساعد")

# دالة لحذف الرسائل على شكل دفعات
async def _batch_delete_messages(assistant: Client, chat_id: int) -> int:
    total_deleted = 0
    message_ids = []
    async for message in assistant.get_chat_history(chat_id):
        message_ids.append(message.id)
        if len(message_ids) >= 100:
            try:
                await assistant.delete_messages(chat_id, message_ids)
                total_deleted += len(message_ids)
                message_ids = []
            except FloodWait as fw:
                await asyncio.sleep(fw.value + 2)
            except RPCError as e:
                logger.error(f"خطأ في الحذف الجماعي: {e}")
    if message_ids:
        await assistant.delete_messages(chat_id, message_ids)
        total_deleted += len(message_ids)
    return total_deleted

async def _cleanup_assistant(main_client: Client, chat_id: int, assistant_id: int):
    try:
        await main_client.promote_chat_member(
            chat_id,
            assistant_id,
            privileges=ChatPrivileges()
        )
    except RPCError as e:
        logger.warning(f"خطأ في التنظيف: {e}")
        
        
        
