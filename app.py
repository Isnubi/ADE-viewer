import os
from flask import Flask, render_template
import requests
from ics import Calendar as ics_Calendar
from datetime import datetime, timedelta
import pytz


app = Flask(__name__)


class Event:
    def __init__(self, name: str, begin: datetime, end: datetime, location: str, duration: str):
        self.name = name
        self.begin = begin
        self.end = end
        self.location = location
        self.duration = duration

    def __dict__(self):
        return {
            'name': self.name,
            'begin': self.begin,
            'end': self.end,
            'location': self.location,
            'duration': self.duration
        }


class Calendar:
    def __init__(self, url: str, timezone: pytz.timezone, timedelta: int):
        self.url = url
        self.timezone = timezone
        self.timedelta = timedelta
        self.calendar = self.get_calendar()

    def get_calendar(self) -> str | None:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return ics_Calendar(response.text)
        except requests.exceptions.RequestException as e:
            return None

    def adjust_event(self, event: str) -> Event:
        event_begin = event.begin
        event_end = event.end

        event_begin = event_begin.astimezone(self.timezone)
        event_end = event_end.astimezone(self.timezone)

        event_begin += timedelta(hours=self.timedelta)
        event_end += timedelta(hours=self.timedelta)

        return Event(event.name, event_begin, event_end, event.location, event.duration)

    def get_current_event(self) -> str | None:
        now = datetime.now(self.timezone)
        for event in self.calendar.timeline:
            adjusted_event = self.adjust_event(event)
            if adjusted_event.begin <= now <= adjusted_event.end:
                return adjusted_event
        return None

    def get_next_event(self) -> str | None:
        now = datetime.now(self.timezone)
        for event in self.calendar.timeline:
            adjusted_event = self.adjust_event(event)
            if now < adjusted_event.begin:
                return adjusted_event
        return None



@app.route('/')
def classes_info():
    ade_url = os.getenv('ADE_URL')
    timezone = pytz.timezone(os.getenv('TZ', 'Europe/Paris'))
    timedelta = int(os.getenv('TIME_DELTA', 0))

    calendar = Calendar(ade_url, timezone, timedelta)
    if not calendar:
        return "<p>Error fetching data<p>"

    current_event = calendar.get_current_event()
    next_event = calendar.get_next_event()

    if current_event:
        current_info = current_event.__dict__()
    else:
        current_info = None

    if next_event:
        next_info = next_event.__dict__()
    else:
        next_info = None

    return render_template('index.html', current=current_info, next=next_info)

