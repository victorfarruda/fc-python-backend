from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core._shared.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)

    notification: Notification = field(default_factory=Notification)

    def __post_init__(self):
        self.validate()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id


@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int
