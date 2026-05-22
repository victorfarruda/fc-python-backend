import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.models import CastMemberModel


@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(id=uuid.uuid4(), name="Some person", type=CastMemberType.ACTOR)
        cast_member_repository = DjangoORMCastMemberRepository()

        assert CastMemberModel.objects.count() == 0
        cast_member_repository.save(cast_member)

        assert CastMemberModel.objects.count() == 1
        cast_member_model = CastMemberModel.objects.first()
        assert cast_member_model.id == cast_member.id
        assert cast_member_model.name == cast_member.name
        assert cast_member_model.type == cast_member.type.value
