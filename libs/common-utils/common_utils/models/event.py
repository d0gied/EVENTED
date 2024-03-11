from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: int
    name_ru: str
    name_en: str
    pivot: dict[str, int]


class Event(BaseModel):
    id: int
    type: Literal["projects", "ml", "remote", "hackathon", "meetup", "test"]
    name: str
    start_date: datetime | None
    end_date: datetime | None
    start_registration: datetime
    end_registration: datetime
    prize: str | None
    image_id: int
    team_limit: int
    min_team_limit: int
    show_count_members: int
    slug: str
    playground_mode: int
    status: str
    url: str
    blur_url: str
    users_count: int
    available_task_types: list[str]
    tags: list[Tag]


EventDict = dict[str, Any]
