from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCastMember:
    def test_update_cast_member_name(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Test Director",
            type=CastMemberType.DIRECTOR,
        )
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository_mock)
        request = UpdateCastMember.Input(
            id=cast_member.id,
            name="Outher Director",
        )

        use_case.execute(request)

        assert cast_member.name == "Outher Director"
        assert cast_member.type == CastMemberType.DIRECTOR
        repository_mock.update.assert_called_once_with(cast_member)

    def test_update_cast_member_type(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Filme",
            type=CastMemberType.DIRECTOR,
        )
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository_mock)
        request = UpdateCastMember.Input(
            id=cast_member.id,
            type=CastMemberType.ACTOR,
        )

        use_case.execute(request)

        assert cast_member.name == "Filme"
        assert cast_member.type == CastMemberType.ACTOR
        repository_mock.update.assert_called_once_with(cast_member)

    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Director 1",
            type=CastMemberType.DIRECTOR,
        )
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository_mock)
        request = UpdateCastMember.Input(
            id=cast_member.id,
            name="Outher Person",
            type=CastMemberType.ACTOR,
        )

        use_case.execute(request)

        assert cast_member.name == "Outher Person"
        assert cast_member.type == CastMemberType.ACTOR
        repository_mock.update.assert_called_once_with(cast_member)

    def test_cannot_update_cast_member_not_found(self):
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = None

        use_case = UpdateCastMember(repository=repository_mock)
        request = UpdateCastMember.Input(
            id=uuid.uuid4(),
            name="Outher Person",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(Exception, match=f"CastMember with {request.id} not found"):
            use_case.execute(request)
