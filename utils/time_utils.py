from datetime import datetime
from zoneinfo import ZoneInfo


def parse_datetime(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo("America/Havana"))

def parse_start_end_date_time(date, start_time, end_time):
    if date is None or start_time is None or end_time is None:
        return None, None
    
    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)
    
    start_dt = start_dt.replace(tzinfo=ZoneInfo("America/Havana"))
    end_dt = end_dt.replace(tzinfo=ZoneInfo("America/Havana"))

    return start_dt, end_dt
