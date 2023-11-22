import uvicorn

from src.services.scheduler_service import cron


class Server(uvicorn.Server):
    """Customized uvicorn.Server"""

    def handle_exit(self, sig, frame) -> None:
        cron.clear()
        return super().handle_exit(sig, frame)
