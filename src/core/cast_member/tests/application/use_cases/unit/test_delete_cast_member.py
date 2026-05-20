import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Daniel Radcliffe",
            type=CastMemberType.ACTOR,
        )
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(repository_mock)
        use_case.execute(DeleteCastMember.DeleteCastMemberInput(id=cast_member.id))

        repository_mock.delete.assert_called_once_with(cast_member.id)

    def test_when_cast_member_not_found_then_raise_exception(self):
        repository_mock = create_autospec(CastMemberRepository)
        repository_mock.get_by_id.return_value = None
        use_case = DeleteCastMember(repository=repository_mock)
        request = DeleteCastMember.DeleteCastMemberInput(id=uuid.uuid4())
        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)

        repository_mock.delete.assert_not_called()
