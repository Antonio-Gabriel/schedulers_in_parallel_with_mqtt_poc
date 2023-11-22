import asyncio
import uvicorn

from server import Server
from src.http.http import app

from src.services.scheduler_service import SchedulerService, cron


async def scheduler_thread():
    """cron thread"""
    scheduler = SchedulerService()
    scheduler.run_cron()


# v.jinsha@tcs.com

async def run_cron():
    while True:
        cron.run_pending()
        await asyncio.sleep(1)


async def main():
    server = Server(config=uvicorn.Config(
        app, workers=1, loop='asyncio', port=8000, host="127.0.0.1")
    )

    api = asyncio.create_task(server.serve())
    cron_threads = asyncio.create_task(scheduler_thread())
    pending_schedulers_process = asyncio.create_task(run_cron())

    await asyncio.gather(api, cron_threads, pending_schedulers_process)

if __name__ == "__main__":
    asyncio.run(main())
