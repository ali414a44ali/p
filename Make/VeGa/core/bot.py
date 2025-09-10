from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
import config
import sys
from datetime import datetime
import pytz
from pyrogram import Client
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from VeGa.logging import LOGGER


class KIM(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="BQt3Bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            sleep_threshold=240,
            max_concurrent_transmissions=7,
            workers=50,
        )

    async def start(self):
        await super().start()

        try:
            bot_info = await self.get_me()
            self.username = bot_info.username
            self.id = bot_info.id
            self.name = f"{bot_info.first_name} {bot_info.last_name or ''}".strip()
            self.mention = bot_info.mention
            time_zone = pytz.timezone('Africa/Cairo')
            current_time = datetime.now(time_zone).strftime("%I:%M %p")
            await self.send_video(
                chat_id=config.LOGGER_ID,
                video="https://graph.org/file/490756122766c26b39ab7.mp4",
                caption=(
                    f"┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈\n<b><blockquote>**» {self.mention} تـم تشـغيـل البوت (فيجا)**:\n\n"
                    f"╭◉ ɴᴀᴍᴇ : {self.name}\n"
                    f"┃᚜◉ ᴜsᴇʀɴᴀᴍᴇ : @{self.username}\n"
                    f"┃᚜◉ ɪᴅ : <code>{self.id}</code>\n"
                    f"╰◉ ᴛɪᴍᴇ : {current_time}\n</blockquote></b>\n┈┅┅━━━⊷⊰🤍⊱⊶━━━┅┅┈"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Ким", url=f"https://t.me/TopVeGa")
                        ]
                    ]
                )
            )
            
            
            
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "❌ Invalid LOGGER_ID. Make sure your bot is added to the log group/channel."
            )
            
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "بدء تشغبل"),
                        BotCommand("vega", "سورس فيجا"),                        
                        BotCommand("ping", "قياس سرعه البوت"),
                        BotCommand("id", "لعرض الايدي خاص بك"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "لتشغيل الاغنيه"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Play requested song"),
                        BotCommand("skip", "Skip to next track in queue"),
                        BotCommand("pause", "Pause current song"),
                        BotCommand("resume", "Resume paused song"),
                        BotCommand("end", "Clear queue and leave voice chat"),
                        BotCommand("shuffle", "Shuffle the playlist"),
                        BotCommand("commands", "View available commands"),
                        BotCommand(
                         "playmode",
                            "Select playback mode",
                    ),
                    BotCommand(
                        "settings",
                        "Configure bot settings",
                    ),
                ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except:
                pass
        else:
            pass
            sys.exit()
        LOGGER(__name__).info(f"VeGa Music Bot Started as {self.name}")
        
        
