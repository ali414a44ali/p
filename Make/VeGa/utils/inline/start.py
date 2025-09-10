from pyrogram.types import InlineKeyboardButton
import config
from VeGa import app


def start_panel(_):
    return [[InlineKeyboardButton(text=_["S_B_4"], url=config.SUPPORT_CHANNEL)]]


def private_panel(_):
    return [
        [
            InlineKeyboardButton(text=_["S_B_7"], user_id=config.OWNER_ID),
            
        ],
    ]
