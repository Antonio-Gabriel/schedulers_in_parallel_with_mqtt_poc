from threading import current_thread

from src.constants.out_colors import GREEN, WHITE, ENDC


class MQTTService:

    def publish_data_into_broker(self, topic: str, data: dict):
        """publish data into a specific topic on mosquitto"""
        print(GREEN + "JOB TURNED %s" % current_thread() + ENDC)
        print(f"[{GREEN}SERVICE(MQTT){ENDC}]: {WHITE}PROCESSING DATA THOSE DATA {data} ON THIS TOPIC {topic} {ENDC}")
