from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.list_entity import output_entity
from src.core._shared.entity import ListOutputMeta
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = ""
        current_page: int = 1
        per_page: int = 2

    @dataclass
    class Output:
        data: list[CastMemberOutput]
        meta: ListOutputMeta

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()
        cast_member_list = [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
            for cast_member in cast_members
        ]

        meta, paginated_cast_members = output_entity(input, cast_member_list)
        return self.Output(
            data=paginated_cast_members,
            meta=meta,
        )
