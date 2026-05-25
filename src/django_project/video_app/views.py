from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
)

from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoWithoutMedia.Input(
            **serializer.validated_data,
        )

        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            genre_repository=DjangoORMGenreRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
        )
        output: CreateVideoWithoutMedia.Output = use_case.execute(input)

        cast_member_output = CreateVideoOutputSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=cast_member_output.data,
        )
