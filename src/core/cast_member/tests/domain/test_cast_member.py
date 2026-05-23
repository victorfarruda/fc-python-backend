from uuid import UUID, uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    # def test_id_is_required(self):
    #     with pytest.raises(
    #         TypeError, match="missing 1 required positional argument: 'id'"
    #     ):
    #         CastMember(name="John Doe", type=CastMemberType("ACTOR"))

    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            CastMember(id=uuid4(), type=CastMemberType("ACTOR"))

    def test_name_cannot_be_empty(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(id=uuid4(), name="", type=CastMemberType("ACTOR"))

    def test_type_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'type'"
        ):
            CastMember(id=uuid4(), name="John Doe")

    def test_create_cast_member(self):
        cast_member = CastMember(
            id=uuid4(), name="John Doe", type=CastMemberType("ACTOR")
        )
        assert cast_member.name == "John Doe"
        assert cast_member.type == CastMemberType.ACTOR
        assert cast_member.id is not None
        assert isinstance(cast_member.id, UUID)
