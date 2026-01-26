from datetime import datetime


def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()

def parse_date(time_str):
    return datetime.strptime(time_str, '%Y-%m-%d').date()

def parse_start_end_date_time(event):
    date_event = event.date
    start_time = datetime.combine(date_event, event.start_time)
    end_time = datetime.combine(date_event, event.end_time)

    return start_time, end_time