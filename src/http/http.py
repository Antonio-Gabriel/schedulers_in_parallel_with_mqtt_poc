from typing import List
from fastapi import FastAPI

from src.models.time_model import TimeModel
from src.models.schedule_model import ScheduleModel

from src.db.in_momery_db import times
from src.DI.containers import Container
from src.services.scheduler_service import SchedulerService

app = FastAPI()

container = Container()
container.init_resources()
container.wire(modules=["src.services.scheduler_service"])

scheduler_service = SchedulerService()


@app.get('/', response_model=ScheduleModel)
def main():
    """main route"""

    return {
        "msg": "Welcome to schedule by threads app"
    }


@app.post("/time/register")
def register_time(time: TimeModel):
    """endpoint to register time into list"""

    times.append(time)

    return "Time registered successfully"


@app.get("/times")
def get_times() -> List[TimeModel]:
    """get times list"""
    return times


@app.post("/scheduler/register")
def register_scheduler(scheduler: ScheduleModel):
    """endpoint to register a scheduler"""

    scheduler_service.add_schedule(scheduler.date, scheduler.times)

    return "Schedule registered sucessfully"


@app.get("/schedules")
def get_schedules() -> List:
    """get all schedules"""
    return scheduler_service.get_schedulers()
