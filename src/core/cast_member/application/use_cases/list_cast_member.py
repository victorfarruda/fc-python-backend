from dataclasses import dataclass
from uuid import UUID

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
        mapped_cast_members = [
            CastMemberOutput(
                id=cast_member.id,
                name=cast_member.name,
                type=cast_member.type,
            )
            for cast_member in cast_members
        ]
        if input.order_by:
            mapped_cast_members.sort(key=lambda x: getattr(x, input.order_by))

        page_offset = (input.current_page - 1) * input.per_page
        paginated_cast_members = mapped_cast_members[
            page_offset : page_offset + input.per_page
        ]

        return self.Output(
            data=paginated_cast_members,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=input.per_page,
                total=len(mapped_cast_members),
            ),
        )
