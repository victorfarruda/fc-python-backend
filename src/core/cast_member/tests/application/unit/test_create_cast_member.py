from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.exceptions import InvalidCastMember


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository_mock = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=repository_mock)
        input = CreateCastMember.Input(
            name="Peter Jackson",
            type=CastMemberType.DIRECTOR,
        )

        output: CreateCastMember.Output = use_case.execute(input)

        assert isinstance(output, CreateCastMember.Output)
        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert repository_mock.save.called is True

    def test_create_cast_member_with_empty_name(self):
        repository_mock = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=repository_mock)
        input = CreateCastMember.Input(
            name="",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(
            InvalidCastMember, match="name cannot be empty"
        ) as exc_inf:
            use_case.execute(input)

        assert exc_inf.type is InvalidCastMember
        assert str(exc_inf.value) == "name cannot be empty"

    def test_create_cast_member_with_invalid_type(self):
        repository_mock = MagicMock(CastMemberRepository)
        use_case = CreateCastMember(repository=repository_mock)
        input = CreateCastMember.Input(
            name="Peter Jackson",
            type="WRITER",
        )

        with pytest.raises(
            InvalidCastMember, match="type must be either 'ACTOR' or 'DIRECTOR'"
        ) as exc_inf:
            use_case.execute(input)

        assert exc_inf.type is InvalidCastMember
        assert (
            str(exc_inf.value)
            == "type must be either 'ACTOR' or 'DIRECTOR'"
        )
