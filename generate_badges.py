#!/usr/bin/env python3
"""
Generate space-themed resolution and audio badge icons for Kodi addon
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Space theme colors
COLORS = {
    'bg_dark': (12, 18, 35),
    'bg_medium': (20, 30, 55),
    'cyan_glow': (60, 180, 220),
    'blue_accent': (30, 100, 180),
    'purple_accent': (100, 60, 160),
    'text_white': (240, 245, 255),
    'gold': (255, 200, 100),
}

def create_badge(text, width=100, height=40, color_scheme='cyan'):
    """Create a space-themed badge with text"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Choose color based on scheme
    if color_scheme == 'cyan':
        border_color = COLORS['cyan_glow']
        bg_color = (*COLORS['bg_dark'], 220)
    elif color_scheme == 'purple':
        border_color = COLORS['purple_accent']
        bg_color = (*COLORS['bg_dark'], 220)
    elif color_scheme == 'gold':
        border_color = COLORS['gold']
        bg_color = (*COLORS['bg_dark'], 220)
    else:
        border_color = COLORS['blue_accent']
        bg_color = (*COLORS['bg_dark'], 220)
    
    # Draw rounded rectangle background
    draw.rounded_rectangle([2, 2, width-2, height-2], radius=6, fill=bg_color, outline=border_color, width=2)
    
    # Draw text centered
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 2
    
    draw.text((x, y), text, fill=COLORS['text_white'], font=font)
    
    return img

def create_quality_badge(quality, size=100):
    """Create quality/resolution badge"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle
    draw.ellipse([5, 5, size-5, size-5], fill=(*COLORS['bg_dark'], 230), outline=COLORS['cyan_glow'], width=3)
    
    # Quality text
    try:
        if len(quality) <= 3:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        else:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), quality, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 2
    
    draw.text((x, y), quality, fill=COLORS['cyan_glow'], font=font)
    
    return img

def create_format_badge(text, width=100, height=50):
    """Create format/codec badge"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Rounded rectangle
    draw.rounded_rectangle([2, 2, width-2, height-2], radius=8, 
                          fill=(*COLORS['bg_medium'], 220), 
                          outline=COLORS['cyan_glow'], width=2)
    
    try:
        font_size = 14 if len(text) > 6 else 18
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 2
    
    draw.text((x, y), text, fill=COLORS['text_white'], font=font)
    
    return img

def main():
    base_path = '/home/ubuntu/kodi/plugin.video.zwpseudo/resources/skins/Default/media'
    
    print("Generating space-themed badges...")
    
    # Resolution badges
    resolution_path = f'{base_path}/resolution'
    os.makedirs(resolution_path, exist_ok=True)
    
    resolutions = {
        '4k.png': '4K',
        '1080p.png': '1080p',
        '1080p_orig.png': '1080p',
        '720p.png': '720p',
        'sd.png': 'SD',
        'CAM.png': 'CAM',
        'scr.png': 'SCR',
    }
    
    for filename, text in resolutions.items():
        badge = create_quality_badge(text)
        badge.save(f'{resolution_path}/{filename}', 'PNG')
    
    # Source/codec badges
    source_path = f'{base_path}/source'
    os.makedirs(source_path, exist_ok=True)
    
    sources = {
        '3d.png': '3D',
        'avi.png': 'AVI',
        'bluray.png': 'BLURAY',
        'bluray2.png': 'BLURAY',
        'divx.png': 'DIVX',
        'dv.png': 'DV',
        'dvd.png': 'DVD',
        'dx50.png': 'DX50',
        'h264.png': 'H.264',
        'hdr.png': 'HDR',
        'hdr2.png': 'HDR',
        'hdr3.png': 'HDR10+',
        'hdtv.png': 'HDTV',
        'hevc.png': 'HEVC',
        'm2ts.PNG': 'M2TS',
        'mkv.png': 'MKV',
        'mkv2.png': 'MKV',
        'mpeg_video.png': 'MPEG',
        'web-dl.png': 'WEB-DL',
        'web-dl2.png': 'WEB-DL',
        'wmv2.png': 'WMV',
        'x264.png': 'x264',
        'xvid.png': 'XVID',
        'xvid2.png': 'XVID',
    }
    
    for filename, text in sources.items():
        badge = create_format_badge(text)
        badge.save(f'{source_path}/{filename}', 'PNG')
    
    # Audio badges
    audio_path = f'{base_path}/audio'
    os.makedirs(audio_path, exist_ok=True)
    
    audio_formats = {
        'aac.png': 'AAC',
        'atmos.png': 'ATMOS',
        'dolbydigital.png': 'DD',
        'dolbydigital_ex.jpg': 'DD-EX',
        'dolbytruehd.png': 'TRUEHD',
        'dts.png': 'DTS',
        'dts2.png': 'DTS',
        'dtshd_ma.png': 'DTS-HD',
        'dtsx.png': 'DTS:X',
        'dts_x.png': 'DTS:X',
        'eac3.png': 'EAC3',
        'flac.png': 'FLAC',
        'mp3.png': 'MP3',
        'multi_lingual.png': 'MULTI',
        'opus.png': 'OPUS',
        'truehd.png': 'TRUEHD',
        'wmav2.png': 'WMA',
    }
    
    for filename, text in audio_formats.items():
        badge = create_format_badge(text)
        # Handle both PNG and JPG
        if filename.endswith('.jpg'):
            badge = badge.convert('RGB')
            badge.save(f'{audio_path}/{filename}', 'JPEG', quality=95)
        else:
            badge.save(f'{audio_path}/{filename}', 'PNG')
    
    # Channel badges
    channels_path = f'{base_path}/channels'
    os.makedirs(channels_path, exist_ok=True)
    
    channels = {
        '2.png': '2.0',
        '6.png': '5.1',
        '7.png': '6.1',
        '8.png': '7.1',
        '10.png': '7.1.4',
    }
    
    for filename, text in channels.items():
        badge = create_format_badge(text, width=80, height=45)
        badge.save(f'{channels_path}/{filename}', 'PNG')
    
    print("Space-themed badges generated successfully!")

if __name__ == '__main__':
    main()
