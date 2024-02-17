from fastapi import FastAPI
import freeTime
import freeIntervals
import freebusy
from pydantic import BaseModel
from datetime import datetime
from typing import List
from datetime import datetime, time, timedelta

class TimeBounds(BaseModel):
    start: datetime
    end: datetime
    timezone: str
    calendar_ids: List[str]

class DayInfo(BaseModel):
    date: datetime
    timezone: str
    calendar_ids: List[str]

app = FastAPI()

@app.get('/specific-date')
async def spcefic(time: TimeBounds):

    start_str = time.start.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = time.end.strftime("%Y-%m-%dT%H:%M:%S")

    # Convert strings back to datetime for calculations
    start_datetime = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(end_str, "%Y-%m-%dT%H:%M:%S")

    # Calculate min and max
    min_datetime = start_datetime - timedelta(days=3.5)
    max_datetime = end_datetime + timedelta(days=3.5)

    # Convert back to strings
    min_str = min_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    max_str = max_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    response = freebusy.collectBusyTimes(min_str, max_str, time.calendar_ids)
    
    return freeTime.is_everyone_free(response, start_str, end_str)

@app.get('/full-day')
async def full(day: DayInfo):
    print(day)
    date = day.date

    # Set min and max to the start and end of the day
    min_datetime = datetime.combine(date, time.min)
    max_datetime = datetime.combine(date, time.max)

    # Convert to strings
    min_str = min_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    max_str = max_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    response = freebusy.collectBusyTimes("2024-02-17T10:00:00", "2024-02-17T12:00:00", day.calendar_ids)
    return freeIntervals.find_free_slots(response, date)
