import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
from asBASE import asJSON

load_dotenv()


db = asJSON("as.json")




# ▂▂▂▂▂ Basic Bot Configuration ▂▂▂▂▂ #
API_ID = int(getenv("API_ID", '8186557'))
API_HASH = getenv("API_HASH","efd77b34c69c164ce158037ff5a0d117")
BOT_TOKEN = getenv("BOT_TOKEN")




OWNER_ID = int(getenv("OWNER_ID", 7654641648))
OWNER_USERNAME = getenv("OWNER_USERNAME")
BOT_USERNAME = getenv("ID")
BOT_NAME = getenv("BOT_NAME", "˹ᴛᴜɴᴇ ᴠɪᴀ ʙᴏᴛ˼")
ASSUSERNAME = getenv("ASSUSERNAME", "")
EVALOP = list(map(int, getenv("EVALOP", "6797202080").split()))





# ▂▂▂▂▂ Mongo & Logging ▂▂▂▂▂ #
MONGO_DB_URI = getenv("MONGO_DB_URI","mongodb+srv://kuldiprathod2003:kuldiprathod2003@cluster0.wxqpikp.mongodb.net/?retryWrites=true&w=majority")
LOGGER_ID = int(getenv("OWNER_ID"))


SET_CMDS = getenv("SET_CMDS", "True")




# ▂▂▂▂▂ Limits and Durations ▂▂▂▂▂ #
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 7500))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "2147483648"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "10200"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "2147483648"))  # 2 GB
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "2147483648"))  # 2 GB



# ▂▂▂▂▂ Custom API Configs ▂▂▂▂▂ #
COOKIE_URL = getenv("COOKIE_URL") #necessary
API_URL = getenv("API_URL","0aa99a_Z-zb8j1TeybrOTKSndlOM24Wxkam_K2Q") #optional
API_KEY = getenv("API_KEY") #optional




# ▂▂▂▂▂ Heroku Configuration ▂▂▂▂▂ #
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")




# ▂▂▂▂▂ Git & Updates ▂▂▂▂▂ #
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/CertifiedCoders/TuneViaBot")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "Master")
GIT_TOKEN = getenv("GIT_TOKEN")



# ▂▂▂▂▂ Support & Community ▂▂▂▂▂ #
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/updatevega")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Breakvega")




# ▂▂▂▂▂ Assistant Auto Leave ▂▂▂▂▂ #
AUTO_LEAVING_ASSISTANT = False
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "11500"))




# ▂▂▂▂▂ Spotify Credentials ▂▂▂▂▂ #
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "22b6125bfe224587b722d6815002db2b")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "c9c63c6fbf2f467c8bc68624851e9773")



# ▂▂▂▂▂ Session Strings ▂▂▂▂▂ #
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")



# ▂▂▂▂▂ Server Settings ▂▂▂▂▂ #
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "3000"))
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "2500"))



# ▂▂▂▂▂ Bot Media Assets ▂▂▂▂▂ #
START_VIDS = [
    "https://graph.org/file/490756122766c26b39ab7.mp4",
]




STICKERS = [
    "CAACAgQAAxkBAAIQMGgcpHHxeS56sRIRT_MIkhPa0UbMAALlCAACBLdoUptLHUJBk0XYHgQ",
    "CAACAgQAAxkBAAIQNmgcpJLeCD15jDTeOXrFpl5NmU7_AAJoFQACOwK5UDnwcejEfZ0hHgQ",
    "CAACAgQAAyEFAASb7_CbAAJXmWgXogmvwvx-g12Yt1Wmu5egrvS9AAJoFQACOwK5UDnwcejEfZ0hHgQ",
    "CAACAgQAAyEFAASb7_CbAAJXnGgXok3kMrv4wg1jbKMM4Qs85ktxAALlCAACBLdoUptLHUJBk0XYHgQ",
    "CAACAgQAAyEFAASb7_CbAAJXomgXomkPDdpEQqma_XIyCu4ctNXkAAJPDwACzFOYU73VM05xhJEJHgQ"
]



HELP_VID_URL = "https://graph.org/file/490756122766c26b39ab7.mp4"
PING_VID_URL = "https://graph.org/file/490756122766c26b39ab7.mp4"
PLAYLIST_VIDS_URL = "https://files.catbox.moe/uiuwse.mp4"
STATS_VID_URL = "https://graph.org/file/490756122766c26b39ab7.mp4"

TELEGRAM_AUDIO_URL = "https://files.catbox.moe/90juvd.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/7qplwr.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/d2jndi.jpg"
FAILED = "https://files.catbox.moe/d2jndi.jpg"


# ▂▂▂▂▂ Utility & Functional ▂▂▂▂▂ #
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

LOG = 2

# ▂▂▂▂▂ Bot Introduction Messages ▂▂▂▂▂ #
AYU = ["🦋","⚡️", "🔥"]


# ▂▂▂▂▂ Runtime Structures ▂▂▂▂▂ #
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ▂▂▂▂▂ URL Validation ▂▂▂▂▂ #
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")



bot_id = BOT_TOKEN.split(":")[0]