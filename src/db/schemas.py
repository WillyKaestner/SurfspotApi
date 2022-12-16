from typing import Optional
from pydantic import BaseModel
import datetime

class LocationBase(BaseModel):
    name: str
    kitespot: bool
    surfspot: bool
    best_wind: Optional[str] = ""
    best_tide: Optional[str] = ""
    wave_info: Optional[str] = ""


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: float
    created_at: datetime.datetime

    class Config:
        orm_mode = True
