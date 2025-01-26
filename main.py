import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

from csv_ical import Convert

BASE_DIR = Path(__file__).resolve().parent
CAL_DIR = BASE_DIR / "cals"
CSV_DIR = BASE_DIR / "csv"


def convert_ics_to_csv(filename):
    csv_filename = filename.replace("ics", "csv")
    convert = Convert()
    convert.read_ical(CAL_DIR / filename)
    convert.make_csv()
    convert.save_csv(CSV_DIR / filename)
    return True

def convert_all_ics_to_csv():
    """ Read all calendars and convert theme to csv file."""
    cals = os.listdir(CAL_DIR)
    for cal in cals:
        print(f"Calendar {cal} converted to csv successfuly.")
        if not convert_ics_to_csv(cal):
            print(f"Problem happend on convert_ics_to_csv")
            return False
    print("All calendars converted successfully.")
    return True

    

# 1
def clear_cals_name():
    cals = os.listdir(CAL_DIR)
    for cal in cals:
        cal_name = cal.split("_")[0].lower() + ".ics"
        old_name = CAL_DIR / cal
        new_name = CAL_DIR / cal_name
        # print(old_name, '-->', new_name)
        os.rename(old_name, new_name)


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


def extract_action(event):
    return event.split()[0].strip().lower()


def extract_project(event):
    if ":" in event:
        return event.split()[0].strip().lower()
    return "No Project"


def extract_area(event):
    if ":" in event:
        return event.split(":")[0].strip().lower()
    return event


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
    return int(hours), int(minutes)


def get_cal_events(calname):
    row = {}
    data = []
    for row in read_csv(CSV_DIR / calname):
        event, start, end, desc, *_ = row
        row = {}
        row["area"] = extract_area(event)
        row["duration"] = calculate_duration(start, end)
        data.append(row)
    return data


def grouping():
    pass


def get_analysis_by_week():
    pass


def get_analysis_by_month():
    pass


def parse_time(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def extract_subcalendar(events):
    """Calculate how much time spent on sub-calendar.
    A sub-calendar is in form of `sub-calendar: event detail`
    """
    subcal_dur = {}
    for event in events:
        subcal = event.get("area")
        dur = event.get("duration")
        if subcal in subcal_dur:
            subcal_dur[subcal] += dur
        else:
            subcal_dur[subcal] = dur

    subcal_formatted = {}
    for subcal, dur in subcal_dur.items():
        hour, minute = format_duration(dur)
        subcal_formatted[subcal] = f"{hour:0>2}:{minute:0>2}"

    return subcal_formatted



def calendar_duration(events):
    """Calculate how much time spend on a calendar."""
    # durations in timedelta format
    durations = [event.get("duration") for event in events]
    total_duration = sum(durations, timedelta())
    hour, minute = format_duration(total_duration)
    return f"{hour:0>2}:{minute:0>2}"

# ui
def print_cal_dur():
    calendars = os.listdir(CAL_DIR)
    for calendar in calendars:
        events = get_cal_events(calendar)
        dur = calendar_duration(events)
        print(calendar, "-->", dur)


def main():
    # 1. cleaer calendars name
    # clear_cals_name()
    # 2. make csv file out of ics files
    # convert_all_ics_to_csv()
    # print_cal_dur()
    events = get_cal_events("growth.ics")
    x = extract_subcalendar(events)
    print(x)




if __name__ == "__main__":
    main()
