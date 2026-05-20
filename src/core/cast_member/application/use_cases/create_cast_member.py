from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.core.cast_member.application.exceptions import (
    InvalidCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CreateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        name: str
        type: CastMemberType
        id: UUID = field(default_factory=uuid4)

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:
            cast_member = CastMember(
                id=input.id,
                name=input.name,
                type=input.type,
            )
        except ValueError as e:
            raise InvalidCastMember(e)

        self.repository.save(cast_member)
        return self.Output(
            id=cast_member.id,
        )
