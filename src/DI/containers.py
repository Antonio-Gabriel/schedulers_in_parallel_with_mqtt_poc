from dependency_injector import containers, providers

from src.db.in_momery_db import InMemoryDB
from src.services.mqtt_service import MQTTService


class Container(containers.DeclarativeContainer):

    memory_db = providers.Factory(
        InMemoryDB
    )

    mqtt_service = providers.Factory(
        MQTTService
    )
