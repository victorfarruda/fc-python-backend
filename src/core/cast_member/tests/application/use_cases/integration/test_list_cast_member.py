import uuid

import pytest

from src.core._shared.entity import ListOutputMeta
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(
        id=uuid.uuid4(),
        name="Actor Name",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def cast_member_repository(actor_cast_member) -> CastMemberRepository:
    repository = InMemoryCastMemberRepository()
    return repository


class TestListCastMember:
    def test_list_cast_member(self, actor_cast_member, cast_member_repository):
        cast_member_repository.save(actor_cast_member)
        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 1

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor_cast_member.id,
                    name=actor_cast_member.name,
                    type=actor_cast_member.type,
                )
            ],
            meta=ListOutputMeta(total=1, current_page=1, per_page=2),
        )

    def test_list_cast_member_empty(self, cast_member_repository):
        use_case = ListCastMember(repository=cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(
            data=[], meta=ListOutputMeta(total=0, current_page=1, per_page=2)
        )
