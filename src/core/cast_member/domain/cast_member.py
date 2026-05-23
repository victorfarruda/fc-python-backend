from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID
from src.core._shared.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            self.notification.add_error("id must be a valid UUID")
            # raise ValueError("id must be a valid UUID")

        if not isinstance(self.name, str):
            self.notification.add_error("name must be a string")
            # raise ValueError("name must be a string")

        if not self.name:
            self.notification.add_error("name cannot be empty")
            # raise ValueError("name cannot be empty")

        if not isinstance(self.type, CastMemberType):
            self.notification.add_error("type must be either 'ACTOR' or 'DIRECTOR'")
            # raise ValueError("type must be either 'ACTOR' or 'DIRECTOR'")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

        self.type = CastMemberType(self.type)

    def __str__(self):
        return f"{self.name} ({self.type})"

    def __repr__(self):
        return f"{self.name} ({self.type})"

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def change_type(self, type: CastMemberType):
        self.type = type
        self.validate()
