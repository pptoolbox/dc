from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta
import calendar

# ======================
# CONFIG
# ======================
WIDTH, HEIGHT = 3840, 2160  # 4K
BG_COLOR = (245, 245, 245)

MONTH_BG = (225, 225, 225)
PAST_COLOR = (150, 150, 150)
OUTSIDE_MONTH_COLOR = (200, 200, 200)
FUTURE_COLOR = (20, 20, 20)

TODAY_BG = (0, 100, 255)
TODAY_TEXT = (255, 255, 255)
MONTH_TEXT = (55, 55, 55)

PADDING_X = 100
PADDING_Y = 100
MONTH_RADIUS = 30

CELL_SIZE_X = 117
CELL_SIZE_Y = 65
CELL_GAP_X = 10   # horizontal spacing between dates
CELL_GAP_Y = 15   # vertical spacing between weeks
DAY_RADIUS = 12

FONT_PATH = "/opt/dc/DMMono-Medium.ttf"

OUTPUT_FILE = "/usr/local/share/wallpapers/dc-light.png"

# ======================
# SETUP
# ======================
today = date.today()
year = today.year
cal = calendar.Calendar(firstweekday=0)  # Monday start

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_day = ImageFont.truetype(FONT_PATH, 45)
    font_month = ImageFont.truetype(FONT_PATH, 33)
except:
    font_day = ImageFont.load_default()
    font_month = ImageFont.load_default()

# ======================
# LAYOUT
# ======================
months_per_row = 4
rows = 3

month_width = (WIDTH - 2 * PADDING_X) // months_per_row
month_height = (HEIGHT - 2 * PADDING_Y) // rows

panel_pad = 28
title_height = 64

# ======================
# DRAW MONTHS
# ======================
for month in range(1, 13):
    row = (month - 1) // months_per_row
    col = (month - 1) % months_per_row

    ox = PADDING_X + col * month_width
    oy = PADDING_Y + row * month_height

    # Month panel background
    draw.rounded_rectangle(
        [
            ox,
            oy,
            ox + month_width - 20,
            oy + month_height - 20
        ],
        radius=MONTH_RADIUS,
        fill=MONTH_BG
    )

    # Month title
    draw.text(
        (ox + panel_pad, oy + panel_pad),
        calendar.month_name[month].upper(),
        fill=MONTH_TEXT,
        font=font_month
    )

    grid_x = ox + panel_pad
    grid_y = oy + panel_pad + title_height

    weeks = cal.monthdatescalendar(year, month)

    # Ensure exactly 6 weeks
    while len(weeks) < 6:
        last_week = weeks[-1]
        next_week = [d + timedelta(days=7) for d in last_week]
        weeks.append(next_week)

    for week_idx, week in enumerate(weeks[:6]):
        for day_idx, d in enumerate(week):
            x = grid_x + day_idx * (CELL_SIZE_X + CELL_GAP_X)
            y = grid_y + week_idx * (CELL_SIZE_Y + CELL_GAP_Y)

            # TODAY
            if d == today and d.month == month:
                draw.rounded_rectangle(
                    [x -5 , y, x + 69, y + CELL_SIZE_Y],
                    radius=DAY_RADIUS,
                    fill=TODAY_BG
                )
                draw.text(
                    (x + 6, y + 6),
                    f"{d.day:02d}",
                    fill=TODAY_TEXT,
                    font=font_day
                )
                continue

            # Color logic
            if d.month != month:
                color = OUTSIDE_MONTH_COLOR
            else:
                color = PAST_COLOR if d < today else FUTURE_COLOR

            draw.text(
                (x + 8, y + 6),
                f"{d.day:02d}",
                fill=color,
                font=font_day
            )

# ======================
# SAVE
# ======================
img.save(OUTPUT_FILE)
print(f"Wallpaper generated: {OUTPUT_FILE}")
