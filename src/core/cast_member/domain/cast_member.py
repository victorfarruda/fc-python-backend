from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class CastMemberType(StrEnum):
    ACTOR = 'ACTOR'
    DIRECTOR = 'DIRECTOR'


@dataclass
class CastMember:
    id: UUID
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not isinstance(self.id, UUID):
            raise ValueError("id must be a valid UUID")

        if not isinstance(self.name, str):
            raise ValueError("name must be a string")

        if not self.name:
            raise ValueError("name cannot be empty")

        if not isinstance(self.type, CastMemberType):
            raise ValueError("type must be either 'ACTOR' or 'DIRECTOR'")

        self.type = CastMemberType(self.type)

    def __str__(self):
        return f"{self.name} ({self.type})"
    
    def __repr__(self):
        return f"{self.name} ({self.type})"

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False

        return self.id == other.id
