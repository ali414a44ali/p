import os 
from pyrogram import Client
from pyrogram import idle
from pyromod import listen
from Maker import *
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden
from Maker import *
from asBASE import asJSON
from asyncio import sleep
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats
from asyncio import sleep
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden
import os 
import asyncio
from pyrogram import Client, idle
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats
from asBASE import asJSON
import os 
import asyncio
from pyrogram import Client, idle
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats
from asBASE import asJSON


db = asJSON("as.json")


TOKEN = "7917365611:AAEINsFYfSjme7nY9iXcD5MnxmFjZXkUoYU"
SUDORS = [7654641648, 8122544723]
SET_CMDS = True


bot = Client(
    name="VeGa",
    api_id=8186557,
    api_hash="efd77b34c69c164ce158037ff5a0d117",
    bot_token=TOKEN,
    plugins=dict(root="Maker")
)

async def start_bot():
    print("[INFO] Source code developed by: @TopVeGa")
    print("[INFO] Starting bot...⚡")
    
    try:
        await bot.start()
        print("[SUCCESS] Bot started successfully🌀")


        if SET_CMDS:
            try:
                commands = [
                    BotCommand("start", "Start the bot"),
                    BotCommand("kim", "About developer"),
                    BotCommand("fox", "About developer"),
                    BotCommand("vega", "About developer"),
                    BotCommand("release", "Version info")
                ]
                await bot.set_bot_commands(commands, scope=BotCommandScopeAllPrivateChats())
                print("[SUCCESS] Bot commands set successfully🔅")
            except Exception as e:
                print(f"[ERROR] Failed to set commands: {str(e)}")

     
        print("[INFO] Notifying developers...🍁")
        for dev_id in SUDORS:
            try:
                await bot.send_message(dev_id, "🤖 Bot started successfully!")
                print(f"[SUCCESS] Notified developer: {dev_id}")
            except PeerIdInvalid:
                print(f"[WARNING] Developer {dev_id} not found")
            except ChatWriteForbidden:
                print(f"[WARNING] No permission to message developer {dev_id}")
            except Exception as e:
                print(f"[ERROR] Failed to notify {dev_id}: {str(e)}")

        print("[INFO] Bot is now running...⚡")
        await idle()

    except Exception as e:
        print(f"[CRITICAL] Bot startup failed: {str(e)}")
    finally:
        try:
            if bot.is_connected:
                await bot.stop()
                print("[INFO] Bot stopped gracefully⛔")
        except Exception as e:
            print(f"[WARNING] Error while stopping bot: {str(e)}")

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("\n[INFO] Bot stopped by user🔺")
    except Exception as e:
        print(f"[FATAL] Unexpected error: {str(e)}")
    finally:
        loop.close()

bot_id = TOKEN.split(":")[0]


    
    
    
    

