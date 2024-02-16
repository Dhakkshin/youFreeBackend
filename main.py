from fastapi import FastAPI
import freeTime
from pydantic import BaseModel
from datetime import datetime


class TimeBounds(BaseModel):
    start: datetime
    end: datetime
    timezone: str

# class FunctionResult(BaseModel):
#     isFree: bool  
#     unavailable: list

app = FastAPI()

@app.get('/')
async def root(time: TimeBounds):

    start_str = time.start.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = time.end.strftime("%Y-%m-%dT%H:%M:%S")

    return freeTime.is_everyone_free(freeTime.response, start_str, end_str)