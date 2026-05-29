from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from src.core._shared.infra.storage.local_storage import LocalStorage
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from src.core.video.application.use_cases.delete_video import DeleteVideo
from src.core.video.application.use_cases.list_video import ListVideo
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.shared.views import get_params
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
    DeleteVideoInputSerializer,
    ListVideoOutputSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by, current_page, per_page = get_params(request, default_order_by="title")
        input = ListVideo.Input(
            order_by=order_by, current_page=current_page, per_page=per_page
        )
        use_case = ListVideo(repository=DjangoORMVideoRepository())
        output = use_case.execute(input)

        serializer = ListVideoOutputSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)

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

        video_output = CreateVideoOutputSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=video_output.data,
        )

    def destroy(self, request: Request, pk: str) -> Response:
        serializer = DeleteVideoInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = DeleteVideo.DeleteVideoInput(**serializer.validated_data)
        use_case = DeleteVideo(repository=DjangoORMVideoRepository())

        try:
            use_case.execute(input)
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk: str) -> Response:
        file = request.FILES.get("video_file")
        content = file.read()
        content_type = file.content_type

        use_case = UploadVideo(
            video_repository=DjangoORMVideoRepository(), storage_service=LocalStorage()
        )

        input_data = UploadVideo.Input(
            video_id=pk, file_name=file.name, content=content, content_type=content_type
        )
        try:
            use_case.execute(input_data)
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)
