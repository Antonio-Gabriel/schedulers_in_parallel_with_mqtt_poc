import schedule as cron
from threading import Thread
from datetime import datetime
from typing import List, Callable

from src.db.in_momery_db import InMemoryDB
from src.services.mqtt_service import MQTTService

from src.DI.containers import Container
from dependency_injector.wiring import inject, Provide

from src.utils.format_date import format_date, DATE_FORMAT
from src.constants.out_colors import GREEN, WHITE, RED, ENDC


@inject
class SchedulerService:
    def __init__(self, memory_db: InMemoryDB = Provide[Container.memory_db],
                 mqtt_service: MQTTService = Provide[Container.mqtt_service]) -> None:
        self.__memory_db = memory_db
        self.__mqtt_service = mqtt_service

    def __run_schedule_threaded(self, job_action: Callable, triggered_date: datetime):

        time = triggered_date.strftime("%H:%M")

        worker_thread = Thread(target=job_action, args=(
            "mqtt-audio-encoded-to-broker", {"data": "eny data", "time": time}))
        worker_thread.start()

    def add_schedule(self, date: str, times: List[str]):
        self.__memory_db.save_schedulers(date, times)
        self.run_cron()

    def get_schedulers(self):
        return self.__memory_db.get_schedulers()

    def __schedule_task(self, primery_date: datetime, secondary_date: datetime):
        """shedule a task into cron"""
        task_list = [
            cron.every().day.at(date.strftime("%H:%M")).do(
                self.__run_schedule_threaded,
                self.__mqtt_service.publish_data_into_broker,
                triggered_date=date
            )
            for date in [primery_date, secondary_date]
        ]

        return task_list

    def run_cron(self):
        cron.clear()

        # TODO: Validate if the current date wasen't dispatched yet

        if len(self.__memory_db.get_schedulers()) == 0:
            print(f"[{RED}CRON{ENDC}]: {WHITE}NO SCHEDULERS AVAILABLE{ENDC}")
            return

        for schedule in self.__memory_db.get_schedulers():
            print(f"[{GREEN}CRON{ENDC}]: {WHITE}RELOADING SCHEDULERS LIST{ENDC}")

            current_date = datetime.now().date()
            scheduled_date = datetime.strptime(
                schedule.get("date"), DATE_FORMAT).date()

            # if current_date >= scheduled_date:
            #     return

            print("CHEGOU AQUI")
            for time in schedule.get("times"):
                primary_time, secondary_time = time.split('-')

                primary_date = format_date(schedule.get("date"), primary_time)
                secondary_date = format_date(
                    schedule.get("date"), secondary_time)

                self.__schedule_task(primary_date, secondary_date)
