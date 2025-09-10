from VeGa.core.bot import KIM
from VeGa.core.dir import dirr
from pyromod import listen
from VeGa.core.userbot import Userbot
from VeGa.misc import dbb, heroku
from VeGa.logging import LOGGER

dirr()
dbb()
heroku()

app = KIM()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
