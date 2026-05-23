from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMember,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMember,
)
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    DeleteCastMemberInputSerializer,
    ListCastMemberOutputSerializer,
    UpdateCastMemberInputSerializer,
)
from src.core.cast_member.application.exceptions import (
    CastMemberNotFound,
)

from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.core.cast_member.application.use_cases.list_cast_member import (
    ListCastMember,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        input = ListCastMember.Input(order_by=order_by)
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(input)

        serializer = ListCastMemberOutputSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMember.Input(
            **serializer.validated_data,
        )

        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        output: CreateCastMember.Output = use_case.execute(input)

        cast_member_output = CreateCastMemberOutputSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=cast_member_output.data,
        )

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCastMemberInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        input = UpdateCastMember.Input(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(input=input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCastMemberInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = DeleteCastMember.DeleteCastMemberInput(**serializer.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(input=input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
