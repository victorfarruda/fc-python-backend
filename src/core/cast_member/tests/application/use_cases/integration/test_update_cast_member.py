import uuid

import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member import (
    InMemoryCastMemberRepository,
)


class TestUpdateCastMember:
    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Some Director",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMember.Input(
            id=cast_member.id, name="Some Actor", type=CastMemberType.ACTOR
        )
        use_case.execute(request)

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Some Actor"
        assert updated_cast_member.type == CastMemberType.ACTOR

    def test_update_cast_member_name(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Some Director",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMember.Input(id=cast_member.id, name="Some Person")
        use_case.execute(request)

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Some Person"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_update_cast_member_type(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Some Person",
            type=CastMemberType.DIRECTOR,
        )

        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMember.Input(id=cast_member.id, type=CastMemberType.ACTOR)
        use_case.execute(request)

        updated_cast_member = repository.get_by_id(cast_member.id)
        assert updated_cast_member.name == "Some Person"
        assert updated_cast_member.type == CastMemberType.ACTOR

    def test_cannot_update_cast_member_not_found(self):
        cast_member = CastMember(
            id=uuid.uuid4(),
            name="Some Actor",
            type=CastMemberType.ACTOR,
        )
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member)

        use_case = UpdateCastMember(repository=repository)
        request = UpdateCastMember.Input(
            id=uuid.uuid4(),
            name="Other Actor",
        )

        with pytest.raises(CastMemberNotFound):
            use_case.execute(request)
