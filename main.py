import csv
import os
from datetime import datetime
from datetime import timedelta

from csv_ical import Convert


def convert_ics_to_csv(filename):
    csv_filename = filename.replace("ics", "csv")
    convert = Convert()
    convert.read_ical("calendars/" + filename)
    convert.make_csv()
    convert.save_csv("csv/" + csv_filename)


def convert_all_calendars():
    for file in os.listdir("calendars"):
        convert_ics_to_csv(file)
        print(f"{file} calendar converted to csv")


def read_csv(filename):
    rows = []
    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            rows.append(row)
    return rows


def calendars_name_csv():
    return os.listdir("csv")


def extract_action(event):
    return event.split()[0].strip().lower()


def extract_project(event):
    if ":" in event:
        return event.split()[0].strip().lower()
    return "No Project"


def extract_area(event):
    if "@" in event:
        return event.split("@")[-1].strip().lower()
    return "No Area"


def extract_tag(event):
    if "#" in event:
        return event.split("#")[-1].strip().lower()
    return "No Tag"

def calculate_duration(start, end):
    start_time = datetime.fromisoformat(start)
    end_time = datetime.fromisoformat(end)
    duration = end_time - start_time
    return duration

def format_duration(duration):
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

def get_cal_events(calname):
    row = {}
    data = []
    for row in read_csv("csv/" + calname):
        event, start, end, desc, *_ = row
        row = {}
        row["action"] = extract_action(event)
        row["project"] = extract_project(event)
        row["area"] = extract_area(event)
        row["tag"] = extract_tag(event)
        row["duration"] = calculate_duration(start, end)
        data.append(row)
    return data


def grouping():
    pass

def parse_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def get_subcalendar(events):
    """ Calculate how much time spent on sub-calendar.
        A sub-calendar is in form of `sub-calendar: event detail`
    """

def calendar_duration(events):
    """Calculate how much time spend on a calendar."""
    # durations in timedelta format
    durations = [event.get("duration") for event in events]
    total_duration = sum(durations, timedelta())
    return total_duration


def main():
    calendars = calendars_name_csv()
    events = get_cal_events("work.csv")
    x = calendar_duration(events)


if __name__ == "__main__":
    main()
