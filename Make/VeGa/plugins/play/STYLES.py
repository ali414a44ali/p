import random
import re
from pyrogram import filters, Client
from pyrogram import Client
from pyrogram.types import Message
from VeGa import app
#from pyrogram import Client, filters
from pyrogram.types import Message
import random
import re
from pyrogram import filters, Client
from pyrogram import Client
from pyrogram.types import Message
from VeGa import app
import random
import re
import time
from pyrogram import filters, Client
from pyrogram.types import Message
from VeGa import app
import random
import re
from pyrogram import filters, Client
from pyrogram.types import Message
from VeGa import app





# قائمة أنماط الزخرفة العربية
english_styles = {
    "1": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",  # Fraktur
    "2": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",  # Bold Fraktur
    "3": "𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",  # Script
    "4": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",  # Bold Script
    "5": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",  # Double-struck
    "6": "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",  # Sans-serif
    "7": "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",  # Sans-serif bold
    "8": "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",  # Sans-serif italic
    "9": "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",  # Sans-serif bold italic
    "10": "𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",  # Monospace
    "11": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",  # Squared
    "12": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",  # Negative squared
    "13": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",  # Bold
    "14": "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍",  # Italic
    "15": "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",  # Bold italic
    "16": "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",  # Script
    "17": "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",  # Bold script
    "18": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",  # Blackboard bold
    "19": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",  # Bold Fraktur
    "20": "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",  # Sans-serif
    "21": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",  # Fullwidth
    "22": "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",  # Negative circled
    "23": "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",  # Fraktur alternate
    "24": "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ",  # Small caps
    "25": "₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ",  # Currency style
    "26": "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ",  # Block letters
    "27": "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙",  # Asian style
    "28": "ค๒ς๔єŦﻮђเןкɭ๓ภ๏קợгรՇยשฬאץչ",  # Thai style
    "29": "ꍏ♭☾ᕲ€Ϝ❡♄♗♪ϰ↳ᗰ♫⊙ρ☭☈ⓢ☂☋✓Ꮤ⌘⚧☡",  # Symbolic
    "30": "ǟɮƈɖɛʄɢɦɨʝӄʟʍռօքզʀֆȶʊʋաӼʏʐ",  # Cursive
    "31": "αႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ",  # Greek inspired
    "32": "ᏗᏰፈᎴᏋᎦᎶᏂᎥᏠᏦᏝᎷᏁᎧᎮᎤᏒᏕᏖᏬᏉᏇጀᎩፚ",  # Cherokee inspired
    "33": "ค๖¢໓ēfງhiวkl๓ຖ໐p๑rŞtนงຟxฯຊ",  # Lao inspired
    "34": "ꁲꌃꏳꂟꑾꊰꁅꑛꂑ꒻ꀗ꒒ꂵꋊꆂꉣꁸꋪꌚ꓅ꐇꏝꅏꇓꐔꑒ",  # Yi syllables
    "35": "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉",  # Squared uppercase
    "36": "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",  # Negative squared uppercase
    "37": "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",  # Bold uppercase
    "38": "𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛",  # Bold script lowercase
    "39": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",  # Double-struck lowercase
    "40": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"  # Bold Fraktur lowercase
}

def zakhrafa_text(text, style):
    """تزيين النص بأسلوب معين"""
    result = []
    char_map = {}
    
    # إنشاء خريطة للأحرف الكبيرة
    for i in range(26):
        char = chr(ord('A') + i)
        if i < len(style):
            char_map[char] = style[i]
        else:
            char_map[char] = char
    
    # إنشاء خريطة للأحرف الصغيرة
    for i in range(26):
        char = chr(ord('a') + i)
        if i < len(style):
            # استخدام الأحرف الصغيرة المقابلة إن وجدت، وإلا استخدام الأحرف الكبيرة
            lower_char = style[i].lower() if style[i].lower() != style[i] else style[i]
            char_map[char] = lower_char
        else:
            char_map[char] = char
    
    # تحويل النص المدخل
    for char in text:
        if char in char_map:
            result.append(char_map[char])
        else:
            result.append(char)
    
    return ''.join(result)

@app.on_message(filters.command(["زخرفه", "زغرفه", "زخرفة"], ""), group=4241)
async def decorate_command(client: Client, message: Message):
    # التحقق من وجود مرسل
    if not message.from_user:
        return
    
    # الحصول على هوية المستخدم الذي أرسل الأمر
    user_id = message.from_user.id
    
    # معالجة النص المدخل
    if len(message.command) < 2:
        if message.reply_to_message:
            # إذا كان الأمر رداً على رسالة
            text = message.reply_to_message.text or message.reply_to_message.caption or ""
        else:
            # طلب النص من المستخدم
            ask = await message.reply_text("⌔︙ أرسل الكلمة أو الجملة التي تريد زخرفتها")
            try:
                # الانتظار للرد من نفس المستخدم فقط
                text_msg = await client.listen(
                    chat_id=message.chat.id,
                    filters=filters.text & filters.user(user_id),
                    timeout=300
                )
                text = text_msg.text
                await ask.delete()
            except TimeoutError:
                await ask.edit_text("⌔︙ انتهى وقت الانتظار")
                return
    else:
        text = ' '.join(message.command[1:])
    
    # التحقق من وجود نص لزخرفته
    if not text:
        await message.reply_text("⌔︙ لم يتم تقديم نص لزخرفته")
        return
    
    # إنشاء النصوص المزخرفة
    reply_text = f"🔮 • النص الأصلي: {text}\n\n"
    reply_text += "✨ • النسخ المزخرفة:\n\n"
    
    for style_name, style_chars in english_styles.items():
        decorated = zakhrafa_text(text, style_chars)
        reply_text += f"**• النمط {style_name}**: `{decorated}`\n"
    
    await message.reply_text(reply_text)