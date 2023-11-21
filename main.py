import uvicorn

from threading import Thread, Event

from src.http.http import app
from src.cron.scheduler import Scheduler

# Event to sinalize when fastapi server is ready
server_ready_event = Event()


def server_thread():
    """fastapi server thread"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # Notify that the server is ready
    server_ready_event.set()


def scheduler_thread():
    """cron thread"""
    scheduler = Scheduler()
    scheduler.run_cron()


if __name__ == "__main__":
    fastapi_thread = Thread(target=server_thread)
    fastapi_thread.start()

    # Wait the signal get when fastapi server was ready
    server_ready_event.wait()

    cron_thread = Thread(target=scheduler_thread)
    cron_thread.start()

    fastapi_thread.join()
    cron_thread.join()
