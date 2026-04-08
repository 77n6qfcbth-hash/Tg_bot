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
            f"🕐 {event.begin.strftime('%H:%M')} - {event.end.strftime('%H:%M')}\n"
            f"📘 {event.name}\n"
            f"📍 {event.location}\n"
            f"👨‍🏫 {event.description}\n\n"
        )

    return text

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