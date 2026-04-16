from ics import Calendar
import datetime
import os
calendar = None
def load_schedule():
    global calendar
    if calendar is None:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "781000741.ics")

        with open(file_path, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())

    return calendar

def get_events_by_date(date):
    cal = load_schedule()
    return sorted(
        event for event in cal.events
        if event.begin.date() == date
    )
    
def format_events(events, title=""):
    if not events:
        return f"{title}\nНет пар 🎉"

    text = f"{title}\n\n"

    for event in events:
        text += (
            f"🕐 {event.begin.to('Europe/Samara').strftime('%H:%M')} - {event.end.to('Europe/Samara').strftime('%H:%M')}\n"
            f"📘 {event.name}\n"
            f"📍 {event.location}\n"
            f"👨‍🏫 {event.description}\n\n"
        )

    return text

def parse_location(location: str):
    if not location:
        return "other", "—"

    parts = location.split("/")

    type_part = parts[0].strip().lower()
    place_part = parts[1].strip() if len(parts) > 1 else "—"

    if "лек" in type_part:
        event_type = "lecture"
    elif "лаб" in type_part:
        event_type = "lab"
    elif "прак" in type_part:
        event_type = "practice"
    else:
        event_type = "other"

    return event_type, place_part


COLOR_MAP = {
    "lecture": "#4CAF50",
    "practice": "#FF9800",
    "lab": "#2196F3",
    "other": "#999999"
}

def get_next_days(n=7):
    today = datetime.date.today()
    return (today + datetime.timedelta(days=i) for i in range(n))


def format_day(day):
    return format_events(
        get_events_by_date(day),
        f"📆 {day.strftime('%A (%d.%m)')}"
    )

def get_week():
    return "📅 Расписание на неделю\n\n" + "\n".join(
        format_day(day) for day in get_next_days()
    )
def get_today():
    today = datetime.date.today()
    return format_day(today)