import schedule as cron
from threading import Thread
from datetime import datetime
from typing import List, Callable

from src.db.in_momery_db import InMemoryDB
from src.services.mqtt_service import MQTTService

from src.DI.containers import Container
from dependency_injector.wiring import inject, Provide

from src.utils.format_date import format_date
from src.constants.out_colors import GREEN, WHITE, ENDC


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

    def run_cron(self):
        cron.clear()

        print(f"[{GREEN}CRON{ENDC}]: {WHITE}RELOADING SCHEDULERS LIST{ENDC}")

        # TODO: Validate if the current date wasen't dispatched yet

        if len(self.__memory_db.get_schedulers()) > 0:
            for schedule in self.__memory_db.get_schedulers():
                for time in schedule.get("times"):
                    primary, secondary = time.split('-')

                    primary_date = format_date(schedule.get("date"), primary)
                    secondary_date = format_date(
                        schedule.get("date"), secondary)

                    cron.every().day.at(primary_date.strftime("%H:%M"))\
                        .do(self.__run_schedule_threaded,
                            self.__mqtt_service.publish_data_into_broker, triggered_date=primary_date)

                    cron.every().day.at(secondary_date.strftime("%H:%M"))\
                        .do(self.__run_schedule_threaded,
                            self.__mqtt_service.publish_data_into_broker, triggered_date=secondary_date)
