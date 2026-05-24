from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.entity import Entity
from src.core.video.domain.value_objects import Rating


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error("Title should not exceed 255 characters")

        if not self.title:
            self.notification.add_error("Title is required")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
