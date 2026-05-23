from uuid import UUID

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.models import CastMemberModel


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def save(self, cast_member: CastMember):
        cast_member_model = CastMemberModelMapper.to_model(cast_member)
        cast_member_model.save()

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member = self.cast_member_model.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member)
        except self.cast_member_model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_model.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type.value,
        )

    def list(self) -> list[CastMember]:
        return [
            CastMemberModelMapper.to_entity(cast_member)
            for cast_member in self.cast_member_model.objects.all()
        ]


class CastMemberModelMapper:
    @staticmethod
    def to_model(cast_member: CastMember) -> CastMemberModel:
        return CastMemberModel(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type.value,
        )

    @staticmethod
    def to_entity(cast_member_model: CastMemberModel) -> CastMember:
        return CastMember(
            id=cast_member_model.id,
            name=cast_member_model.name,
            type=CastMemberType(cast_member_model.type),
        )
