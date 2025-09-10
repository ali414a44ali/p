import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from datetime import datetime

from pyrogram import enums
import config
from config import OWNER_ID
from os import getenv
import random
from random import choice
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions, Message, CallbackQuery
from pyrogram.enums import ChatMemberStatus, ChatType
import asyncio
from VeGa.misc import db
from config import BANNED_USERS, lyrical
from VeGa import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from VeGa.core.call import KIM
from VeGa.utils import seconds_to_min, time_to_seconds
from VeGa.utils.channelplay import get_channeplayCB
from VeGa.utils.decorators.language import languageCB
from VeGa.utils.decorators.play import PlayWrapper
from VeGa.utils.decorators.must_join import must_join_ch
from VeGa.utils.formatters import formats
from VeGa.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from VeGa.utils.logger import play_logs
from VeGa.utils.stream.stream import stream
from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
import logging
from VeGa.misc import db
from VeGa.utils.thumbnails import get_thumb
LOGGER = logging.getLogger(__name__)







OWNER_ID = getenv("OWNER_ID")











@app.on_message(filters.command(["مين شغل","م شغل","مين مشغل"], ""), group=5880)
async def playingy(client, message):
    chat_id = message.chat.id
    try:
        playing = db.get(chat_id)
        
        if not playing:
            return await message.reply_text("🚫 لا يوجد أي شيء يتم تشغيله حالياً")
            
        if not isinstance(playing, list) or len(playing) == 0:
            return await message.reply_text("⚠️ بيانات التشغيل غير صالحة")
            
        current_track = playing[0]
        user_id = current_track.get("by") 
        song_title = current_track.get("title", "غير معروف")
        duration = current_track.get("dur", "غير معروف")
        
        if not user_id:
            return await message.reply_text("⚠️ لا يمكن تحديد المستخدم الذي قام بالتشغيل")
        
        try:
            user = await client.get_users(user_id)
            user_mention = user.mention
        except PeerIdInvalid:
            user_mention = f"المستخدم ({user_id})"
        except Exception as e:
            LOGGER.error(f"Error getting user info: {e}")
            user_mention = f"المستخدم ({user_id})"
        response = (
            f"🎧 <b>• معلومات التشغيل الحالي</b>\n\n"
            f"👤 <b>• الشخص الذي شغل:</b> {user_mention}\n\n"
            f"🎵 <b>• الأغنية:</b> {song_title}\n"
            f"⏳ <b>• المدة:</b> {duration}"
        )
        if current_track.get("vidid"):
            try:
                thumb = await get_thumb(current_track["vidid"])
                await message.reply_photo(
                    photo=thumb,
                    caption=response,
                    reply_to_message_id=message.id
                )
                return
            except Exception as e:
                LOGGER.error(f"Error sending photo: {e}")
        
        await message.reply_text(response, reply_to_message_id=message.id)
        
    except Exception as e:
        LOGGER.error(f"Error in playingy command: {e}", exc_info=True)
        await message.reply_text("⚠️ حدث خطأ أثناء جلب معلومات التشغيل")




music_global = False  # False يعني الميوزك مفعل | True يعني معطل

@app.on_message(filters.command(["قفل الميوزك عام", "تعطيل الميوزك عام"], ""), group=82826389)
async def disable_music_global(client, message):
    if str(message.from_user.id) == OWNER_ID:
        global music_global
        if music_global:
            return await message.reply_text("الميوزك معطل بالفعل **عموماً** في كل الجروبات ♪")
        music_global = True
        await message.reply_text("✓ تم **تعطيل الميوزك عموماً** في كل الجروبات ♪")
    else:
        await message.reply_text("هذا الأمر يخص ❪ المطور الاساسي ❫ بس")

@app.on_message(filters.command(["فتح الميوزك عام", "تفعيل الميوزك عام"], ""), group=82826389)
async def enable_music_global(client, message):
    if str(message.from_user.id) == OWNER_ID:
        global music_global
        if not music_global:
            return await message.reply_text("الميوزك مفعل بالفعل **عموماً** في كل الجروبات ♪")
        music_global = False
        await message.reply_text("✓ تم **تفعيل الميوزك عموماً** في كل الجروبات ♪")
    else:
        await message.reply_text("هذا الأمر يخص ❪ المطور الاساسي ❫ بس")



@app.on_message(filters.command(["تشغيل", "شغل", "فيديو", "فديو"], "") & ~BANNED_USERS, group=1)
@app.on_message(
    filters.command(
        [
            "play",
            "vplay",
            "cplay",
            "cvplay",
            "playforce",
            "vplayforce",
            "cplayforce",
            "cvplayforce",
        ]
    )
    & filters.group
    & ~BANNED_USERS, group=1221
)
 
@must_join_ch
@PlayWrapper
async def play_command(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    if music_global:  # إذا كان التعطيل عاما
        return await message.reply_text("⇜االميوزك معطل  بواسطه المطور الاساسي")
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else random.choice("⚡")
    )
    
    plist_id, plist_type, spotify, slider = None, None, None, None
    user_id = message.from_user.id if message.from_user else "1121532100"
    user_name = message.from_user.first_name if message.from_user else message.chat.title
    username = f"@{message.from_user.username}" if message.from_user and message.from_user.username else user_name

    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message else None
    )

    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])

        duration_min = seconds_to_min(audio_telegram.duration)
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
            )

        file_path = await Telegram.get_filepath(audio=audio_telegram)
        downloaded = await Telegram.download(_, message, mystic, file_path)
        if downloaded:
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)

            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
                return await mystic.edit_text(err)

            return await mystic.delete()
        return

    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message else None
    )

    if video_telegram:
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                        _["play_7"].format(" | ".join(formats))
                    )
            except:
                return await mystic.edit_text(
                    _["play_7"].format(" | ".join(formats))
                )

        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])

        file_path = await Telegram.get_filepath(video=video_telegram)
        downloaded = await Telegram.download(_, message, mystic, file_path)
        if downloaded:
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram, file_path)

            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
                return await mystic.edit_text(err)

            return await mystic.delete()
        return

    if url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(url, config.PLAYLIST_FETCH_LIMIT, user_id)
                except:
                    return await mystic.edit_text(_["play_3"])

                plist_type = "yt"
                plist_id = (url.split("="))[1].split("&")[0] if "&" in url else (url.split("="))[1]
                img = config.PLAYLIST_VIDS_URL
                cap = _["play_9"]
                streamtype = "playlist"

            else:
                try:
                    details, track_id = await YouTube.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
                streamtype = "youtube"

        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID or not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text(
                    "»  sᴘᴏᴛɪғʏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ʏᴇᴛ.\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
                )

            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
                streamtype = "youtube"

            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                plist_type = "spplay"
                img = config.SPOTIFY_PLAYLIST_IMG_URL
                cap = _["play_11"].format(app.mention, message.from_user.mention)
                streamtype = "playlist"

            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                plist_type = "spalbum"
                img = config.SPOTIFY_ALBUM_IMG_URL
                cap = _["play_11"].format(app.mention, message.from_user.mention)
                streamtype = "playlist"

            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                plist_type = "spartist"
                img = config.SPOTIFY_ARTIST_IMG_URL
                cap = _["play_11"].format(message.from_user.first_name)
                streamtype = "playlist"

            else:
                return await mystic.edit_text(_["play_15"])

        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
                streamtype = "youtube"

            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except:
                    return await mystic.edit_text(_["play_3"])

                plist_type = "apple"
                img = url
                cap = _["play_12"].format(app.mention, message.from_user.mention)
                streamtype = "playlist"

            else:
                return await mystic.edit_text(_["play_3"])

        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except:
                return await mystic.edit_text(_["play_3"])

            img = details["thumb"]
            cap = _["play_10"].format(details["title"], details["duration_min"])
            streamtype = "youtube"

        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except:
                return await mystic.edit_text(_["play_3"])

            if details["duration_sec"] > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
                )

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="soundcloud",
                    forceplay=fplay,
                )
            except Exception as e:
                err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
                return await mystic.edit_text(err)

            return await mystic.delete()

        else:
            try:
                await KIM.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(_["black_9"])
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=_["play_17"],
                )
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))

            await mystic.edit_text(_["str_2"])
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    url,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=video,
                    streamtype="index",
                    forceplay=fplay,
                )
            except Exception as e:
                err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
                return await mystic.edit_text(err)

            return await play_logs(message, streamtype="M3U8 or Index Link")

    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup(_)
            return await mystic.edit_text(
                _["play_18"],
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")

        try:
            details, track_id = await YouTube.track(query)
        except:
            return await mystic.edit_text(_["play_3"])

        streamtype = "youtube"

    if str(playmode) == "Direct":
        if not plist_type:
            if details.get("duration_min"):
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec and duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
                    )
            else:
                buttons = livestream_markup(
                    _,
                    track_id,
                    user_id,
                    "v" if video else "a",
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                return await mystic.edit_text(
                    _["play_13"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype=streamtype,
                spotify=spotify,
                forceplay=fplay,
            )
        except Exception as e:
            err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
            return await mystic.edit_text(err)

        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)

    else:
        if plist_type:
            ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(
                _,
                ran_hash,
                user_id,
                plist_type,
                "c" if channel else "g",
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_photo(
                photo=(details["thumb"] if plist_type == "yt" else (details if plist_type == "apple" else img)),
                caption=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")

        else:
            if slider:
                buttons = slider_markup(
                    _,
                    track_id,
                    user_id,
                    query,
                    0,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption=_["play_10"].format(
                        details["title"].title(),
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype="Searched on YouTube")

            else:
                buttons = track_markup(
                    _,
                    track_id,
                    user_id,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption=_["play_10"].format(
                        details["title"],
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype="URL Search Inline")

@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS, group=2234)
@languageCB

async def play_music(client, CallbackQuery, _):
    try:
        callback_data = CallbackQuery.data.split(None, 1)[1]
        vidid, user_id, mode, cplay, fplay = callback_data.split("|")

        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)

        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)

        user_name = CallbackQuery.from_user.first_name
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()

        mystic = await CallbackQuery.message.reply_text(
            _["play_2"].format(channel) if channel else random.choice("⚡")
        )

        details, track_id = await YouTube.track(vidid, videoid=vidid)

        if details.get("duration_min"):
            duration_sec = time_to_seconds(details["duration_min"])
            if duration_sec and duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(config.DURATION_LIMIT_MIN, app.mention)
                )
        else:
            buttons = livestream_markup(
                _,
                track_id,
                CallbackQuery.from_user.id,
                mode,
                "c" if cplay == "c" else "g",
                "f" if fplay else "d",
            )
            return await mystic.edit_text(
                _["play_13"], reply_markup=InlineKeyboardMarkup(buttons)
            )

        video = mode == "v"
        forceplay = fplay == "f"

        await stream(
            _,
            mystic,
            CallbackQuery.from_user.id,
            details,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="youtube",
            forceplay=forceplay,
        )

        await mystic.delete()

    except Exception as e:
        err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
        return await CallbackQuery.message.reply_text(err)

@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)

async def anonymous_check(client, CallbackQuery):
    try:
        await CallbackQuery.answer(
            "» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ :\n\n"
            "ᴏᴘᴇɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs.\n"
            "-> ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs\n-> ᴄʟɪᴄᴋ ᴏɴ ʏᴏᴜʀ ɴᴀᴍᴇ\n"
            "-> ᴜɴᴄʜᴇᴄᴋ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.",
            show_alert=True,
        )
    except:
        pass

@app.on_callback_query(filters.regex("AnniePlaylists") & ~BANNED_USERS, group=245)
@languageCB

async def play_playlists_command(client, CallbackQuery, _):
    try:
        callback_data = CallbackQuery.data.split(None, 1)[1]
        videoid, user_id, ptype, mode, cplay, fplay = callback_data.split("|")

        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)

        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
        user_name = CallbackQuery.from_user.first_name
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()

        mystic = await CallbackQuery.message.reply_text(
            _["play_2"].format(channel) if channel else random.choice("⚡")
        )

        videoid = lyrical.get(videoid)
        video = mode == "v"
        forceplay = fplay == "f"
        spotify = True

        if ptype == "yt":
            spotify = False
            result = await YouTube.playlist(videoid, config.PLAYLIST_FETCH_LIMIT, CallbackQuery.from_user.id, True)
        elif ptype == "spplay":
            result, _ = await Spotify.playlist(videoid)
        elif ptype == "spalbum":
            result, _ = await Spotify.album(videoid)
        elif ptype == "spartist":
            result, _ = await Spotify.artist(videoid)
        elif ptype == "apple":
            result, _ = await Apple.playlist(videoid, True)
        else:
            return

        await stream(
            _,
            mystic,
            CallbackQuery.from_user.id,
            result,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="playlist",
            spotify=spotify,
            forceplay=forceplay,
        )

        await mystic.delete()

    except Exception as e:
        err = e if type(e).__name__ == "AssistantErr" else _["general_2"].format(type(e).__name__)
        return await CallbackQuery.message.reply_text(err)

@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS, group=223)
@languageCB

async def slider_queries(client, CallbackQuery, _):
    try:
        callback_data = CallbackQuery.data.split(None, 1)[1]
        what, rtype, query, user_id, cplay, fplay = callback_data.split("|")

        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)

        rtype = int(rtype)
        query_type = (rtype + 1) if what == "F" else (rtype - 1)

        if query_type > 9:
            query_type = 0
        if query_type < 0:
            query_type = 9

        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)

        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption=_["play_10"].format(
                title.title(),
                duration_min,
            ),
        )

        await CallbackQuery.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
        await CallbackQuery.answer(_["playcb_2"])

    except Exception:
        pass
