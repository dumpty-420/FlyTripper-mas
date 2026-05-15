"""ICS calendar generation and response-cleaning helpers."""

import re
from datetime import datetime, timedelta

from icalendar import Calendar, Event


def generate_ics_content(
    plan_text: str,
    start_date: datetime | None = None,
) -> bytes:
    """Convert a day-by-day itinerary text into .ics calendar bytes."""
    cal = Calendar()
    cal.add("prodid", "-//Multi-Agent Travel Planner//")
    cal.add("version", "2.0")

    if start_date is None:
        start_date = datetime.today()

    cleaned = plan_text.replace("Final Answer:", "").strip()
    day_pattern = re.compile(r"Day (\d+)[:\s]+(.*?)(?=Day \d+|$)", re.DOTALL)
    days = day_pattern.findall(cleaned)

    if not days:
        # Fallback: single all-day event
        event = Event()
        event.add("summary", "Travel Itinerary")
        event.add("description", cleaned)
        event.add("dtstart", start_date.date())
        event.add("dtend", start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
    else:
        for day_num_str, day_content in days:
            day_num = int(day_num_str)
            current_date = start_date + timedelta(days=day_num - 1)
            event = Event()
            event.add("summary", f"Day {day_num} Itinerary")
            event.add("description", day_content.strip())
            event.add("dtstart", current_date.date())
            event.add("dtend", current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()


def clean_response(response: str) -> str:
    """Strip the 'Final Answer:' prefix from an agent response."""
    if "Final Answer:" in response:
        return response.split("Final Answer:", 1)[1].strip()
    return response.strip()
