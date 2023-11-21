from typing import List
from pydantic import BaseModel

from .time_model import TimeModel


class ScheduleModel(BaseModel):
    date: str
    times: List[str]

    def __init__(self, date: str, times: List[str]):
        super().__init__(date=date, times=times)
        self.date = date
        self.times = times
