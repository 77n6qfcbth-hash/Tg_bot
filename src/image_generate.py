import os

from PIL import Image, ImageDraw, ImageFont
from shedule import get_next_days, get_events_by_date
import io

WIDTH = 900
HEIGHT = 1800
PADDING = 20

BG_COLOR = "#f5f7fb"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#1e1e1e"

TYPE_COLORS = {
    "📗": "#4CAF50",  # лекция
    "📕": "#FF9800",  # практика
    "📘": "#2196F3",  # лаба
}


base_dir = os.path.dirname(__file__)
font_path = os.path.join(base_dir, "fonts", "DejaVuSans.ttf")

font_title = ImageFont.truetype(font_path, 40)
font_day = ImageFont.truetype(font_path, 26)
font_text = ImageFont.truetype(font_path, 22)


def draw_card(draw, x, y, w, h, color):
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=20,
        fill=color
    )


def generate_week_image():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = PADDING

    # заголовок
    draw.text((PADDING, y), "📅 Расписание на неделю", font=font_title, fill=TEXT_COLOR)
    y += 60

    for day in get_next_days():
        events = get_events_by_date(day)

        # день
        day_str = day.strftime("%d.%m (%A)")
        draw.text((PADDING, y), f"📆 {day_str}", font=font_day, fill=TEXT_COLOR)
        y += 35

        if not events:
            draw.text((PADDING + 10, y), "Нет пар 🎉", font=font_text, fill="gray")
            y += 40
            continue

        for event in events:
            card_height = 90

            # цвет по типу
            emoji = event.name.strip()[0]
            color = TYPE_COLORS.get(emoji, "#999999")

            # карточка
            draw_card(draw, PADDING, y, WIDTH - 2 * PADDING, card_height, CARD_COLOR)

            # цветная полоска
            draw.rectangle(
                (PADDING, y, PADDING + 10, y + card_height),
                fill=color
            )

            # время
            draw.text(
                (PADDING + 20, y + 10),
                f"{event.begin.to('Europe/Samara').strftime('%H:%M')} - {event.end.to('Europe/Samara').strftime('%H:%M')}",
                font=font_text,
                fill=TEXT_COLOR
            )

            # предмет
            draw.text(
                (PADDING + 20, y + 40),
                event.name[:40],
                font=font_text,
                fill=TEXT_COLOR
            )

            y += card_height + 10

        y += 10


    bio = io.BytesIO()
    bio.name = "week.png"  # важно!
    img.save(bio, "PNG")
    bio.seek(0)

    return bio