import schedule as cron
from typing import List

from src.db.in_momery_db import InMemoryDB
from src.utils.format_date import format_date
from threading import Thread, current_thread, Lock, Event


class Scheduler:
    def __init__(self) -> None:
        self.__lock = Lock()
        self.__event = Event()
        self.__in_memory_db = InMemoryDB()

    def _print_with_lock(self, message: str):
        with self.__lock:
            print(message)

    def _dispatch_event_to_mqtt(self):
        self._print_with_lock("Job turned %s" % current_thread())

    def _run_schedule_threaded(self, job_action):
        worker_thread = Thread(target=job_action)
        worker_thread.start()

    def add_schedule(self, date: str, times: List[str]):
        with self.__lock:
            self.__in_memory_db.save_schedulers(date, times)
            self.__event.set()

    def get_schedulers(self):
        self.__in_memory_db.get_schedulers()

    def run_cron(self):
        while True:
            self.__event.wait()
            self.__event.clear()

            self._print_with_lock("Realoading event")

            cron.clear()

            for schedule in self.__in_memory_db.get_schedulers():
                for time in schedule.get("times"):
                    primary, secondary = time.split('-')

                    primary_date = format_date(schedule.get("date"), primary)
                    secondary_date = format_date(
                        schedule.get("date"), secondary)

                    cron.every().day.at(primary_date.strftime("%H:%M"))\
                        .do(self._run_schedule_threaded, self._dispatch_event_to_mqtt)

                    cron.every().day.at(secondary_date.strftime("%H:%M"))\
                        .do(self._run_schedule_threaded, self._dispatch_event_to_mqtt)
