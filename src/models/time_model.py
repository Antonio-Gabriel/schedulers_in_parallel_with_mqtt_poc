from typing import Optional
from pydantic import BaseModel


class TimeModel(BaseModel):
    primary_time: str
    secondary_time: str
    primary_frase: str
    secondary_frase: str
