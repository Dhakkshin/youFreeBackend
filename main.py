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

@app.post('/specific-date')
async def spcefic(time: TimeBounds):

    # Calculate min and max datetimes
    min_datetime = time.start - timedelta(days=3.5)
    max_datetime = time.end + timedelta(days=3.5)

    # Convert min and max datetimes to strings
    min_str = min_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    max_str = max_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    # Collect busy times
    response = freebusy.collectBusyTimes(min_str, max_str, time.calendar_ids)

    # Check availability
    print(min_datetime, max_datetime, time.start, time.end, sep='\n')
    return freeTime.is_everyone_free(response, time.start, time.end)



@app.post('/full-day')
async def full(day: DayInfo):
    print(day)
    date = day.date

    # Set min and max to the start and end of the day
    min_datetime = datetime.combine(date, time.min)
    max_datetime = datetime.combine(date, time.max)

    # Convert to strings
    min_str = min_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    max_str = max_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    response = freebusy.collectBusyTimes(min_str, max_str, day.calendar_ids)

    return freeIntervals.find_free_slots(response, date)
