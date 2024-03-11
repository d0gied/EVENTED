from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(None, description="The id of the event")
    name: str = Field(None, description="The name of the event")
    description: str = Field(None, description="The description of the event")

    class Config:
        extra = "allow"


EventDict = dict[str, Any]


class WithRegistration(Event):
    registration_link: str = Field(
        None, description="The link to the registration of the event"
    )
    registration_start_time: datetime = Field(
        None, description="The start time of the registration"
    )
    registration_end_time: datetime = Field(
        None, description="The end time of the registration"
    )


class LongEvent(Event):
    start_time: datetime = Field(None, description="The start time of the event")
    end_time: datetime = Field(None, description="The end time of the event")


class ShortEvent(Event):
    timestamp: datetime = Field(None, description="The time of the event")


class OnlineEvent(Event):
    link: str = Field(None, description="The link to the event")
    platform: str = Field(None, description="The platform where the event is hosted")


class OfflineEvent(Event):
    location: str = Field(None, description="The location of the event")


class HybridEvent(OnlineEvent, OfflineEvent):
    pass


class TeamEvent(LongEvent):
    max_team_size: int = Field(None, description="The maximum team size for the event")
    min_team_size: int = Field(None, description="The minimum team size for the event")


class IndividualEvent(LongEvent):
    pass


class Hackathon(LongEvent):
    prize: str = Field(None, description="The prize for the hackathon")
    rules: str = Field(None, description="The rules of the hackathon")


class Lecture(LongEvent):
    speaker: str = Field(None, description="The speaker of the lecture")
    topic: str = Field(None, description="The topic of the lecture")
