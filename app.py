import os
from flask import Flask, render_template
import requests
from ics import Calendar
from datetime import datetime, timedelta
import pytz


app = Flask(__name__)

def get_ics_data(url: str) -> str | None:
    try:
        r = requests.get(url)
        r.raise_for_status()

        return Calendar(r.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def get_current_class(calendar: Calendar, delta: int) -> str | None:
    now = datetime.now(pytz.utc)
    for event in calendar.timeline.now():
            event.begin = event.begin + timedelta(hours=delta)
            event.end = event.end + timedelta(hours=delta)
            return event
    return None


def get_next_class(calendar: Calendar, delta: int) -> str | None:
    now = datetime.now(pytz.utc)
    for event in calendar.timeline.start_after(now):
        event.begin = event.begin + timedelta(hours=delta)
        event.end = event.end + timedelta(hours=delta)
        return event
    return None


@app.route('/')
def classes_info():
    ade_url = os.getenv('ADE_URL')
    delta = 1 if os.getenv('WINTER_HOUR') == "True" else 2

    calendar = get_ics_data(ade_url)
    if not calendar:
        return "<p>Error fetching data<p>"

    current_event = get_current_class(calendar, delta)
    next_event = get_next_class(calendar, delta)

    if current_event:
        current_info = current_event
    else:
        current_info = None

    if next_event:
        next_info = next_event
    else:
        next_info = None

    return render_template('index.html', current=current_info, next=next_info)
