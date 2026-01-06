#!/usr/bin/env python3
"""
Generate dark lonely space themed assets for Kodi addon
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import math
import os

# Space theme color palette
COLORS = {
    'deep_space': (8, 10, 20),
    'dark_nebula': (15, 20, 40),
    'purple_nebula': (40, 20, 60),
    'blue_accent': (30, 80, 140),
    'cyan_glow': (60, 180, 220),
    'star_white': (255, 255, 255),
    'star_blue': (180, 200, 255),
    'star_yellow': (255, 240, 200),
    'nebula_pink': (80, 40, 80),
    'nebula_blue': (20, 40, 80),
    'highlight': (100, 140, 200),
}

def draw_stars(draw, width, height, num_stars=200, seed=None):
    """Draw random stars with varying sizes and brightness"""
    if seed:
        random.seed(seed)
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.choice([1, 1, 1, 1, 2, 2, 3])
        brightness = random.randint(150, 255)
        color_choice = random.choice(['star_white', 'star_blue', 'star_yellow'])
        base_color = COLORS[color_choice]
        color = tuple(min(255, int(c * brightness / 255)) for c in base_color)
        if size == 1:
            draw.point((x, y), fill=color)
        else:
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)

def create_nebula_gradient(img, colors_list):
    """Add nebula-like gradient overlays"""
    width, height = img.size
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for _ in range(3):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        radius = random.randint(min(width, height) // 3, min(width, height))
        color = random.choice(colors_list)
        
        for r in range(radius, 0, -5):
            alpha = int(15 * (1 - r / radius))
            c = (*color[:3], alpha)
            draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c)
    
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def create_fanart(width=1920, height=1080):
    """Create main fanart background - dark lonely space"""
    img = Image.new('RGB', (width, height), COLORS['deep_space'])
    draw = ImageDraw.Draw(img)
    
    # Create gradient from deep space to slightly lighter
    for y in range(height):
        ratio = y / height
        r = int(COLORS['deep_space'][0] + (COLORS['dark_nebula'][0] - COLORS['deep_space'][0]) * ratio * 0.5)
        g = int(COLORS['deep_space'][1] + (COLORS['dark_nebula'][1] - COLORS['deep_space'][1]) * ratio * 0.5)
        b = int(COLORS['deep_space'][2] + (COLORS['dark_nebula'][2] - COLORS['deep_space'][2]) * ratio * 0.5)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add nebula clouds
    img = create_nebula_gradient(img, [COLORS['purple_nebula'], COLORS['nebula_blue'], COLORS['nebula_pink']])
    img = img.convert('RGB')
    
    # Blur for smoother nebula effect
    img = img.filter(ImageFilter.GaussianBlur(radius=30))
    
    # Draw stars
    draw = ImageDraw.Draw(img)
    draw_stars(draw, width, height, num_stars=400, seed=42)
    
    # Add a distant galaxy/nebula glow
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Distant galaxy
    gx, gy = width * 0.7, height * 0.3
    for r in range(200, 0, -2):
        alpha = int(8 * (1 - r / 200))
        overlay_draw.ellipse([gx-r*2, gy-r, gx+r*2, gy+r], fill=(60, 100, 180, alpha))
    
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    return img

def create_icon(size=512):
    """Create main addon icon - planet in space"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Dark space background circle
    margin = 10
    draw.ellipse([margin, margin, size-margin, size-margin], fill=COLORS['deep_space'])
    
    # Draw background stars
    draw_stars(draw, size, size, num_stars=80, seed=123)
    
    # Draw a planet
    planet_cx, planet_cy = size * 0.5, size * 0.55
    planet_r = size * 0.28
    
    # Planet base
    for i in range(int(planet_r), 0, -1):
        ratio = i / planet_r
        r = int(20 + 30 * ratio)
        g = int(40 + 50 * ratio)
        b = int(80 + 60 * ratio)
        draw.ellipse([planet_cx-i, planet_cy-i, planet_cx+i, planet_cy+i], fill=(r, g, b, 255))
    
    # Planet ring
    ring_width = planet_r * 2.2
    ring_height = planet_r * 0.4
    for offset in range(-3, 4):
        alpha = 180 - abs(offset) * 40
        draw.arc([planet_cx-ring_width, planet_cy-ring_height+offset, 
                  planet_cx+ring_width, planet_cy+ring_height+offset],
                 start=160, end=380, fill=(100, 120, 160, alpha), width=2)
    
    # Glow around planet
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for r in range(int(planet_r * 1.5), int(planet_r), -2):
        alpha = int(20 * (1 - (r - planet_r) / (planet_r * 0.5)))
        glow_draw.ellipse([planet_cx-r, planet_cy-r, planet_cx+r, planet_cy+r], 
                         fill=(60, 120, 180, alpha))
    
    img = Image.alpha_composite(glow, img)
    
    # Add subtle outer ring/border
    draw = ImageDraw.Draw(img)
    draw.ellipse([margin+2, margin+2, size-margin-2, size-margin-2], outline=(40, 80, 140, 100), width=3)
    
    return img

def create_menu_icon(name, size=256, icon_type='generic'):
    """Create themed menu icons"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background with space theme
    padding = 8
    
    # Rounded rectangle background
    draw.rounded_rectangle([padding, padding, size-padding, size-padding], 
                          radius=20, fill=(12, 18, 35, 230))
    
    # Add subtle stars
    draw_stars(draw, size, size, num_stars=15, seed=hash(name) % 10000)
    
    # Add glow effect based on icon type
    center = size // 2
    glow_color = COLORS['cyan_glow']
    
    # Draw icon-specific element
    icon_margin = size // 4
    
    if icon_type == 'movies':
        # Film reel shape
        draw.rounded_rectangle([icon_margin, icon_margin, size-icon_margin, size-icon_margin],
                              radius=10, outline=glow_color, width=3)
        # Film holes
        for y in [icon_margin + 15, size - icon_margin - 15]:
            for x in range(icon_margin + 20, size - icon_margin - 10, 25):
                draw.rectangle([x, y-5, x+15, y+5], fill=COLORS['deep_space'])
    
    elif icon_type == 'tv':
        # TV screen shape
        draw.rounded_rectangle([icon_margin, icon_margin+10, size-icon_margin, size-icon_margin-10],
                              radius=8, outline=glow_color, width=3)
        # Antenna
        draw.line([center-20, icon_margin+10, center, icon_margin-15], fill=glow_color, width=2)
        draw.line([center+20, icon_margin+10, center, icon_margin-15], fill=glow_color, width=2)
    
    elif icon_type == 'search':
        # Magnifying glass
        glass_r = size // 5
        draw.ellipse([center-glass_r-10, center-glass_r-20, center+glass_r-10, center+glass_r-20],
                    outline=glow_color, width=4)
        draw.line([center+glass_r-20, center+glass_r-30, center+glass_r+25, center+glass_r+15],
                 fill=glow_color, width=4)
    
    elif icon_type == 'star':
        # Star shape
        points = []
        for i in range(5):
            angle = i * 72 - 90
            r = size // 3
            x = center + r * math.cos(math.radians(angle))
            y = center + r * math.sin(math.radians(angle))
            points.append((x, y))
            angle += 36
            r = size // 6
            x = center + r * math.cos(math.radians(angle))
            y = center + r * math.sin(math.radians(angle))
            points.append((x, y))
        draw.polygon(points, outline=glow_color, width=2)
    
    elif icon_type == 'calendar':
        # Calendar shape
        cal_margin = icon_margin + 5
        draw.rounded_rectangle([cal_margin, cal_margin+15, size-cal_margin, size-cal_margin],
                              radius=5, outline=glow_color, width=2)
        draw.line([cal_margin, cal_margin+40, size-cal_margin, cal_margin+40], fill=glow_color, width=2)
        # Calendar hooks
        for x in [cal_margin + 25, size - cal_margin - 25]:
            draw.line([x, cal_margin+5, x, cal_margin+25], fill=glow_color, width=3)
    
    elif icon_type == 'people':
        # Person silhouette
        head_r = size // 8
        draw.ellipse([center-head_r, icon_margin+10, center+head_r, icon_margin+10+head_r*2],
                    outline=glow_color, width=3)
        # Body
        draw.arc([center-size//4, center-10, center+size//4, size-icon_margin+20],
                start=0, end=180, fill=glow_color, width=3)
    
    elif icon_type == 'gear':
        # Gear/settings
        gear_r = size // 4
        draw.ellipse([center-gear_r, center-gear_r, center+gear_r, center+gear_r],
                    outline=glow_color, width=3)
        # Gear teeth
        for i in range(8):
            angle = i * 45
            x1 = center + gear_r * math.cos(math.radians(angle))
            y1 = center + gear_r * math.sin(math.radians(angle))
            x2 = center + (gear_r + 15) * math.cos(math.radians(angle))
            y2 = center + (gear_r + 15) * math.sin(math.radians(angle))
            draw.line([x1, y1, x2, y2], fill=glow_color, width=4)
    
    elif icon_type == 'download':
        # Download arrow
        arrow_w = size // 6
        draw.line([center, icon_margin+20, center, size-icon_margin-30], fill=glow_color, width=4)
        draw.line([center-arrow_w, size-icon_margin-50, center, size-icon_margin-30], fill=glow_color, width=4)
        draw.line([center+arrow_w, size-icon_margin-50, center, size-icon_margin-30], fill=glow_color, width=4)
        draw.line([icon_margin+20, size-icon_margin-10, size-icon_margin-20, size-icon_margin-10], fill=glow_color, width=3)
    
    elif icon_type == 'trending':
        # Trending up arrow
        draw.line([icon_margin+20, size-icon_margin-30, center, center-10, size-icon_margin-20, icon_margin+40],
                 fill=glow_color, width=4)
        # Arrow head
        draw.line([size-icon_margin-40, icon_margin+30, size-icon_margin-20, icon_margin+40], fill=glow_color, width=4)
        draw.line([size-icon_margin-30, icon_margin+60, size-icon_margin-20, icon_margin+40], fill=glow_color, width=4)
    
    elif icon_type == 'list':
        # List lines
        for i in range(4):
            y = icon_margin + 30 + i * 35
            draw.ellipse([icon_margin+20, y-4, icon_margin+28, y+4], fill=glow_color)
            draw.line([icon_margin+45, y, size-icon_margin-20, y], fill=glow_color, width=2)
    
    elif icon_type == 'folder':
        # Folder shape
        fold_h = size // 3
        draw.polygon([
            (icon_margin+10, center-fold_h//2+15),
            (icon_margin+10 + size//4, center-fold_h//2+15),
            (icon_margin+10 + size//4 + 15, center-fold_h//2),
            (size-icon_margin-10, center-fold_h//2),
            (size-icon_margin-10, center+fold_h//2+10),
            (icon_margin+10, center+fold_h//2+10),
        ], outline=glow_color, width=3)
    
    elif icon_type == 'play':
        # Play triangle
        tri_size = size // 3
        draw.polygon([
            (center - tri_size//2 + 10, center - tri_size),
            (center - tri_size//2 + 10, center + tri_size),
            (center + tri_size, center)
        ], outline=glow_color, width=3)
    
    elif icon_type == 'network':
        # Network/globe
        globe_r = size // 4
        draw.ellipse([center-globe_r, center-globe_r, center+globe_r, center+globe_r],
                    outline=glow_color, width=2)
        draw.arc([center-globe_r//2, center-globe_r, center+globe_r//2, center+globe_r],
                start=0, end=360, fill=glow_color, width=2)
        draw.line([center-globe_r, center, center+globe_r, center], fill=glow_color, width=2)
    
    else:
        # Generic circle with glow
        draw.ellipse([center-30, center-30, center+30, center+30], outline=glow_color, width=3)
        draw.ellipse([center-15, center-15, center+15, center+15], fill=glow_color)
    
    # Add outer glow effect
    glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.rounded_rectangle([padding-2, padding-2, size-padding+2, size-padding+2],
                                radius=22, outline=(60, 180, 220, 60), width=2)
    
    result = Image.alpha_composite(glow_layer, img)
    return result

def create_button_texture(width=256, height=64, variant='normal'):
    """Create button textures"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if variant == 'normal':
        # Dark space button
        draw.rounded_rectangle([2, 2, width-2, height-2], radius=8,
                              fill=(15, 25, 45, 200), outline=(40, 80, 140, 150), width=1)
    elif variant == 'focus':
        # Glowing cyan button
        draw.rounded_rectangle([2, 2, width-2, height-2], radius=8,
                              fill=(20, 40, 70, 220), outline=(60, 180, 220, 255), width=2)
    elif variant == 'selected':
        # Selected state
        draw.rounded_rectangle([2, 2, width-2, height-2], radius=8,
                              fill=(30, 60, 100, 200), outline=(80, 200, 240, 255), width=2)
    
    return img

def create_background_texture(width=64, height=64):
    """Create tileable dark space background"""
    img = Image.new('RGBA', (width, height), COLORS['deep_space'] + (255,))
    draw = ImageDraw.Draw(img)
    draw_stars(draw, width, height, num_stars=5, seed=99)
    return img

def create_gradient_overlay(width=1920, height=100, direction='horizontal'):
    """Create gradient overlay for UI elements"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if direction == 'horizontal':
        for x in range(width):
            alpha = int(180 * (1 - x / width))
            draw.line([(x, 0), (x, height)], fill=(8, 10, 20, alpha))
    else:
        for y in range(height):
            alpha = int(180 * (1 - y / height))
            draw.line([(0, y), (width, y)], fill=(8, 10, 20, alpha))
    
    return img

def create_scrollbar(width=8, height=100):
    """Create scrollbar textures"""
    # Background
    bg = Image.new('RGBA', (width, height), (20, 30, 50, 100))
    
    # Nib/handle
    nib = Image.new('RGBA', (width, height//3), (0, 0, 0, 0))
    nib_draw = ImageDraw.Draw(nib)
    nib_draw.rounded_rectangle([1, 1, width-1, height//3-1], radius=3,
                               fill=(60, 120, 180, 200))
    
    return bg, nib

def main():
    base_path = '/home/ubuntu/kodi/plugin.video.zwpseudo'
    
    print("Generating space theme assets...")
    
    # Create main fanart
    print("Creating fanart...")
    fanart = create_fanart(1920, 1080)
    fanart.save(f'{base_path}/fanart.png', 'PNG')
    fanart.save(f'{base_path}/resources/media/zwpseudo/fanart.jpg', 'JPEG', quality=90)
    fanart.save(f'{base_path}/resources/skins/Default/media/common/fanart.png', 'PNG')
    
    # Create main icon
    print("Creating main icon...")
    icon = create_icon(512)
    icon.save(f'{base_path}/icon.png', 'PNG')
    icon.save(f'{base_path}/resources/media/icon.png', 'PNG')
    icon.save(f'{base_path}/resources/media/zwpseudo/icon.png', 'PNG')
    icon.save(f'{base_path}/resources/media/zwpseudo/poster.png', 'PNG')
    
    # Small icon for skin
    icon_small = icon.resize((256, 256), Image.LANCZOS)
    icon_small.save(f'{base_path}/resources/skins/Default/media/common/icon.png', 'PNG')
    
    # Create menu icons
    print("Creating menu icons...")
    menu_icons = {
        'movies.png': 'movies',
        'tvshows.png': 'tv',
        'search.png': 'search',
        'trending.png': 'trending',
        'most-popular.png': 'star',
        'highly-rated.png': 'star',
        'most-voted.png': 'star',
        'oscar-winners.png': 'star',
        'featured.png': 'star',
        'genres.png': 'folder',
        'years.png': 'calendar',
        'calendar.png': 'calendar',
        'airing-today.png': 'calendar',
        'people.png': 'people',
        'people-search.png': 'people',
        'people-watching.png': 'people',
        'tools.png': 'gear',
        'downloads.png': 'download',
        'networks.png': 'network',
        'channels.png': 'network',
        'languages.png': 'network',
        'certificates.png': 'folder',
        'userlists.png': 'list',
        'trakt.png': 'list',
        'imdb.png': 'star',
        'tmdb.png': 'star',
        'tvdb.png': 'tv',
        'tvmaze.png': 'tv',
        'new-tvshows.png': 'tv',
        'returning-tvshows.png': 'tv',
        'latest-episodes.png': 'tv',
        'latest-movies.png': 'movies',
        'mymovies.png': 'movies',
        'mytvshows.png': 'tv',
        'libmovies.png': 'movies',
        'libtv.png': 'tv',
        'boxsets.png': 'folder',
        'box-office.png': 'movies',
        'in-theaters.png': 'movies',
        'documentaries.png': 'movies',
        'martial-arts.png': 'movies',
        'boxing.png': 'movies',
        'next.png': 'play',
        'premium.png': 'star',
        'youtube.png': 'play',
        'library_update.png': 'download',
        'banner.png': 'generic',
        'collectionboxset.png': 'folder',
        'collectiondisney.png': 'folder',
        'collectionkids.png': 'folder',
        'collectionkidsboxset.png': 'folder',
        'collectionsuperhero.png': 'folder',
        'dc-comics.png': 'folder',
        'marvel-comics.png': 'folder',
        # Debrid services
        'realdebrid.png': 'download',
        'premiumize.png': 'download',
        'alldebrid.png': 'download',
        'easydebrid.png': 'download',
        'easynews.png': 'download',
        'offcloud.png': 'download',
        'torbox.png': 'download',
        'MyAccounts.png': 'gear',
        'fenomscrapers.png': 'gear',
    }
    
    media_path = f'{base_path}/resources/media/zwpseudo'
    for filename, icon_type in menu_icons.items():
        icon_img = create_menu_icon(filename, 256, icon_type)
        icon_img.save(f'{media_path}/{filename}', 'PNG')
    
    # Create skin textures
    print("Creating skin textures...")
    skin_media = f'{base_path}/resources/skins/Default/media/common'
    
    # Buttons
    btn_normal = create_button_texture(256, 64, 'normal')
    btn_normal.save(f'{skin_media}/button.png', 'PNG')
    btn_normal.save(f'{skin_media}/button1.png', 'PNG')
    btn_normal.save(f'{skin_media}/box.png', 'PNG')
    btn_normal.save(f'{skin_media}/box2.png', 'PNG')
    
    btn_focus = create_button_texture(256, 64, 'focus')
    btn_focus.save(f'{skin_media}/button2.png', 'PNG')
    btn_focus.save(f'{skin_media}/button3.png', 'PNG')
    
    btn_selected = create_button_texture(256, 64, 'selected')
    btn_selected.save(f'{skin_media}/button5.png', 'PNG')
    btn_selected.save(f'{skin_media}/selected2.png', 'PNG')
    
    # Background texture
    bg = create_background_texture(64, 64)
    bg.save(f'{skin_media}/bg.png', 'PNG')
    
    # Gradient
    gradient = create_gradient_overlay(256, 64, 'horizontal')
    gradient.save(f'{skin_media}/gradient-diffuse-horizontal.png', 'PNG')
    
    # Shadow
    shadow = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    for i in range(32):
        alpha = int(60 * (1 - i/32))
        shadow_draw.rectangle([i, i, 64-i, 64-i], fill=(0, 0, 0, alpha))
    shadow.save(f'{skin_media}/shadow.png', 'PNG')
    
    # Black/White solid colors
    black = Image.new('RGBA', (32, 32), (8, 10, 20, 255))
    black.save(f'{skin_media}/black.png', 'PNG')
    
    white = Image.new('RGBA', (32, 32), (255, 255, 255, 255))
    white.save(f'{skin_media}/white.png', 'PNG')
    
    # Close button
    close = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    close_draw = ImageDraw.Draw(close)
    close_draw.ellipse([4, 4, 44, 44], fill=(40, 20, 30, 200))
    close_draw.line([14, 14, 34, 34], fill=(200, 100, 100), width=3)
    close_draw.line([34, 14, 14, 34], fill=(200, 100, 100), width=3)
    close.save(f'{skin_media}/close.png', 'PNG')
    
    # Play button
    play = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    play_draw = ImageDraw.Draw(play)
    play_draw.ellipse([4, 4, 60, 60], fill=(20, 40, 60, 200))
    play_draw.polygon([(24, 18), (24, 46), (48, 32)], fill=COLORS['cyan_glow'])
    play.save(f'{skin_media}/play.png', 'PNG')
    
    # Stop button
    stop = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    stop_draw = ImageDraw.Draw(stop)
    stop_draw.ellipse([4, 4, 60, 60], fill=(20, 40, 60, 200))
    stop_draw.rectangle([20, 20, 44, 44], fill=COLORS['cyan_glow'])
    stop.save(f'{skin_media}/stop.png', 'PNG')
    
    # Star
    star = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    star_draw = ImageDraw.Draw(star)
    points = []
    cx, cy = 32, 32
    for i in range(5):
        angle = i * 72 - 90
        x = cx + 26 * math.cos(math.radians(angle))
        y = cy + 26 * math.sin(math.radians(angle))
        points.append((x, y))
        angle += 36
        x = cx + 12 * math.cos(math.radians(angle))
        y = cy + 12 * math.sin(math.radians(angle))
        points.append((x, y))
    star_draw.polygon(points, fill=(255, 200, 100))
    star.save(f'{skin_media}/star.png', 'PNG')
    
    # Scrollbar textures
    print("Creating scrollbar textures...")
    scrollbar_path = f'{base_path}/resources/skins/Default/media/scrollbars'
    
    scroll_bg = Image.new('RGBA', (12, 100), (15, 25, 45, 150))
    scroll_bg.save(f'{scrollbar_path}/scrollbaruni-bg.png', 'PNG')
    
    scroll_bar = Image.new('RGBA', (8, 50), (0, 0, 0, 0))
    scroll_draw = ImageDraw.Draw(scroll_bar)
    scroll_draw.rounded_rectangle([1, 1, 7, 49], radius=3, fill=(50, 100, 150, 200))
    scroll_bar.save(f'{scrollbar_path}/scrollbaruni-bar.png', 'PNG')
    
    scroll_bar_focus = Image.new('RGBA', (8, 50), (0, 0, 0, 0))
    scroll_focus_draw = ImageDraw.Draw(scroll_bar_focus)
    scroll_focus_draw.rounded_rectangle([1, 1, 7, 49], radius=3, fill=(60, 180, 220, 255))
    scroll_bar_focus.save(f'{scrollbar_path}/scrollbaruni-bar-focus.png', 'PNG')
    
    scroll_nib = Image.new('RGBA', (12, 20), (0, 0, 0, 0))
    nib_draw = ImageDraw.Draw(scroll_nib)
    nib_draw.rounded_rectangle([2, 2, 10, 18], radius=4, fill=(60, 140, 200, 255))
    scroll_nib.save(f'{scrollbar_path}/scrollbaruni-nib.png', 'PNG')
    
    print("Space theme assets generated successfully!")

if __name__ == '__main__':
    main()
