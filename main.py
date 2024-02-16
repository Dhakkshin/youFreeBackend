from fastapi import FastAPI
import freeTime
import freeIntervals
import freebusy
from pydantic import BaseModel
from datetime import datetime
from typing import List

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

@app.get('/')
async def spcefic(time: TimeBounds):

    start_str = time.start.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = time.end.strftime("%Y-%m-%dT%H:%M:%S")

    response = freebusy.collectBusyTimes(time.calendar_ids)
    return freeTime.is_everyone_free(response, start_str, end_str)

@app.get('/full-day')
async def full(day: DayInfo):
    response = freebusy.collectBusyTimes(day.calendar_ids)
    freeIntervals.find_free_slots(response, day.date)
    return True