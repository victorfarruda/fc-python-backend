from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.exceptions import CastMemberNotFound


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        type: str | None = None

    @dataclass
    class Output:
        id: UUID
        name: str
        type: str

    def execute(self, request: Input) -> None:
        cast_member: CastMember = self.repository.get_by_id(id=request.id)
        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with {request.id} not found")

        current_name = cast_member.name
        current_type = cast_member.type

        if request.name is not None:
            current_name = request.name

        if request.type is not None:
            current_type = CastMemberType(request.type)

        cast_member.change_name(name=current_name)
        cast_member.change_type(type=current_type)

        self.repository.update(cast_member)
