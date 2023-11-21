import json

from typing import List
from pathlib import Path

from src.config import ROOT
from src.models.time_model import TimeModel

times: List[TimeModel] = []

class InMemoryDB:
  def __init__(self) -> None:
    self.__schedulers = []
    self.__source = Path(f"{ROOT}/db/schedulers.json")

    if len(json.loads(self.__source.read_text())) > 0:
      self.__schedulers.append(json.loads(self.__source.read_text())[0])

  def save_schedulers(self, date: str, times: List[str]):
    """adding schedulers into file db"""
    schedule_payload = {
      "date": date,
      "times": times
    }

    self.__schedulers.append(schedule_payload)
    dump_to_json = json.dumps(self.__schedulers, indent=1)

    self.__source.write_text(dump_to_json)
  
  def get_schedulers(self):
    """return schedulers from file db"""
    return self.__schedulers
