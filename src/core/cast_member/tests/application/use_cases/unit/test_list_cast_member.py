from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(
        id=uuid.uuid4(),
        name="Actor Name",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def mock_cast_member_repository(actor_cast_member) -> CastMemberRepository:
    mock = create_autospec(CastMemberRepository)
    mock.list.return_value = [actor_cast_member]
    return mock


@pytest.fixture
def mock_empty_cast_member_repository() -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = []
    return repository


class TestListCastMember:
    def test_list_cast_member(self, actor_cast_member, mock_cast_member_repository):

        use_case = ListCastMember(repository=mock_cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 1

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(
                    id=actor_cast_member.id,
                    name=actor_cast_member.name,
                    type=actor_cast_member.type,
                )
            ]
        )

    def test_list_cast_member_empty(self, mock_empty_cast_member_repository):
        use_case = ListCastMember(repository=mock_empty_cast_member_repository)
        output = use_case.execute(input=ListCastMember.Input())

        assert len(output.data) == 0
        assert output == ListCastMember.Output(data=[])
