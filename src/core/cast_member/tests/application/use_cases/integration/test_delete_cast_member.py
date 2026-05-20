import uuid

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member import (
    InMemoryCastMemberRepository,
)


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Daniel Radcliffe",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = DeleteCastMember(repository)
        use_case.execute(DeleteCastMember.DeleteCastMemberInput(id=cast_member.id))

        assert repository.get_by_id(cast_member.id) is None
        assert len(repository.cast_members) == 0

    def test_when_cast_member_not_found_then_raise_exception(self):
        repository = InMemoryCastMemberRepository()
        request = DeleteCastMember.DeleteCastMemberInput(id=uuid.uuid4())
        use_case = DeleteCastMember(repository=repository)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)

        assert len(repository.cast_members) == 0
