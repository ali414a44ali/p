import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import FAILED

# Constants
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

PANEL_W, PANEL_H = 763, 545
PANEL_X = (1280 - PANEL_W) // 2
PANEL_Y = 88
TRANSPARENCY = 170
INNER_OFFSET = 36

# Thumbnail settings
THUMB_SIZE = 280
THUMB_X = PANEL_X + (PANEL_W - THUMB_SIZE) // 2
THUMB_Y = PANEL_Y + INNER_OFFSET + 20

# Title settings
TITLE_X = PANEL_X + (PANEL_W - 500) // 2
TITLE_Y = THUMB_Y + THUMB_SIZE + 20

# Progress bar settings
BAR_TOTAL_LEN = 480
BAR_RED_LEN = 280

# Metadata and progress bar positioning
META_Y = TITLE_Y + 45
BAR_X = PANEL_X + (PANEL_W - BAR_TOTAL_LEN) // 2
BAR_Y = META_Y + 30
META_X = BAR_X  # Aligned with progress bar start

# Icons settings - now matching progress bar width
ICONS_W = BAR_TOTAL_LEN  # Same width as progress bar
ICONS_H = 62
ICONS_X = BAR_X  # Aligned with progress bar start
ICONS_Y = BAR_Y + 30  # 30px below progress bar

MAX_TITLE_WIDTH = 500

def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text) - 1, 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis

async def get_thumb(videoid: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_v4.png")
    if os.path.exists(cache_path):
        return cache_path

    # YouTube video data fetch
    results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    try:
        results_data = await results.next()
        result_items = results_data.get("result", [])
        if not result_items:
            raise ValueError("No results found.")
        data = result_items[0]
        thumbnail = data.get("thumbnails", [{}])[0].get("url", FAILED)
        duration = data.get("duration")
        views = data.get("viewCount", {}).get("short", "Unknown Views")
    except Exception:
        thumbnail, duration, views = FAILED, None, "Unknown Views"

    is_live = not duration or str(duration).strip().lower() in {"", "live", "live now"}
    duration_text = "Live" if is_live else duration or "Unknown Mins"

    # Download thumbnail
    thumb_path = os.path.join(CACHE_DIR, f"thumb{videoid}.png")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
    except Exception:
        return FAILED

    # Create base image
    base = Image.open(thumb_path).resize((1280, 720)).convert("RGBA")
    bg = ImageEnhance.Brightness(base.filter(ImageFilter.BoxBlur(10))).enhance(0.6)

    # Frosted glass panel
    panel_area = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
    overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
    frosted = Image.alpha_composite(panel_area, overlay)
    mask = Image.new("L", (PANEL_W, PANEL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)
    bg.paste(frosted, (PANEL_X, PANEL_Y), mask)

    # Draw details
    draw = ImageDraw.Draw(bg)
    try:
        title_font = ImageFont.truetype("VeGa/assets/thumb/font2.ttf", 42)
        regular_font = ImageFont.truetype("VeGa/assets/thumb/font.ttf", 18)
    except OSError:
        title_font = regular_font = ImageFont.load_default()
        title_font.size = 42

    # Create circular thumbnail
    thumb = base.resize((THUMB_SIZE, THUMB_SIZE))
    
    # Create mask for circular thumbnail
    mask = Image.new("L", (THUMB_SIZE, THUMB_SIZE), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, THUMB_SIZE, THUMB_SIZE), fill=255)
    
    # Paste circular thumbnail
    bg.paste(thumb, (THUMB_X, THUMB_Y), mask)

    # Draw white borders around the image
    border_width = 3
    border_padding = 20
    corner_size = 30
    
    # Top border
    draw.line([(border_padding, border_padding), 
              (bg.width - border_padding, border_padding)], 
              fill="white", width=border_width)
    
    # Left border
    draw.line([(border_padding, border_padding), 
              (border_padding, bg.height - border_padding)], 
              fill="white", width=border_width)
    
    # Bottom border
    draw.line([(border_padding, bg.height - border_padding), 
              (bg.width - border_padding, bg.height - border_padding)], 
              fill="white", width=border_width)
    
    # Right border
    draw.line([(bg.width - border_padding, border_padding), 
              (bg.width - border_padding, bg.height - border_padding)], 
              fill="white", width=border_width)
    
    # Corners
    # Top-left corner
    draw.line([(border_padding, border_padding + corner_size), 
              (border_padding + corner_size, border_padding)], 
              fill="white", width=border_width)
    
    # Top-right corner
    draw.line([(bg.width - border_padding - corner_size, border_padding), 
              (bg.width - border_padding, border_padding + corner_size)], 
              fill="white", width=border_width)
    
    # Bottom-left corner
    draw.line([(border_padding, bg.height - border_padding - corner_size), 
              (border_padding + corner_size, bg.height - border_padding)], 
              fill="white", width=border_width)
    
    # Bottom-right corner
    draw.line([(bg.width - border_padding - corner_size, bg.height - border_padding), 
              (bg.width - border_padding, bg.height - border_padding - corner_size)], 
              fill="white", width=border_width)

    # Draw VEGA MUSIC as main title (centered)
    vega_title = "VEGA | MUSIC"
    title_width = title_font.getlength(vega_title)
    title_x = PANEL_X + (PANEL_W - title_width) // 2
    draw.text((title_x, TITLE_Y), vega_title, fill="black", font=title_font)

    # Metadata - aligned with progress bar start
    draw.text((META_X, META_Y), f"YouTube | {views}", fill="black", font=regular_font)

    # Progress bar
    draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
    draw.line([(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)], fill="gray", width=5)
    draw.ellipse([(BAR_X + BAR_RED_LEN - 7, BAR_Y - 7), (BAR_X + BAR_RED_LEN + 7, BAR_Y + 7)], fill="red")

    draw.text((BAR_X, BAR_Y + 15), "00:00", fill="black", font=regular_font)
    end_text = "Live" if is_live else duration_text
    draw.text((BAR_X + BAR_TOTAL_LEN - (90 if is_live else 60), BAR_Y + 15), end_text, fill="red" if is_live else "black", font=regular_font)

    
    icons_path = "VeGa/assets/play_icons.png"
    if os.path.isfile(icons_path):
        play_icons = Image.open(icons_path).resize((ICONS_W, ICONS_H)).convert("RGBA")
        bg.paste(play_icons, (ICONS_X, ICONS_Y), play_icons)
    
    try:
        os.remove(thumb_path)
    except OSError:
        pass

    bg.save(cache_path)
    return cache_path